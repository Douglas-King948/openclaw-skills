#!/usr/bin/env python3
"""
Smart Meme v6.0 - 统一发送接口
自动检测平台，选择最佳发送方式，支持失败降级

使用示例：
    from smart_meme import send_meme
    
    # 最简单用法 - 自动检测关键词
    send_meme("来个马喽")
    
    # 指定分类
    send_meme(category="panda")
    
    # 指定目标和平台
    send_meme(message="来个猫咪", target="ou_xxx", channel="feishu")
"""

import sys
import os
import urllib.request
import tempfile
from pathlib import Path
from typing import Optional, Literal

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from url_sender import get_meme_url_by_keyword, get_random_meme_url
from url_sources import KEYWORD_MAP

# 导入新的飞书卡片发送器
try:
    from feishu_card_sender import send_feishu_card, upload_image
    FEISHU_CARD_AVAILABLE = True
except ImportError:
    FEISHU_CARD_AVAILABLE = False

# 平台检测
def detect_channel() -> str:
    """自动检测当前平台"""
    return os.environ.get('OPENCLAW_CHANNEL', 'feishu')


def download_image(url: str) -> str:
    """
    下载图片到临时文件
    
    Args:
        url: 图片 URL
        
    Returns:
        本地文件路径
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    
    # 生成临时文件路径
    ext = '.jpg'
    if '.' in url.split('/')[-1]:
        ext = '.' + url.split('/')[-1].split('.')[-1].split('?')[0]
        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            ext = '.jpg'
    
    temp_path = os.path.join(tempfile.gettempdir(), f'smart_meme_{id(url)}{ext}')
    
    with urllib.request.urlopen(request, timeout=15) as response:
        with open(temp_path, 'wb') as f:
            f.write(response.read())
    
    return temp_path


def parse_keyword(message: str) -> Optional[str]:
    """
    从消息中解析关键词
    
    Args:
        message: 用户消息
        
    Returns:
        分类名称或 None
    """
    message = message.lower()
    
    # 扩展关键词映射
    keyword_map = {
        # 马喽/猴子
        "猴子": "monkeys", "猴": "monkeys", "monkey": "monkeys", "monkeys": "monkeys",
        "马喽": "monkeys", "吗喽": "monkeys", "马猴": "monkeys", "猴哥": "monkeys",
        "马楼": "monkeys", "吗楼": "monkeys",
        "猩猩": "monkeys", "猿": "monkeys", "ape": "monkeys", "orangutan": "monkeys",
        
        # 熊猫头
        "熊猫头": "panda", "熊猫": "panda", "滚滚": "panda", "panda": "panda",
        "斗图": "panda", "梗图": "panda", "搞笑": "panda", "乐": "panda",
        
        # 猫咪
        "猫咪": "cats", "猫": "cats", "cat": "cats", "cats": "cats",
        "喵喵": "cats", "kitty": "cats", "哈基米": "cats",
        
        # 狗狗
        "狗狗": "dogs", "狗": "dogs", "dog": "dogs", "dogs": "dogs",
        "汪汪": "dogs", "puppy": "dogs",
        
        # 鸭子
        "鸭子": "ducks", "鸭": "ducks", "duck": "ducks", "ducks": "ducks",
        "嘎嘎": "ducks", "小鸭子": "ducks", "ducky": "ducks",
        
        # 动漫/二次元
        "动漫": "anime", "anime": "anime", "二次元": "anime", "动画": "anime",
        "猫娘": "anime", "萌": "anime", "少女": "anime", "美少女": "anime",
        "pixiv": "anime", "p站": "anime", "壁纸": "anime",
        
        # 程序员
        "程序员": "programmer", "programmer": "programmer", "码农": "programmer",
        "coding": "programmer", "code": "programmer",
        
        # 武侠
        "武侠": "wuxia", "wuxia": "wuxia", "功夫": "wuxia",
        
        # 动物
        "动物": "animals", "animals": "animals", "animal": "animals",
        
        # 东方
        "东方": "touhou", "东方project": "touhou", "touhou": "touhou", "车万": "touhou",
        
        # Doro
        "doro": "doro", "多洛": "doro", "nikke": "doro", "妮姬": "doro",
    }
    
    # 精确匹配
    if message in keyword_map:
        return keyword_map[message]
    
    # 包含匹配
    for keyword, category in keyword_map.items():
        if keyword in message:
            return category
    
    return None


def get_interactive_text(category: str) -> str:
    """获取分类对应的互动文案"""
    import random
    
    texts = {
        "monkeys": ["马喽驾到！🐵", "猴哥来了！", "这是你要的马喽～"],
        "panda": ["滚滚来了～🐼", "熊猫头驾到！", "搞笑熊猫头请收好～"],
        "cats": ["喵～🐱", "猫咪来了！", "治愈猫咪请查收～"],
        "dogs": ["汪汪～🐶", "狗狗来了！", "可爱狗狗请收好～"],
        "ducks": ["嘎嘎～🦆", "鸭子来了！", "小鸭子请收好～"],
        "anime": ["二次元来了！✨", "猫娘驾到～🐱", "美图请查收～"],
        "programmer": ["程序员梗图！💻", "同行都懂的表情包～", "代码之外的默契😄"],
        "wuxia": ["武侠风来了！⚔️", "江湖气息表情包～", "功夫熊猫请收好～"],
        "touhou": ["车万来了！🎵", "东方Project～", "符卡攻击！💫"],
        "doro": ["Doro来了！🌟", "多洛表情包～", "NIKKE梗图请收好～"],
        "animals": ["小动物来了！🐾", "萌宠表情包～", "治愈动物请查收～"],
    }
    
    return random.choice(texts.get(category, ["表情包来啦！", "请收好～", "这是你要的表情包～"]))


def send_meme(
    message: Optional[str] = None,
    category: Optional[str] = None,
    target: Optional[str] = None,
    channel: Optional[str] = None
) -> dict:
    """
    统一发送接口 - 智能选择最佳发送方式
    
    Args:
        message: 用户消息（自动解析关键词）
        category: 直接指定分类（优先级高于 message）
        target: 目标用户/群聊 ID（默认当前会话）
        channel: 平台类型（默认自动检测）
        
    Returns:
        {"success": bool, "message_id": str|None, "error": str|None, "url": str|None}
    """
    # 解析分类
    if category is None and message:
        category = parse_keyword(message)
    
    if category is None:
        category = "misc"
    
    # 获取表情包 URL
    if message and not parse_keyword(message):
        result = get_meme_url_by_keyword(message)
    else:
        result = get_random_meme_url(category)
    
    if not result["success"]:
        return {"success": False, "message_id": None, "error": result["error"], "url": None}
    
    url = result["url"]
    actual_category = result.get("category", category)
    
    # 自动检测平台和目标
    if channel is None:
        channel = detect_channel()
    
    if target is None:
        target = os.environ.get('OPENCLAW_TARGET', 'ou_f35e74b14ff44420bdd4ede905c3b587')
    
    # 获取互动文案
    interactive_text = get_interactive_text(actual_category)
    
    # 飞书平台 - 使用卡片消息
    if channel == "feishu":
        try:
            # 下载图片
            local_path = download_image(url)
            
            # 使用 Python 版飞书卡片发送器
            if FEISHU_CARD_AVAILABLE:
                title_map = {
                    "monkeys": "🐵 马喽驾到！",
                    "panda": "🐼 熊猫头驾到！",
                    "cats": "🐱 猫咪来了！",
                    "dogs": "🐶 狗狗来了！",
                    "ducks": "🦆 鸭子来了！",
                    "anime": "✨ 二次元来了！",
                    "programmer": "💻 程序员梗图！",
                    "wuxia": "⚔️ 武侠风来了！",
                    "touhou": "🎵 车万来了！",
                    "doro": "🌟 Doro来了！",
                    "animals": "🐾 小动物来了！",
                }
                title = title_map.get(actual_category, "🎨 表情包来啦！")
                
                result = send_feishu_card(
                    target=target,
                    image_path=local_path,
                    title=title,
                    text=interactive_text,
                    color="blue"
                )
                
                result["url"] = url
                return result
            else:
                # 回退：返回 URL 供外部处理
                return {
                    "success": True,
                    "message_id": None,
                    "error": None,
                    "url": url,
                    "category": actual_category,
                    "text": interactive_text,
                    "local_path": local_path
                }
            
        except Exception as e:
            return {"success": False, "message_id": None, "error": str(e), "url": url}
    
    # 其他平台
    else:
        return {
            "success": True,
            "message_id": None,
            "error": None,
            "url": url,
            "category": actual_category,
            "text": interactive_text
        }


# 便捷函数
def send_monkey(target: Optional[str] = None) -> dict:
    """发送马喽"""
    return send_meme(category="monkeys", target=target)

def send_panda(target: Optional[str] = None) -> dict:
    """发送熊猫头"""
    return send_meme(category="panda", target=target)

def send_cat(target: Optional[str] = None) -> dict:
    """发送猫咪"""
    return send_meme(category="cats", target=target)

def send_dog(target: Optional[str] = None) -> dict:
    """发送狗狗"""
    return send_meme(category="dogs", target=target)

def send_duck(target: Optional[str] = None) -> dict:
    """发送鸭子"""
    return send_meme(category="ducks", target=target)

def send_anime(target: Optional[str] = None) -> dict:
    """发送二次元"""
    return send_meme(category="anime", target=target)

def send_programmer(target: Optional[str] = None) -> dict:
    """发送程序员梗图"""
    return send_meme(category="programmer", target=target)


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        message = sys.argv[1]
        result = send_meme(message=message)
        print(f"Result: {result}")
    else:
        result = send_meme("来个马喽")
        print(f"Test result: {result}")


# 导入新的飞书卡片发送器
try:
    from feishu_card_sender import send_feishu_card, upload_image
    FEISHU_CARD_AVAILABLE = True
except ImportError:
    FEISHU_CARD_AVAILABLE = False

# 平台检测
def detect_channel() -> str:
    """自动检测当前平台"""
    return os.environ.get('OPENCLAW_CHANNEL', 'feishu')


def download_image(url: str) -> str:
    """
    下载图片到临时文件
    
    Args:
        url: 图片 URL
        
    Returns:
        本地文件路径
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    
    # 生成临时文件路径
    ext = '.jpg'
    if '.' in url.split('/')[-1]:
        ext = '.' + url.split('/')[-1].split('.')[-1].split('?')[0]
        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            ext = '.jpg'
    
    temp_path = os.path.join(tempfile.gettempdir(), f'smart_meme_{id(url)}{ext}')
    
    with urllib.request.urlopen(request, timeout=15) as response:
        with open(temp_path, 'wb') as f:
            f.write(response.read())
    
    return temp_path


