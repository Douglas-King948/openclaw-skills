#!/usr/bin/env python3
"""
Smart Meme v3 - 自愈模块
受控的自动修复功能
"""

from typing import Dict, List
from core.store import get_store
from core.download import MemeDownloader
from evolve.health import get_checker
import config


class SelfHealer:
    """
    自愈控制器
    
    重要安全特性:
    1. 只处理已明确识别的问题
    2. 自动补充有熔断机制保护
    3. 可以手动关闭
    4. 详细日志记录
    """
    
    def __init__(self):
        self.store = get_store()
        self.checker = get_checker()
        self.downloader = MemeDownloader()
    
    def heal(self, dry_run: bool = False) -> Dict:
        """
        执行自愈操作
        
        Args:
            dry_run: True=只检查不执行，False=实际执行
        
        Returns:
            操作结果报告
        """
        results = {
            "dry_run": dry_run,
            "actions": [],
            "success": True
        }
        
        # 先执行健康检查
        health = self.checker.check_all()
        results["health_check"] = health
        
        if not config.FEATURES["auto_restock"]:
            results["actions"].append({
                "type": "skip",
                "reason": "auto_restock功能已关闭"
            })
            return results
        
        # 处理库存不足
        low_stock_issues = [i for i in health["issues"] if i["type"] == "low_stock"]
        for issue in low_stock_issues:
            for cat in issue.get("categories", []):
                if dry_run:
                    results["actions"].append({
                        "type": "would_restock",
                        "category": cat,
                        "status": "planned"
                    })
                else:
                    # 实际执行补充
                    success, skip = self.downloader.download_category(cat)
                    results["actions"].append({
                        "type": "restock",
                        "category": cat,
                        "downloaded": success,
                        "skipped": skip,
                        "status": "completed" if success > 0 else "failed"
                    })
        
        # 处理损坏文件（标记为待清理）
        broken_issues = [i for i in health["issues"] if i["type"] == "broken_files"]
        for issue in broken_issues:
            results["actions"].append({
                "type": "cleanup_needed",
                "count": issue["count"],
                "note": "请手动运行清理脚本"
            })
        
        return results
    
    def restock_category(self, category: str, dry_run: bool = False) -> Dict:
        """
        补充指定分类
        
        Args:
            category: 分类名
            dry_run: 是否只检查
        
        Returns:
            操作结果
        """
        if dry_run:
            current = self.store.count(category)
            return {
                "category": category,
                "current_count": current,
                "would_download": len(config.MEME_SOURCES.get(category, [])),
                "dry_run": True
            }
        
        success, skip = self.downloader.download_category(category)
        return {
            "category": category,
            "downloaded": success,
            "skipped": skip,
            "dry_run": False
        }


# 便捷函数
healer = None

def get_healer() -> SelfHealer:
    """获取自愈器实例"""
    global healer
    if healer is None:
        healer = SelfHealer()
    return healer


def heal(dry_run: bool = False) -> Dict:
    """
    执行自愈（带安全检查）
    
    只有当auto_restock=True时才会实际执行
    """
    return get_healer().heal(dry_run)


def check_and_heal() -> Dict:
    """
    检查并自愈（触发式）
    
    典型用法：在发送表情包时调用
    如果库存不足，自动尝试补充
    """
    checker = get_checker()
    healer = get_healer()
    
    health = checker.check_all()
    
    # 只有当有库存不足问题且功能开启时才执行
    if not config.FEATURES["auto_restock"]:
        return {
            "action": "skipped",
            "reason": "auto_restock disabled",
            "health": health
        }
    
    low_stock = [i for i in health["issues"] if i["type"] == "low_stock"]
    if not low_stock:
        return {
            "action": "none_needed",
            "health": health
        }
    
    # 执行自愈
    return healer.heal(dry_run=False)
