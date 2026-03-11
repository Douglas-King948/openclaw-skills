#!/usr/bin/env python3
"""
Smart Meme v3 - 选择器模块
只读操作，零风险
"""

import random
from typing import Optional, Dict, List
from core.store import get_store
import config


class MemeSelector:
    """
    表情包选择器
    - 只读操作，不会修改数据
    - 支持多种选择策略
    """
    
    def __init__(self):
        self.store = get_store()
    
    def random(self, category: str = None) -> Optional[Dict]:
        """
        随机选择一个表情包
        
        Args:
            category: 指定分类，None表示所有
        
        Returns:
            表情包信息字典，没有则返回None
        """
        return self.store.get_random(category)
    
    def by_category(self, category: str) -> List[Dict]:
        """
        获取指定分类的所有表情包
        
        Args:
            category: 分类名
        
        Returns:
            表情包列表
        """
        # 简单的筛选，从store获取
        all_memes = self.store._data.get("memes", [])
        return [m for m in all_memes if m["category"] == category]
    
    def stats(self) -> Dict:
        """获取统计信息"""
        return self.store.get_stats()
    
    def categories(self) -> List[str]:
        """列出所有分类"""
        return config.CATEGORIES
    
    def check_low_stock(self, threshold: int = 5) -> List[str]:
        """
        检查库存不足的分类
        
        Args:
            threshold: 低于此数量视为不足
        
        Returns:
            库存不足的分类列表
        """
        low = []
        for cat in config.CATEGORIES:
            if self.store.count(cat) < threshold:
                low.append(cat)
        return low


# 便捷函数
_selector = None

def get_selector() -> MemeSelector:
    """获取选择器实例"""
    global _selector
    if _selector is None:
        _selector = MemeSelector()
    return _selector


def random_meme(category: str = None) -> Optional[Dict]:
    """随机获取一个表情包"""
    return get_selector().random(category)


def get_stats() -> Dict:
    """获取统计信息"""
    return get_selector().stats()