def parse_keyword(message: str) -> Optional[str]:
    """
    从消息中解析关键词
    
    Args:
        message: 用户消息
        
    Returns:
        分类名称或 None
    """
    message = message.lower()
    
    # 扩展关键词映射
    keyword_map = {
        # 马喽/猴子
        "猴子": "monkeys", "猴": "monkeys", "monkey": "monkeys", "monkeys": "monkeys",
        "马喽": "monkeys", "吗喽": "monkeys", "马猴": "monkeys", "猴哥": "monkeys",
        "马楼": "monkeys", "吗楼": "monkeys",
        "猩猩": "monkeys", "猿": "monkeys", "ape": "monkeys", "orangutan": "monkeys",
        
        # 熊猫头
        "熊猫头": "panda", "熊猫": "panda", "滚滚": "panda", "panda": "panda",
        "斗图": "panda", "梗图": "panda", "搞笑": "panda", "乐": "panda",
        
        # 猫咪
        "猫咪": "cats", "猫": "cats", "cat": "cats", "cats": "cats",
        "喵喵": "cats", "kitty": "cats", "哈基米": "cats",
        
        # 狗狗
        "狗狗": "dogs", "狗": "dogs", "dog": "dogs", "dogs": "dogs",
        "汪汪": "dogs", "puppy": "dogs",
        
        # 鸭子
        "鸭子": "ducks", "鸭": "ducks", "duck": "ducks", "ducks": "ducks",
        "嘎嘎": "ducks", "小鸭子": "ducks", "ducky": "ducks",
        
        # 动漫/二次元
        "动漫": "anime", "anime": "anime", "二次元": "anime", "动画": "anime",
        "猫娘": "anime", "萌": "anime", "少女": "anime", "美少女": "anime",
        "pixiv": "anime", "p站": "anime", "壁纸": "anime",
        
        # 程序员
        "程序员": "programmer", "programmer": "programmer", "码农": "programmer",
        "coding": "programmer", "code": "programmer",
        
        # 武侠
        "武侠": "wuxia", "wuxia": "wuxia", "功夫": "wuxia",
        
        # 动物
        "动物": "animals", "animals": "animals", "animal": "animals",
        
        # 东方
        "东方": "touhou", "东方project": "touhou", "touhou": "touhou", "车万": "touhou",
        
        # Doro
        "doro": "doro", "多洛": "doro", "nikke": "doro", "妮姬": "doro",
    }
    
    # 精确匹配
    if message in keyword_map:
        return keyword_map[message]
    
    # 包含匹配
    for keyword, category in keyword_map.items():
        if keyword in message:
            return category
    
    return None


