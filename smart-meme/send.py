#!/usr/bin/env python3
"""
Smart Meme - 快捷发送工具
直接通过命令行发送表情包
"""

import sys
import json
from pathlib import Path

# 添加技能目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from sender import send_random_meme, get_meme_by_keyword, list_categories, check_stock


def main():
    if len(sys.argv) < 2:
        print("""
Smart Meme - 表情包发送工具

用法:
  python send.py random              # 发送随机表情包
  python send.py random [分类]       # 发送指定分类的表情包
  python send.py keyword [关键词]    # 根据关键词发送
  python send.py stock               # 查看库存
  python send.py list                # 列出所有分类

示例:
  python send.py random              # 随机
  python send.py random panda        # 熊猫头
  python send.py keyword 熊猫头      # 关键词匹配
  python send.py keyword 猫咪        # 关键词匹配

分类列表:
  panda, cats, dogs, anime, wuxia, animals, programmer, misc
""")
        return
    
    command = sys.argv[1].lower()
    
    if command == "random":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        result = send_random_meme(category)
        
        if result["success"]:
            print(f"SUCCESS:{result['file_path']}")
            print(f"CATEGORY:{result['category']}")
        else:
            print(f"ERROR:{result['error']}")
            sys.exit(1)
    
    elif command == "keyword":
        if len(sys.argv) < 3:
            print("ERROR:请提供关键词")
            sys.exit(1)
        
        keyword = sys.argv[2]
        result = get_meme_by_keyword(keyword)
        
        if result["success"]:
            print(f"SUCCESS:{result['file_path']}")
            print(f"CATEGORY:{result['category']}")
        else:
            print(f"ERROR:{result['error']}")
            sys.exit(1)
    
    elif command == "stock":
        stock = check_stock()
        print(json.dumps(stock, indent=2, ensure_ascii=False))
    
    elif command == "list":
        categories = list_categories()
        print("可用的表情包分类:")
        for cat in categories:
            print(f"  - {cat}")
    
    else:
        print(f"未知命令: {command}")
        print("运行 'python send.py' 查看帮助")
        sys.exit(1)


if __name__ == "__main__":
    main()
