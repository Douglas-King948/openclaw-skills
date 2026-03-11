#!/usr/bin/env python3
"""
Smart Meme v3 - 主入口
安全、受控、可自治
"""

import sys
from pathlib import Path

# 确保可以导入本地模块
sys.path.insert(0, str(Path(__file__).parent))

from core.download import download_all, download_category
from core.selector import random_meme, get_stats
from evolve.health import check
from evolve.heal import heal
import config


def print_help():
    """打印帮助信息"""
    print("""
Smart Meme v3 - 安全可控的表情包系统

用法:
  python main.py download          下载所有表情包
  python main.py download [分类]   下载指定分类
  python main.py random            随机获取一个表情包
  python main.py random [分类]     从指定分类随机获取
  python main.py stats             显示统计信息
  python main.py check             健康检查
  python main.py heal              执行自愈（需开启auto_restock）
  python main.py heal --dry-run    预演自愈（不实际执行）
  python main.py config            显示配置信息

配置:
  编辑 config.py 中的 FEATURES 来开启/关闭功能

当前配置:
  auto_restock: {auto_restock}
  health_check: {health_check}
  dedup: {dedup}
  max_storage: {max_storage}MB

安全特性:
  - 熔断机制：连续失败3次后冷却5分钟
  - 存储上限：{max_storage}MB
  - SHA256分块计算：防内存爆炸
  - JSON存储：无并发锁定问题
""".format(
        auto_restock=config.FEATURES["auto_restock"],
        health_check=config.FEATURES["health_check"],
        dedup=config.FEATURES["dedup"],
        max_storage=config.MAX_STORAGE_MB
    ))


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "download":
        if len(sys.argv) > 2:
            cat = sys.argv[2]
            success, skip = download_category(cat)
            print(f"\n结果: 成功{success}, 跳过{skip}")
        else:
            results = download_all()
            print("\n汇总:")
            for cat, (success, skip) in results.items():
                print(f"  {cat}: 成功{success}, 跳过{skip}")
    
    elif command == "random":
        cat = sys.argv[2] if len(sys.argv) > 2 else None
        meme = random_meme(cat)
        if meme:
            print(f"\n随机表情包:")
            print(f"  ID: {meme['id']}")
            print(f"  分类: {meme['category']}")
            print(f"  路径: {meme['path']}")
        else:
            print("\n没有可用的表情包")
            print(f"提示: 运行 'python main.py download' 下载")
    
    elif command == "stats":
        stats = get_stats()
        print("\n统计信息:")
        print(f"  总数: {stats['total_count']}")
        print(f"  总大小: {stats['total_size_mb']}MB")
        print("  分类:")
        for cat, count in stats['categories'].items():
            print(f"    {cat}: {count}")
    
    elif command == "check":
        result = check()
        print("\n健康检查:")
        print(f"  健康状态: {'正常' if result['healthy'] else '异常'}")
        if result['issues']:
            print("  问题:")
            for issue in result['issues']:
                print(f"    [{issue['level']}] {issue['message']}")
        if result['recommendations']:
            print("  建议:")
            for rec in result['recommendations']:
                print(f"    - {rec}")
    
    elif command == "heal":
        dry_run = "--dry-run" in sys.argv
        result = heal(dry_run=dry_run)
        
        if dry_run:
            print("\n[预演模式 - 不实际执行]")
        
        print("\n自愈结果:")
        for action in result['actions']:
            print(f"  {action['type']}: {action.get('status', '')}")
        
        if result.get('health_check'):
            print(f"\n健康检查: {'正常' if result['health_check']['healthy'] else '异常'}")
    
    elif command == "config":
        print("\n配置信息:")
        print(f"  存储目录: {config.MEME_DIR}")
        print(f"  数据库: {config.DB_FILE}")
        print(f"  最大存储: {config.MAX_STORAGE_MB}MB")
        print(f"  最大重试: {config.MAX_RETRY}")
        print(f"  冷却时间: {config.COOLDOWN_SECONDS}秒")
        print("\n功能开关:")
        for name, value in config.FEATURES.items():
            print(f"  {name}: {'开启' if value else '关闭'}")
    
    else:
        print(f"未知命令: {command}")
        print_help()


if __name__ == "__main__":
    main()
