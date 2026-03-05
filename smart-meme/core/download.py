#!/usr/bin/env python3
"""
Smart Meme v3 - 下载模块
带熔断机制，防无限循环
"""

import time
import requests
from pathlib import Path
from typing import Tuple, Optional, Dict
import config
from core.store import get_store


class CircuitBreaker:
    """
    熔断器 - 防止无限循环的关键安全机制
    
    工作原理:
    - 连续失败3次后，进入冷却期
    - 冷却期内拒绝所有请求
    - 冷却期后重置计数
    """
    
    def __init__(self, max_failures: int = 3, cooldown: int = 300):
        self.max_failures = max_failures
        self.cooldown = cooldown  # 秒
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED(正常), OPEN(熔断)
    
    def can_execute(self) -> bool:
        """检查是否可以执行"""
        if self.state == "OPEN":
            # 检查冷却期是否结束
            if time.time() - self.last_failure_time > self.cooldown:
                self.state = "CLOSED"
                self.failure_count = 0
                return True
            return False
        return True
    
    def record_success(self):
        """记录成功"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.max_failures:
            self.state = "OPEN"
            print(f"[熔断器] 连续失败{self.max_failures}次，进入冷却期{self.cooldown}秒")


class MemeDownloader:
    """
    安全下载器
    - 熔断机制防无限循环
    - 存储上限检查
    - 重试机制
    """
    
    def __init__(self):
        self.store = get_store()
        self.breaker = CircuitBreaker(
            max_failures=config.MAX_RETRY,
            cooldown=config.COOLDOWN_SECONDS
        )
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def download_file(self, url: str, save_path: Path, timeout: int = 15) -> bool:
        """
        下载单个文件，带重试
        返回: True=成功, False=失败
        """
        # 检查熔断器
        if not self.breaker.can_execute():
            print(f"[跳过] 熔断器开启中，拒绝下载")
            return False
        
        # 检查存储上限
        if not self.store.check_storage_limit():
            print(f"[跳过] 存储空间已满(>{config.MAX_STORAGE_MB}MB)")
            return False
        
        # 尝试下载
        for attempt in range(config.MAX_RETRY):
            try:
                resp = self.session.get(url, timeout=timeout, stream=True)
                if resp.status_code == 200:
                    # 检查文件大小
                    content_length = int(resp.headers.get('content-length', 0))
                    if content_length > config.MAX_FILE_SIZE_MB * 1024 * 1024:
                        print(f"[失败] 文件太大({content_length/1024/1024:.1f}MB)")
                        self.breaker.record_failure()
                        return False
                    
                    # 下载并保存
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(save_path, 'wb') as f:
                        for chunk in resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    self.breaker.record_success()
                    return True
                else:
                    print(f"[尝试{attempt+1}] HTTP {resp.status_code}")
            except requests.RequestException as e:
                print(f"[尝试{attempt+1}] 网络错误: {e}")
                if attempt < config.MAX_RETRY - 1:
                    time.sleep(1)
        
        # 所有尝试失败
        self.breaker.record_failure()
        return False
    
    def download_category(self, category: str, force: bool = False) -> Tuple[int, int]:
        """
        下载整个分类的表情包
        
        Args:
            category: 分类名
            force: 是否强制重新下载
        
        Returns:
            (成功数, 跳过数)
        """
        if category not in config.MEME_SOURCES:
            print(f"[错误] 未知分类: {category}")
            return (0, 0)
        
        # 检查熔断器
        if not self.breaker.can_execute():
            print(f"[跳过] 熔断器开启中，请{config.COOLDOWN_SECONDS}秒后再试")
            return (0, 0)
        
        cat_dir = config.MEME_DIR / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        skip_count = 0
        
        print(f"\n[下载] 分类: {category}")
        
        for url, filename in config.MEME_SOURCES[category]:
            save_path = cat_dir / filename
            
            # 检查是否已存在
            if save_path.exists() and not force:
                # 检查是否已在数据库中
                # 如果文件存在但未入库，则尝试添加
                if not force:
                    print(f"  [跳过] {filename}")
                    skip_count += 1
                    continue
            
            print(f"  [下载] {filename}...", end=" ")
            
            if self.download_file(url, save_path):
                # 添加到数据库
                if self.store.add(save_path, category, []):
                    print("OK (已入库)")
                    success_count += 1
                else:
                    print("OK (重复，未入库)")
                    skip_count += 1
            else:
                print("FAIL")
        
        return (success_count, skip_count)
    
    def download_all(self, force: bool = False) -> Dict[str, Tuple[int, int]]:
        """下载所有分类"""
        results = {}
        for category in config.CATEGORIES:
            results[category] = self.download_category(category, force)
            # 分类之间稍微延迟，避免请求过快
            time.sleep(0.5)
        return results


# 便捷函数
def download_all(force: bool = False) -> Dict:
    """下载所有表情包"""
    dl = MemeDownloader()
    return dl.download_all(force)


def download_category(category: str, force: bool = False) -> Tuple[int, int]:
    """下载指定分类"""
    dl = MemeDownloader()
    return dl.download_category(category, force)