def get_interactive_text(category: str) -> str:
    """获取分类对应的互动文案"""
    import random
    
    texts = {
        "monkeys": ["马喽驾到！🐵", "猴哥来了！", "这是你要的马喽～"],
        "panda": ["滚滚来了～🐼", "熊猫头驾到！", "搞笑熊猫头请收好～"],
        "cats": ["喵～🐱", "猫咪来了！", "治愈猫咪请查收～"],
        "dogs": ["汪汪～🐶", "狗狗来了！", "可爱狗狗请收好～"],
        "ducks": ["嘎嘎～🦆", "鸭子来了！", "小鸭子请收好～"],
        "anime": ["二次元来了！✨", "猫娘驾到～🐱", "美图请查收～"],
        "programmer": ["程序员梗图！💻", "同行都懂的表情包～", "代码之外的默契😄"],
        "wuxia": ["武侠风来了！⚔️", "江湖气息表情包～", "功夫熊猫请收好～"],
        "touhou": ["车万来了！🎵", "东方Project～", "符卡攻击！💫"],
        "doro": ["Doro来了！🌟", "多洛表情包～", "NIKKE梗图请收好～"],
        "animals": ["小动物来了！🐾", "萌宠表情包～", "治愈动物请查收～"],
    }
    
    return random.choice(texts.get(category, ["表情包来啦！", "请收好～", "这是你要的表情包～"]))


