#!/usr/bin/env python3
"""
Smart Meme - 直接发送接口
直接发送表情包图片文件
"""

import sys
from pathlib import Path
from typing import Optional

# 确保可以导入本地模块
sys.path.insert(0, str(Path(__file__).parent))

from core.selector import random_meme
import config


def send_random_meme(category: Optional[str] = None) -> dict:
    """
    发送随机表情包（返回图片路径，供外部调用）
    
    Args:
        category: 指定分类，None表示随机
        
    Returns:
        {
            "success": bool,
            "file_path": str | None,
            "category": str | None,
            "error": str | None
        }
    """
    try:
        # 获取随机表情包
        meme = random_meme(category)
        
        if not meme:
            return {
                "success": False,
                "file_path": None,
                "category": None,
                "error": f"没有找到{'分类 ' + category if category else ''} 的表情包，请先运行下载"
            }
        
        file_path = meme.get("path")
        meme_category = meme.get("category", "unknown")
        
        # 检查文件是否存在
        if not Path(file_path).exists():
            return {
                "success": False,
                "file_path": None,
                "category": meme_category,
                "error": f"表情包文件不存在: {file_path}"
            }
        
        return {
            "success": True,
            "file_path": file_path,
            "category": meme_category,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "file_path": None,
            "category": None,
            "error": str(e)
        }


def get_meme_by_keyword(keyword: str) -> dict:
    """
    根据关键词获取表情包
    
    支持的关键词映射：
    - 熊猫头, panda -> panda
    - 猫咪, 猫, cat, cats -> cats
    - 狗狗, 狗, dog, dogs -> dogs
    - 动漫, anime -> anime
    - 武侠, wuxia -> wuxia
    - 动物, animal, animals -> animals
    - 程序员, programmer -> programmer
    
    Args:
        keyword: 用户输入的关键词
        
    Returns:
        同 send_random_meme 的返回值
    """
    keyword = keyword.lower().strip()
    
    # 关键词映射表
    keyword_map = {
        # 熊猫头
        "熊猫头": "panda",
        "熊猫": "panda",
        "panda": "panda",
        "滚滚": "panda",
        
        # 猫咪
        "猫咪": "cats",
        "猫": "cats",
        "cat": "cats",
        "cats": "cats",
        "喵喵": "cats",
        "kitty": "cats",
        
        # 狗狗
        "狗狗": "dogs",
        "狗": "dogs",
        "dog": "dogs",
        "dogs": "dogs",
        "汪汪": "dogs",
        "puppy": "dogs",
        
        # 动漫
        "动漫": "anime",
        "anime": "anime",
        "二次元": "anime",
        "动画": "anime",
        
        # 武侠
        "武侠": "wuxia",
        "wuxia": "wuxia",
        "功夫": "wuxia",
        
        # 动物
        "动物": "animals",
        "animals": "animals",
        "animal": "animals",
        
        # 程序员
        "程序员": "programmer",
        "programmer": "programmer",
        "码农": "programmer",
        "coding": "programmer",
        "code": "programmer",
        
        # 杂项
        "杂项": "misc",
        "misc": "misc",
        "其他": "misc",
        "other": "misc",
    }
    
    # 查找匹配的类别
    category = keyword_map.get(keyword)
    
    # 如果没找到，尝试检查是否是有效类别
    if category is None and keyword in config.CATEGORIES:
        category = keyword
    
    return send_random_meme(category)


def list_categories() -> list:
    """列出所有可用的表情包分类"""
    return config.CATEGORIES


def check_stock() -> dict:
    """
    检查库存状态
    
    Returns:
        {
            "total": int,
            "categories": {cat: count},
            "empty_categories": [str]
        }
    """
    from core.selector import get_stats
    
    try:
        stats = get_stats()
    except Exception as e:
        # 如果获取失败，返回空库存
        return {
            "total": 0,
            "categories": {cat: 0 for cat in config.CATEGORIES},
            "empty_categories": list(config.CATEGORIES),
            "error": str(e)
        }
    
    empty_cats = []
    categories_stats = {}
    
    for cat in config.CATEGORIES:
        count = stats.get("categories", {}).get(cat, 0)
        categories_stats[cat] = count
        if count == 0:
            empty_cats.append(cat)
    
    return {
        "total": stats.get("total_count", 0),
        "categories": categories_stats,
        "empty_categories": empty_cats
    }


# 便捷函数
send_meme = send_random_meme  # 别名


if __name__ == "__main__":
    # 测试
    import json
    
    print("测试发送随机表情包:")
    result = send_random_meme()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n测试按关键词获取:")
    result = get_meme_by_keyword("熊猫头")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n当前库存:")
    stock = check_stock()
    print(f"总数: {stock['total']}")
    print(f"分类: {stock['categories']}")
    if stock['empty_categories']:
        print(f"空库存分类: {stock['empty_categories']}")
