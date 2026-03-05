#!/usr/bin/env python3
"""
Smart Meme - 使用示例
展示如何直接发送表情包
"""

import sys
from pathlib import Path

# 添加技能目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from sender import send_random_meme, get_meme_by_keyword


def demo_send_meme():
    """
    演示：发送表情包
    
    返回格式:
    {
        "success": True/False,
        "file_path": "/path/to/meme.jpg",  # 图片文件路径
        "category": "panda",                # 分类
        "error": None                       # 错误信息（如果有）
    }
    """
    
    # 示例 1: 发送随机表情包
    print("=" * 50)
    print("示例 1: 发送随机表情包")
    print("=" * 50)
    
    result = send_random_meme()
    
    if result["success"]:
        print(f"✅ 成功!")
        print(f"   文件路径: {result['file_path']}")
        print(f"   分类: {result['category']}")
        print()
        print(f"   使用方式:")
        print(f'   message(action="send", media="{result["file_path"]}")')
    else:
        print(f"❌ 失败: {result['error']}")
        print()
        print("提示: 需要先下载表情包库存")
        print("运行: python run.bat download")
    
    print()
    
    # 示例 2: 发送熊猫头表情包
    print("=" * 50)
    print("示例 2: 发送熊猫头表情包")
    print("=" * 50)
    
    result = get_meme_by_keyword("熊猫头")
    
    if result["success"]:
        print(f"✅ 成功!")
        print(f"   文件路径: {result['file_path']}")
        print(f"   分类: {result['category']}")
    else:
        print(f"❌ 失败: {result['error']}")
    
    print()
    
    # 示例 3: 发送猫咪表情包
    print("=" * 50)
    print("示例 3: 发送猫咪表情包")
    print("=" * 50)
    
    result = get_meme_by_keyword("猫咪")
    
    if result["success"]:
        print(f"✅ 成功!")
        print(f"   文件路径: {result['file_path']}")
        print(f"   分类: {result['category']}")
    else:
        print(f"❌ 失败: {result['error']}")


def demo_check_stock():
    """演示：检查库存"""
    from sender import check_stock
    
    print()
    print("=" * 50)
    print("库存检查")
    print("=" * 50)
    
    stock = check_stock()
    print(f"总库存: {stock['total']} 个表情包")
    print()
    print("分类统计:")
    for cat, count in stock['categories'].items():
        status = "✅" if count > 0 else "❌"
        print(f"   {status} {cat}: {count} 个")
    
    if stock['empty_categories']:
        print()
        print("空库存分类:")
        for cat in stock['empty_categories']:
            print(f"   - {cat}")


if __name__ == "__main__":
    demo_send_meme()
    demo_check_stock()