def send_meme(
    message: Optional[str] = None,
    category: Optional[str] = None,
    target: Optional[str] = None,
    channel: Optional[str] = None
) -> dict:
    """
    统一发送接口 - 智能选择最佳发送方式
    
    Args:
        message: 用户消息（自动解析关键词）
        category: 直接指定分类（优先级高于 message）
        target: 目标用户/群聊 ID（默认当前会话）
        channel: 平台类型（默认自动检测）
        
    Returns:
        {"success": bool, "message_id": str|None, "error": str|None, "url": str|None}
    """
    # 解析分类
    if category is None and message:
        category = parse_keyword(message)
    
    if category is None:
        category = "misc"
    
    # 获取表情包 URL
    if message and not parse_keyword(message):
        result = get_meme_url_by_keyword(message)
    else:
        result = get_random_meme_url(category)
    
    if not result["success"]:
        return {"success": False, "message_id": None, "error": result["error"], "url": None}
    
    url = result["url"]
    actual_category = result.get("category", category)
    
    # 自动检测平台和目标
    if channel is None:
        channel = detect_channel()
    
    if target is None:
        target = os.environ.get('OPENCLAW_TARGET', 'ou_f35e74b14ff44420bdd4ede905c3b587')
    
    # 获取互动文案
    interactive_text = get_interactive_text(actual_category)
    
    # 飞书平台 - 使用卡片消息
    if channel == "feishu":
        try:
            # 下载图片
            local_path = download_image(url)
            
            # 使用 Python 版飞书卡片发送器
            if FEISHU_CARD_AVAILABLE:
                title_map = {
                    "monkeys": "🐵 马喽驾到！",
                    "panda": "🐼 熊猫头驾到！",
                    "cats": "🐱 猫咪来了！",
                    "dogs": "🐶 狗狗来了！",
                    "ducks": "🦆 鸭子来了！",
                    "anime": "✨ 二次元来了！",
                    "programmer": "💻 程序员梗图！",
                    "wuxia": "⚔️ 武侠风来了！",
                    "touhou": "🎵 车万来了！",
                    "doro": "🌟 Doro来了！",
                    "animals": "🐾 小动物来了！",
                }
                title = title_map.get(actual_category, "🎨 表情包来啦！")
                
                result = send_feishu_card(
                    target=target,
                    image_path=local_path,
                    title=title,
                    text=interactive_text,
                    color="blue"
                )
                
                result["url"] = url
                return result
            else:
                # 回退：返回 URL 供外部处理
                return {
                    "success": True,
                    "message_id": None,
                    "error": None,
                    "url": url,
                    "category": actual_category,
                    "text": interactive_text,
                    "local_path": local_path
                }
            
        except Exception as e:
            return {"success": False, "message_id": None, "error": str(e), "url": url}
    
    # 其他平台
    else:
        return {
            "success": True,
            "message_id": None,
            "error": None,
            "url": url,
            "category": actual_category,
            "text": interactive_text
        }


