#!/usr/bin/env python3
"""
每日工作日报 - 自动发送
每天早上8点自动读取昨日工作记录，生成并发送日报卡片
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加技能路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def get_yesterday_memory():
    """获取昨天的记忆文件内容"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    memory_file = Path(f"D:/openclaw/memory/{yesterday}.md")
    
    if not memory_file.exists():
        print(f"[WARN] 昨天({yesterday})的记忆文件不存在")
        return None, yesterday
    
    with open(memory_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    return content, yesterday

def extract_work_items(content):
    """从记忆内容中提取工作事项"""
    items = []
    
    # 匹配 ✅ 完成的事项
    completed_pattern = r'^\s*[-*]\s*✅\s*(.+)$'
    for match in re.finditer(completed_pattern, content, re.MULTILINE):
        item = match.group(1).strip()
        # 限制长度
        if len(item) > 50:
            item = item[:47] + "..."
        items.append(item)
    
    # 如果没有✅，尝试匹配其他格式
    if not items:
        # 匹配 "完成"、"修复"、"创建" 等关键词开头的行
        work_pattern = r'^\s*[-*]\s*(完成|修复|创建|设置|优化|实现|发布|部署|更新|添加)\s*(.+)$'
        for match in re.finditer(work_pattern, content, re.MULTILINE):
            action = match.group(1)
            desc = match.group(2).strip()
            item = f"{action}{desc}"
            if len(item) > 50:
                item = item[:47] + "..."
            items.append(item)
    
    # 提取待办事项
    todo_items = []
    todo_pattern = r'^\s*[-*]\s*\[\s*\]\s*(.+)$'
    for match in re.finditer(todo_pattern, content, re.MULTILINE):
        todo = match.group(1).strip()
        if len(todo) > 50:
            todo = todo[:47] + "..."
        todo_items.append(f"待完成: {todo}")
    
    # 合并已完成和待办
    all_items = items + todo_items
    
    # 如果没有提取到任何内容，使用默认提示
    if not all_items:
        all_items = ["昨日工作记录已生成", "详细内容请查看记忆文件"]
    
    # 最多显示8条
    return all_items[:8]

def send_daily_work_report():
    """发送每日工作日报"""
    from sender import send_daily_report
    
    # 获取昨天的工作记录
    content, yesterday = get_yesterday_memory()
    
    if content is None:
        # 如果没有记忆文件，发送简化版日报
        items = ["昨日工作记录未找到", f"日期: {yesterday}"]
    else:
        # 提取工作事项
        items = extract_work_items(content)
    
    # 发送日报
    today_str = datetime.now().strftime("%m/%d")
    title = f"📋 {yesterday} 工作日报"
    
    result = send_daily_report(
        title=title,
        items=items,
        mood="working",
        color="blue"
    )
    
    return result

def main():
    print("="*60)
    print("每日工作日报自动发送")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()
    
    try:
        result = send_daily_work_report()
        print()
        print("发送结果:", json.dumps(result, ensure_ascii=False, indent=2))
        
        if result.get("success"):
            print("\n[OK] 日报发送成功!")
            return 0
        else:
            print(f"\n[ERROR] 发送失败: {result.get('error')}")
            return 1
    except Exception as e:
        print(f"\n[ERROR] 异常: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
