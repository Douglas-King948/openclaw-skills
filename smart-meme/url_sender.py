#!/usr/bin/env python3
"""
Smart Meme - URL 直接发送模块
通过 URL 直接发送表情包，自动检测并处理 JSON API 响应
"""

import random
import re
from typing import Optional
from url_sources import MEME_URLS, KEYWORD_MAP, categories


def is_direct_image_url(url: str) -> bool:
    """
    检查 URL 是否可能是直接图片链接
    规则：包含图片扩展名，且不是明显的 API 端点
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
    url_lower = url.lower()
    
    # 检查是否有图片扩展名
    has_extension = any(url_lower.endswith(ext) for ext in image_extensions)
    
    # 检查是否是已知的 JSON API 模式
    api_patterns = [
        r'/api/',
        r'/api\.',
        r'\.json',
        r'/v\d+/',
        r'/search',
        r'nekos\.life',  # 已知返回 JSON
        r'waifu\.im',    # 已知返回 JSON
        r'waifu\.pics',  # 已知返回 JSON
    ]
    
    is_api = any(re.search(pattern, url_lower) for pattern in api_patterns)
    
    return has_extension and not is_api


def get_random_meme_url(category: Optional[str] = None) -> dict:
    """
    获取随机表情包 URL，自动过滤掉可疑的 JSON API
    
    Args:
        category: 指定分类，None表示随机
        
    Returns:
        {
            "success": bool,
            "url": str | None,
            "category": str | None,
            "error": str | None
        }
    """
    try:
        if category is None:
            # 随机选择分类
            category = random.choice(categories)
        
        if category not in MEME_URLS:
            return {
                "success": False,
                "url": None,
                "category": None,
                "error": f"未知分类: {category}"
            }
        
        # 获取该分类的所有 URL
        urls = MEME_URLS[category]
        
        # 优先选择直接图片链接
        direct_urls = [url for url in urls if is_direct_image_url(url)]
        
        if direct_urls:
            url = random.choice(direct_urls)
        elif urls:
            # 如果没有直接图片链接，随机选一个（可能会返回 JSON）
            url = random.choice(urls)
        else:
            return {
                "success": False,
                "url": None,
                "category": None,
                "error": f"分类 {category} 没有可用的 URL"
            }
        
        return {
            "success": True,
            "url": url,
            "category": category,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "url": None,
            "category": None,
            "error": str(e)
        }


def get_meme_url_by_keyword(keyword: str) -> dict:
    """
    根据关键词获取表情包 URL
    
    Args:
        keyword: 用户输入的关键词
        
    Returns:
        同 get_random_meme_url 的返回值
    """
    keyword = keyword.lower().strip()
    
    # 查找匹配的类别
    category = KEYWORD_MAP.get(keyword)
    
    # 如果没找到，尝试检查是否是有效类别
    if category is None and keyword in categories:
        category = keyword
    
    if category:
        return get_random_meme_url(category)
    
    # 关键词未匹配，返回随机
    return get_random_meme_url()


def list_categories() -> list:
    """列出所有可用的表情包分类"""
    return categories


def get_all_urls(category: Optional[str] = None) -> list:
    """获取指定分类的所有 URL，或所有分类的所有 URL"""
    if category:
        return MEME_URLS.get(category, [])
    
    all_urls = []
    for urls in MEME_URLS.values():
        all_urls.extend(urls)
    return all_urls


# 便捷函数
get_url = get_random_meme_url
send_meme = get_random_meme_url


if __name__ == "__main__":
    # 测试
    import json
    
    print("测试获取随机表情包 URL:")
    result = get_random_meme_url()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n测试按关键词获取:")
    result = get_meme_url_by_keyword("猫娘")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n可用分类:")
    print(list_categories())
    
    print("\n测试 URL 检测:")
    test_urls = [
        "https://example.com/image.jpg",
        "https://nekos.life/api/v2/img/neko",
        "https://media.tenor.com/doro.gif",
        "https://api.waifu.im/search",
    ]
    for url in test_urls:
        print(f"  {url}: {'直接图片' if is_direct_image_url(url) else '可能是API'}")