# 便捷函数
def send_monkey(target: Optional[str] = None) -> dict:
    """发送马喽"""
    return send_meme(category="monkeys", target=target)

def send_panda(target: Optional[str] = None) -> dict:
    """发送熊猫头"""
    return send_meme(category="panda", target=target)

def send_cat(target: Optional[str] = None) -> dict:
    """发送猫咪"""
    return send_meme(category="cats", target=target)

def send_dog(target: Optional[str] = None) -> dict:
    """发送狗狗"""
    return send_meme(category="dogs", target=target)

def send_duck(target: Optional[str] = None) -> dict:
    """发送鸭子"""
    return send_meme(category="ducks", target=target)

def send_anime(target: Optional[str] = None) -> dict:
    """发送二次元"""
    return send_meme(category="anime", target=target)

def send_programmer(target: Optional[str] = None) -> dict:
    """发送程序员梗图"""
    return send_meme(category="programmer", target=target)


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        message = sys.argv[1]
        result = send_meme(message=message)
        print(f"Result: {result}")
    else:
        result = send_meme("来个马喽")
        print(f"Test result: {result}")


# 平台检测
def detect_channel() -> str:
    """自动检测当前平台"""
    # 通过环境变量或调用上下文检测
    # 默认返回 feishu（当前主要使用平台）
    return os.environ.get('OPENCLAW_CHANNEL', 'feishu')


