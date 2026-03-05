#!/usr/bin/env python3
"""
Smart Meme v3 - 存储模块
使用JSON文件存储，避免SQLite并发问题
带SHA256去重（分块计算，防内存爆炸）
"""

import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Optional
import config


class MemeStore:
    """
    表情包存储管理
    - 使用JSON文件，无并发锁定问题
    - SHA256分块计算，防止内存爆炸
    - 自动备份，防数据损坏
    """
    
    def __init__(self):
        self.db_file = config.DB_FILE
        self.meme_dir = config.MEME_DIR
        self._data = None
        self._load()
    
    def _load(self):
        """加载数据库，失败时使用空数据"""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                # 文件损坏，从备份恢复
                backup = self.db_file.with_suffix('.json.bak')
                if backup.exists():
                    try:
                        with open(backup, 'r', encoding='utf-8') as f:
                            self._data = json.load(f)
                    except:
                        self._data = {"memes": [], "stats": {}}
                else:
                    self._data = {"memes": [], "stats": {}}
        else:
            self._data = {"memes": [], "stats": {}}
    
    def _save(self):
        """保存数据库，带备份机制"""
        # 先备份旧文件
        if self.db_file.exists():
            backup = self.db_file.with_suffix('.json.bak')
            try:
                backup.write_text(self.db_file.read_text(), encoding='utf-8')
            except:
                pass  # 备份失败继续保存
        
        # 原子写入
        temp_file = self.db_file.with_suffix('.json.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
        temp_file.replace(self.db_file)
    
    def _calculate_sha256(self, file_path: Path) -> str:
        """
        分块计算SHA256，防止内存爆炸
        关键安全机制！
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(config.CHUNK_SIZE)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def exists(self, sha256: str) -> bool:
        """检查是否已存在"""
        return any(m.get("sha256") == sha256 for m in self._data["memes"])
    
    def add(self, file_path: Path, category: str, tags: List[str] = None) -> bool:
        """
        添加表情包
        返回: True=成功, False=已存在或失败
        """
        if not file_path.exists():
            return False
        
        # 检查文件大小
        file_size = file_path.stat().st_size
        if file_size > config.MAX_FILE_SIZE_MB * 1024 * 1024:
            return False  # 文件太大
        
        # 计算SHA256（分块，安全）
        try:
            sha256 = self._calculate_sha256(file_path)
        except (IOError, OSError):
            return False
        
        # 检查重复
        if self.exists(sha256):
            return False
        
        # 添加记录
        meme = {
            "id": f"{category}_{len(self._data['memes'])}",
            "path": str(file_path),
            "category": category,
            "sha256": sha256,
            "size": file_size,
            "tags": tags or [],
            "created_at": time.time()
        }
        self._data["memes"].append(meme)
        self._update_stats()
        self._save()
        return True
    
    def get_random(self, category: str = None) -> Optional[Dict]:
        """随机获取一个表情包"""
        import random
        
        candidates = self._data["memes"]
        if category:
            candidates = [m for m in candidates if m["category"] == category]
        
        if not candidates:
            return None
        
        return random.choice(candidates)
    
    def count(self, category: str = None) -> int:
        """统计数量"""
        if category:
            return sum(1 for m in self._data["memes"] if m["category"] == category)
        return len(self._data["memes"])
    
    def list_categories(self) -> List[str]:
        """列出所有分类"""
        return list(set(m["category"] for m in self._data["memes"]))
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self._data["memes"]:
            return {
                "total_count": 0,
                "total_size_mb": 0,
                "categories": {cat: 0 for cat in config.CATEGORIES}
            }
        
        total_size = sum(m.get("size", 0) for m in self._data["memes"])
        categories = {cat: self.count(cat) for cat in config.CATEGORIES}
        
        return {
            "total_count": len(self._data["memes"]),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "categories": categories
        }
    
    def check_storage_limit(self) -> bool:
        """检查是否超过存储上限"""
        stats = self.get_stats()
        return stats["total_size_mb"] < config.MAX_STORAGE_MB
    
    def remove(self, meme_id: str) -> bool:
        """删除表情包"""
        original_len = len(self._data["memes"])
        self._data["memes"] = [m for m in self._data["memes"] if m["id"] != meme_id]
        if len(self._data["memes"]) < original_len:
            self._update_stats()
            self._save()
            return True
        return False
    
    def _update_stats(self):
        """更新统计数据"""
        self._data["stats"] = self.get_stats()


# 单例模式
_store = None

def get_store() -> MemeStore:
    """获取存储实例（单例）"""
    global _store
    if _store is None:
        _store = MemeStore()
    return _store
