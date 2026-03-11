#!/usr/bin/env python3
"""
Smart Meme v3 - 健康检查模块
只读检查，安全可控
"""

from pathlib import Path
from typing import List, Dict, Tuple
from core.store import get_store
from core.selector import get_selector
import config


class HealthChecker:
    """
    健康检查器
    - 只读操作，不修改任何数据
    - 生成检查报告，供决策者参考
    """
    
    def __init__(self):
        self.store = get_store()
        self.selector = get_selector()
    
    def check_all(self) -> Dict:
        """
        全面健康检查
        
        Returns:
            {
                "healthy": bool,
                "issues": List[Dict],
                "recommendations": List[str]
            }
        """
        issues = []
        recommendations = []
        
        # 1. 检查存储空间
        storage_ok, storage_msg = self._check_storage()
        if not storage_ok:
            issues.append({
                "type": "storage_full",
                "level": "critical",
                "message": storage_msg
            })
            recommendations.append("清理旧表情包或增加存储上限")
        
        # 2. 检查库存数量
        low_stock = self.selector.check_low_stock(threshold=3)
        if low_stock:
            issues.append({
                "type": "low_stock",
                "level": "warning",
                "message": f"以下分类库存不足: {', '.join(low_stock)}",
                "categories": low_stock
            })
            if config.FEATURES["auto_restock"]:
                recommendations.append(f"自动补充功能将尝试补充: {low_stock}")
            else:
                recommendations.append(f"建议手动补充: {low_stock}")
        
        # 3. 检查损坏文件
        broken = self._check_broken_files()
        if broken:
            issues.append({
                "type": "broken_files",
                "level": "warning",
                "message": f"发现{broken}个损坏文件",
                "count": broken
            })
            recommendations.append("运行清理脚本移除损坏文件")
        
        # 4. 检查空分类
        empty_cats = self._check_empty_categories()
        if empty_cats:
            issues.append({
                "type": "empty_categories",
                "level": "info",
                "message": f"以下分类为空: {', '.join(empty_cats)}",
                "categories": empty_cats
            })
        
        # 5. 生成统计
        stats = self.selector.stats()
        
        return {
            "healthy": len([i for i in issues if i["level"] == "critical"]) == 0,
            "issues": issues,
            "recommendations": recommendations,
            "stats": stats
        }
    
    def _check_storage(self) -> Tuple[bool, str]:
        """检查存储空间"""
        if not self.store.check_storage_limit():
            stats = self.selector.stats()
            return (False, f"存储已满: {stats['total_size_mb']}MB / {config.MAX_STORAGE_MB}MB")
        return (True, "存储空间充足")
    
    def _check_broken_files(self) -> int:
        """检查损坏文件数量"""
        broken = 0
        for meme in self.store._data.get("memes", []):
            path = Path(meme["path"])
            if not path.exists():
                broken += 1
        return broken
    
    def _check_empty_categories(self) -> List[str]:
        """检查空分类"""
        empty = []
        for cat in config.CATEGORIES:
            if self.store.count(cat) == 0:
                empty.append(cat)
        return empty


# 便捷函数
checker = None

def get_checker() -> HealthChecker:
    """获取检查器实例"""
    global checker
    if checker is None:
        checker = HealthChecker()
    return checker


def check() -> Dict:
    """快速健康检查"""
    return get_checker().check_all()