def download_image(url: str) -> str:
    """
    下载图片到临时文件
    
    Args:
        url: 图片 URL
        
    Returns:
        本地文件路径
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    
    # 生成临时文件路径
    ext = '.jpg'
    if '.' in url.split('/')[-1]:
        ext = '.' + url.split('/')[-1].split('.')[-1].split('?')[0]
        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            ext = '.jpg'
    
    temp_path = os.path.join(tempfile.gettempdir(), f'smart_meme_{id(url)}{ext}')
    
    with urllib.request.urlopen(request, timeout=15) as response:
        with open(temp_path, 'wb') as f:
            f.write(response.read())
    
    return temp_path


def send_meme_feishu_card(
    target: str,
    image_path: str,
    title: str = "表情包来啦！",
    text: str = "",
    color: str = "blue"
) -> dict:
    """
    使用飞书卡片发送图片
    
    Args:
        target: 目标用户或群聊 ID
        image_path: 本地图片路径
        title: 卡片标题
        text: 卡片正文
        color: 标题颜色
        
    Returns:
        {"success": bool, "message_id": str|None, "error": str|None}
    """
    import subprocess
    import json
    
    feishu_card_script = Path(__file__).parent.parent / "feishu-card" / "send.js"
    
    cmd = [
        "node", str(feishu_card_script),
        "--target", target,
        "--image-path", image_path,
        "--title", title,
        "--color", color
    ]
    
    if text:
        # 写入临时文件避免编码问题
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(text)
            temp_text_file = f.name
        cmd.extend(["--text-file", temp_text_file])
    else:
        temp_text_file = None
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=30)
        
        # 清理临时文件
        if temp_text_file:
            try:
                os.unlink(temp_text_file)
            except:
                pass
        
        if result.returncode != 0:
            return {"success": False, "message_id": None, "error": result.stderr}
        
        # 解析返回结果
        for line in result.stdout.split('\n'):
            if '"message_id"' in line:
                try:
                    start = line.find('{')
                    end = line.rfind('}') + 1
                    if start != -1 and end > start:
                        data = json.loads(line[start:end])
                        return {
                            "success": True,
                            "message_id": data.get("message_id"),
                            "error": None
                        }
                except:
                    pass
        
        return {"success": True, "message_id": None, "error": None}
        
    except Exception as e:
        if temp_text_file:
            try:
                os.unlink(temp_text_file)
            except:
                pass
        return {"success": False, "message_id": None, "error": str(e)}


def parse_keyword(message: str) -> Optional[str]:
    """
    从消息中解析关键词
    
    Args:
        message: 用户消息
        
    Returns:
        分类名称或 None
    """
    message = message.lower()
    
    # 关键词映射（扩展版）
    keyword_map = {
        # 马喽/猴子
        "马喽": "monkeys", "吗喽": "monkeys", "猴子": "monkeys", "猴": "monkeys",
        "monkey": "monkeys", "猴哥": "monkeys", "猩猩": "monkeys", "猿": "monkeys",
        "ape": "monkeys", "orangutan": "monkeys",
        
        # 熊猫头
        "熊猫头": "panda", "熊猫": "panda", "滚滚": "panda", "panda": "panda",
        "斗图": "panda", "梗图": "panda", "搞笑": "panda", "乐": "panda",
        
        # 猫咪
        "猫咪": "cats", "猫": "cats", "cat": "cats", "cats": "cats",
        "喵喵": "cats", "kitty": "cats", "哈基米": "cats",
        
        # 狗狗
        "狗狗": "dogs", "狗": "dogs", "dog": "dogs", "dogs": "dogs",
        "汪汪": "dogs", "puppy": "dogs",
        
        # 动漫/二次元
        "动漫": "anime", "anime": "anime", "二次元": "anime", "动画": "anime",
        "猫娘": "anime", "萌": "anime", "少女": "anime", "美少女": "anime",
        "pixiv": "anime", "p站": "anime", "壁纸": "anime",
        
        # 程序员
        "程序员": "programmer", "programmer": "programmer", "码农": "programmer",
        "coding": "programmer", "code": "programmer", "梗图": "programmer",
        
        # 武侠
        "武侠": "wuxia", "wuxia": "wuxia", "功夫": "wuxia",
        
        # 动物
        "动物": "animals", "animals": "animals", "animal": "animals",
        
        # 东方
        "东方": "touhou", "东方project": "touhou", "touhou": "touhou", "车万": "touhou",
        
        # Doro
        "doro": "doro", "多洛": "doro", "nikke": "doro", "妮姬": "doro",
    }
    
    # 精确匹配
    if message in keyword_map:
        return keyword_map[message]
    
    # 包含匹配
    for keyword, category in keyword_map.items():
        if keyword in message:
            return category
    
    return None


def get_interactive_text(category: str) -> str:
    """获取分类对应的互动文案"""
    import random
    
    texts = {
        "monkeys": ["马喽驾到！🐵", "猴哥来了！", "这是你要的马喽～"],
        "panda": ["滚滚来了～🐼", "熊猫头驾到！", "搞笑熊猫头请收好～"],
        "cats": ["喵～🐱", "猫咪来了！", "治愈猫咪请查收～"],
        "dogs": ["汪汪～🐶", "狗狗来了！", "可爱狗狗请收好～"],
        "anime": ["二次元来了！✨", "猫娘驾到～🐱", "美图请查收～"],
        "programmer": ["程序员梗图！💻", "同行都懂的表情包～", "代码之外的默契😄"],
        "wuxia": ["武侠风来了！⚔️", "江湖气息表情包～", "功夫熊猫请收好～"],
        "touhou": ["车万来了！🎵", "东方Project～", "符卡攻击！💫"],
        "doro": ["Doro来了！🌟", "多洛表情包～", "NIKKE梗图请收好～"],
        "animals": ["小动物来了！🐾", "萌宠表情包～", "治愈动物请查收～"],
    }
    
    return random.choice(texts.get(category, ["表情包来啦！", "请收好～", "这是你要的表情包～"]))


def send_meme(
    message: Optional[str] = None,
    category: Optional[str] = None,
    target: Optional[str] = None,
    channel: Optional[str] = None
) -> dict:
    """
    统一发送接口 - 智能选择最佳发送方式
    
    Args:
        message: 用户消息（自动解析关键词）
        category: 直接指定分类（优先级高于 message）
        target: 目标用户/群聊 ID（默认当前会话）
        channel: 平台类型（默认自动检测）
        
    Returns:
        {"success": bool, "message_id": str|None, "error": str|None, "url": str|None}
    """
    # 解析分类
    if category is None and message:
        category = parse_keyword(message)
    
    if category is None:
        category = "misc"  # 默认分类
    
    # 获取表情包 URL
    if message and not parse_keyword(message):
        # 如果有消息但没解析到关键词，尝试用关键词搜索
        result = get_meme_url_by_keyword(message)
    else:
        result = get_random_meme_url(category)
    
    if not result["success"]:
        return {"success": False, "message_id": None, "error": result["error"], "url": None}
    
    url = result["url"]
    actual_category = result.get("category", category)
    
    # 自动检测平台和目标
    if channel is None:
        channel = detect_channel()
    
    if target is None:
        # 从环境变量或上下文获取
        target = os.environ.get('OPENCLAW_TARGET', 'ou_f35e74b14ff44420bdd4ede905c3b587')
    
    # 获取互动文案
    interactive_text = get_interactive_text(actual_category)
    
    # 飞书平台 - 使用卡片消息（最可靠）
    if channel == "feishu":
        try:
            # 下载图片
            local_path = download_image(url)
            
            # 发送卡片
            title_map = {
                "monkeys": "🐵 马喽驾到！",
                "panda": "🐼 熊猫头驾到！",
                "cats": "🐱 猫咪来了！",
                "dogs": "🐶 狗狗来了！",
                "anime": "✨ 二次元来了！",
                "programmer": "💻 程序员梗图！",
                "wuxia": "⚔️ 武侠风来了！",
                "touhou": "🎵 车万来了！",
                "doro": "🌟 Doro来了！",
                "animals": "🐾 小动物来了！",
            }
            title = title_map.get(actual_category, "🎨 表情包来啦！")
            
            result = send_meme_feishu_card(
                target=target,
                image_path=local_path,
                title=title,
                text=interactive_text,
                color="blue"
            )
            
            result["url"] = url
            return result
            
        except Exception as e:
            return {"success": False, "message_id": None, "error": str(e), "url": url}
    
    # 其他平台 - 返回 URL 由调用者处理
    else:
        return {
            "success": True,
            "message_id": None,
            "error": None,
            "url": url,
            "category": actual_category,
            "text": interactive_text
        }


# 便捷函数
def send_monkey(target: Optional[str] = None) -> dict:
    """发送马喽"""
    return send_meme(category="monkeys", target=target)

def send_panda(target: Optional[str] = None) -> dict:
    """发送熊猫头"""
    return send_meme(category="panda", target=target)

def send_cat(target: Optional[str] = None) -> dict:
    """发送猫咪"""
    return send_meme(category="cats", target=target)

def send_dog(target: Optional[str] = None) -> dict:
    """发送狗狗"""
    return send_meme(category="dogs", target=target)

def send_anime(target: Optional[str] = None) -> dict:
    """发送二次元"""
    return send_meme(category="anime", target=target)

def send_programmer(target: Optional[str] = None) -> dict:
    """发送程序员梗图"""
    return send_meme(category="programmer", target=target)


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        message = sys.argv[1]
        result = send_meme(message=message)
        print(f"Result: {result}")
    else:
        # 默认测试
        result = send_meme("来个马喽")
        print(f"Test result: {result}")
