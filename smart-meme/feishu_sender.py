#!/usr/bin/env python3
"""
Smart Meme - 飞书卡片消息发送模块
专门针对飞书频道优化的表情包发送方式
"""

import sys
import subprocess
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# 确保可以导入本地模块
sys.path.insert(0, str(Path(__file__).parent))

from url_sender import get_meme_url_by_keyword as get_url_by_keyword
from sender import send_random_meme, get_meme_by_keyword

# Feishu Card 脚本路径
FEISHU_CARD_SCRIPT = Path(__file__).parent.parent.parent / "skills" / "feishu-card" / "send.js"

# 工作时段安全分类（工作日 8:30-17:30 可用）
WORK_SAFE_CATEGORIES = ["panda", "cats", "dogs", "animals", "programmer"]

# 非工作时段可用分类（全天可用）
ALL_CATEGORIES = ["panda", "cats", "dogs", "animals", "programmer", "anime", "wuxia", "misc"]

# 分类安全等级说明
CATEGORY_SAFETY = {
    "panda": {"safe": True, "reason": "搞笑沙雕，职场安全"},
    "cats": {"safe": True, "reason": "治愈萌宠， universally loved"},
    "dogs": {"safe": True, "reason": "治愈萌宠， universally loved"},
    "animals": {"safe": True, "reason": "可爱动物，职场安全"},
    "programmer": {"safe": True, "reason": "工作相关，甚至加分"},
    "anime": {"safe": False, "reason": "二次元浓度高，可能社死"},
    "wuxia": {"safe": False, "reason": "中二气息，不够专业"},
    "misc": {"safe": False, "reason": "内容不可控，风险未知"},
}


def is_work_hours() -> bool:
    """
    判断当前是否在工作时间
    工作时间：工作日（周一到周五）8:30 - 17:30
    
    Returns:
        True 表示在工作时间
    """
    from datetime import datetime
    
    now = datetime.now()
    weekday = now.weekday()  # 0=周一, 6=周日
    hour = now.hour
    minute = now.minute
    current_time = hour * 60 + minute  # 转换为分钟
    
    # 周末不算工作时间
    if weekday >= 5:  # 周六(5) 或 周日(6)
        return False
    
    # 工作时间：8:30 - 17:30
    work_start = 8 * 60 + 30   # 510
    work_end = 17 * 60 + 30    # 1050
    
    return work_start <= current_time <= work_end


def get_safe_categories() -> list:
    """
    获取当前时段安全的分类列表
    
    Returns:
        安全的分类列表
    """
    if is_work_hours():
        return WORK_SAFE_CATEGORIES
    return ALL_CATEGORIES


def is_category_safe(category: str) -> bool:
    """
    检查指定分类在当前时段是否安全
    
    Args:
        category: 分类名称
        
    Returns:
        True 表示安全可用
    """
    if not is_work_hours():
        return True  # 非工作时间全部可用
    
    return category in WORK_SAFE_CATEGORIES


def get_safety_warning(category: str) -> str:
    """
    获取分类安全警告信息（用于调试/提示）
    
    Args:
        category: 分类名称
        
    Returns:
        安全状态说明
    """
    if is_category_safe(category):
        return f"✅ {category} 当前可用"
    else:
        reason = CATEGORY_SAFETY.get(category, {}).get("reason", "可能社死")
        return f"⏸️ {category} 工作时间禁用：{reason}"


# 分类互动文案 - 符合猫娘人设，增加互动感
INTERACTIVE_MESSAGES = {
    "panda": [
        "从库存里翻到的熊猫头～ (=^-ω-^=)",
        "这表情绝了哈哈哈！ヽ(★ω★)ノ",
        "熊猫头永不缺席！⌐■_■",
        "来自滚滚的凝视 👀",
        "这个够沙雕，我喜欢！ᕕ( ᐛ )ᕗ",
    ],
    "cats": [
        "喵～和我一样可爱吧？❄️🐱",
        "猫咪即正义！(=◕ ◡◕=)",
        "吸猫时间到～ (=^-ω-^=)",
        "这只好萌，想rua！✨",
        "猫奴福利来啦～ 🐾",
    ],
    "dogs": [
        "汪汪！忠诚的狗狗最棒啦～ 🐕",
        "治愈系狗狗来袭！(ﾉ◕ヮ◕)ﾉ",
        "今天也要开心哦～ 🐶✨",
        " doggo power！੭ ˙ᗜ˙ )੭",
        "这眼神，我爱了～ ❤️",
    ],
    "animals": [
        "小动物治愈时间到～ 🌸",
        "这也太可爱了吧！❤️",
        "心都要化了～ (◕‿◕✿)",
        "大自然的馈赠！🌿",
        "萌度爆表！(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
    ],
    "programmer": [
        "又有bug要修？别急，先笑笑～ 😂",
        "代码写完了吗就来摸鱼！⌐■_■",
        "程序员的日常，懂的都懂... 💻",
        "Ctrl+C, Ctrl+V 大法好！🖱️",
        "这梗太真实了哈哈哈！🤣",
    ],
    "anime": [
        "二次元能量注入！✨(ง'̀-'́)ง",
        "番剧追完了吗？来张图继续肝！",
        "萌即是正义！ヽ(★ω★)ノ",
        "这张好康！收藏了～ 📸",
        "动漫赛高！٩(◕‿◕)۶",
    ],
    "wuxia": [
        "江湖风云再起！⚔️ (•̀ᴗ•́)و",
        "大侠，请收图！🗡️",
        "武功盖世，表情包也要帅！",
        "仗剑走天涯，斗图不能输！",
        "此图只应天上有～ 🏔️",
    ],
    "misc": [
        "翻到了个有趣的～ ᕕ( ᐛ )ᕗ",
        "这个梗我收了！😂",
        "今日份快乐送达！📦✨",
        "莫名觉得好适合现在发！",
        "嘿嘿，惊喜吧～ (=^-ω-^=)",
    ],
}

# 工作时间专用互动文案 - 更专业、更克制
WORK_INTERACTIVE_MESSAGES = {
    "panda": [
        "工作间隙，放松一下～",
        "适当摸鱼，效率更高 😉",
        "来张表情包换换心情",
        "熊猫头，职场通用 🤝",
    ],
    "cats": [
        "猫咪治愈，缓解压力 🐱",
        "工作中也需要一点萌～",
        "看看小猫咪，继续加油！",
        "宠物疗法，科学有效 ✨",
    ],
    "dogs": [
        "狗狗给你带来正能量 🐕",
        "工作中的小确幸～",
        "看看狗狗，心情变好",
        "忠诚的伙伴，一直陪着你 💪",
    ],
    "animals": [
        "大自然的力量，放松一下 🌿",
        "看看小动物，调节状态",
        "萌物治愈，继续战斗！",
        "工作中的绿色小憩 🍃",
    ],
    "programmer": [
        "同行都懂的表情包 💻",
        "程序员的默契，你懂的",
        "工作中的一点幽默 😄",
        "代码之外的共同语言",
    ],
}


def generate_interactive_message(category: str) -> str:
    """
    生成分类对应的互动文案
    工作时间使用更专业的文案，非工作时间使用活泼文案
    
    Args:
        category: 表情包分类
        
    Returns:
        互动文案
    """
    import random
    
    if is_work_hours() and category in WORK_INTERACTIVE_MESSAGES:
        # 工作时间使用专业文案
        messages = WORK_INTERACTIVE_MESSAGES[category]
    else:
        # 非工作时间使用活泼文案
        messages = INTERACTIVE_MESSAGES.get(category, INTERACTIVE_MESSAGES["misc"])
    
    return random.choice(messages)


def download_image(url: str, temp_dir: Optional[Path] = None) -> Path:
    """
    下载图片到本地临时文件
    
    Args:
        url: 图片URL
        temp_dir: 临时目录，默认使用系统临时目录
        
    Returns:
        下载后的本地文件路径
    """
    if temp_dir is None:
        temp_dir = Path(tempfile.gettempdir())
    
    # 从URL提取文件名或使用随机名
    url_path = Path(url.split('?')[0])  # 移除查询参数
    ext = url_path.suffix or '.jpg'
    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
        ext = '.jpg'
    
    temp_file = temp_dir / f"feishu_meme_{id(url)}{ext}"
    
    # 下载图片
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
    }
    
    request = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            with open(temp_file, 'wb') as f:
                f.write(response.read())
        return temp_file
    except Exception as e:
        raise Exception(f"下载图片失败: {e}")


def send_feishu_card(
    target: str,
    image_path: str,
    title: str,
    text: Optional[str] = None,
    color: str = "blue"
) -> dict:
    """
    使用 feishu-card 发送卡片消息
    
    Args:
        target: 目标用户或群聊ID (ou_xxx 或 oc_xxx)
        image_path: 本地图片路径
        title: 卡片标题（作为主消息内容）
        text: 卡片正文（互动文案）
        color: 标题颜色
        
    Returns:
        {
            "success": bool,
            "message_id": str | None,
            "error": str | None
        }
    """
    temp_text_file = None
    
    try:
        # 构建命令
        cmd = [
            "node", str(FEISHU_CARD_SCRIPT),
            "--target", target,
            "--image-path", str(image_path),
            "--title", title,
            "--color", color
        ]
        
        # 如果有正文，写入临时文件再传递（避免Windows命令行编码问题）
        if text:
            temp_text_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
            temp_text_file.write(text)
            temp_text_file.close()
            cmd.extend(["--text-file", temp_text_file.name])
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        # 清理临时文件
        if temp_text_file:
            try:
                Path(temp_text_file.name).unlink()
            except:
                pass
        
        # 检查执行结果
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "未知错误"
            return {
                "success": False,
                "message_id": None,
                "error": f"发送失败: {error_msg}"
            }
        
        # 解析返回的 message_id
        message_id = None
        for line in result.stdout.split('\n'):
            if '"message_id"' in line:
                try:
                    # 尝试从JSON中提取
                    import json
                    start = line.find('{')
                    end = line.rfind('}') + 1
                    if start != -1 and end > start:
                        data = json.loads(line[start:end])
                        message_id = data.get('message_id')
                except:
                    pass
        
        return {
            "success": True,
            "message_id": message_id,
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        # 清理临时文件
        if temp_text_file:
            try:
                Path(temp_text_file.name).unlink()
            except:
                pass
        return {
            "success": False,
            "message_id": None,
            "error": "发送超时"
        }
    except Exception as e:
        # 清理临时文件
        if temp_text_file:
            try:
                Path(temp_text_file.name).unlink()
            except:
                pass
        return {
            "success": False,
            "message_id": None,
            "error": str(e)
        }
        
        # 检查执行结果
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "未知错误"
            return {
                "success": False,
                "message_id": None,
                "error": f"发送失败: {error_msg}"
            }
        
        # 解析返回的 message_id
        message_id = None
        for line in result.stdout.split('\n'):
            if '"message_id"' in line:
                try:
                    # 尝试从JSON中提取
                    import json
                    start = line.find('{')
                    end = line.rfind('}') + 1
                    if start != -1 and end > start:
                        data = json.loads(line[start:end])
                        message_id = data.get('message_id')
                except:
                    pass
        
        return {
            "success": True,
            "message_id": message_id,
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message_id": None,
            "error": "发送超时"
        }
    except Exception as e:
        return {
            "success": False,
            "message_id": None,
            "error": str(e)
        }


def generate_title(category: str, keyword: Optional[str] = None, is_url: bool = False) -> str:
    """
    生成符合聊天习惯的卡片标题
    
    Args:
        category: 表情包分类
        keyword: 用户输入的关键词
        is_url: 是否是从URL获取的
        
    Returns:
        卡片标题文本
    """
    # 分类到中文映射
    category_names = {
        "panda": "熊猫头",
        "cats": "猫咪",
        "dogs": "狗狗",
        "anime": "二次元",
        "wuxia": "武侠",
        "animals": "小动物",
        "programmer": "程序员梗",
        "misc": "表情包"
    }
    
    cat_name = category_names.get(category, category)
    
    # 根据是否有关键词生成不同的标题
    titles = [
        f"Boss，你要的{cat_name}来了！",
        f"给你找了个{cat_name}～",
        f"{cat_name}表情包送上！",
        f"来，{cat_name}～",
        f"{cat_name}来啦！",
    ]
    
    import random
    return random.choice(titles)


def send_meme_feishu(
    target: str,
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    use_local: bool = True
) -> dict:
    """
    发送表情包到飞书（卡片消息格式）
    
    这是主要的飞书发送接口，自动选择本地或URL源
    
    Args:
        target: 目标用户或群聊ID (ou_xxx 或 oc_xxx)
        category: 指定分类
        keyword: 用户输入的关键词（优先于category）
        use_local: 优先使用本地库存（默认True）
        
    Returns:
        {
            "success": bool,
            "message_id": str | None,
            "category": str | None,
            "title": str,
            "error": str | None
        }
    """
    temp_file = None
    
    try:
        # 1. 确定要使用的分类
        if keyword:
            # 尝试从关键词获取分类
            keyword_lower = keyword.lower().strip()
            keyword_map = {
                "熊猫头": "panda", "熊猫": "panda", "panda": "panda", "滚滚": "panda",
                "猫咪": "cats", "猫": "cats", "cat": "cats", "cats": "cats", "喵喵": "cats",
                "狗狗": "dogs", "狗": "dogs", "dog": "dogs", "dogs": "dogs", "汪汪": "dogs",
                "动漫": "anime", "anime": "anime", "二次元": "anime", "动画": "anime",
                "武侠": "wuxia", "wuxia": "wuxia", "功夫": "wuxia",
                "动物": "animals", "animals": "animals", "animal": "animals",
                "程序员": "programmer", "programmer": "programmer", "码农": "programmer",
                "coding": "programmer", "code": "programmer",
                "杂项": "misc", "misc": "misc", "其他": "misc",
            }
            category = keyword_map.get(keyword_lower, category)
        
        # 1.5 工作时间安全检查
        original_category = category
        if category and not is_category_safe(category):
            # 工作时间，分类不安全，切换到安全分类
            import random
            category = random.choice(WORK_SAFE_CATEGORIES)
            print(f"[WorkSafe] {original_category} → {category} (工作时间自动切换)")
        elif not category:
            # 随机选择时，也要考虑工作时间
            import random
            safe_categories = get_safe_categories()
            category = random.choice(safe_categories)
        
        # 2. 尝试获取表情包
        image_path = None
        actual_category = category
        
        if use_local:
            # 先尝试本地库存
            if keyword and not category:
                result = get_meme_by_keyword(keyword)
            else:
                result = send_random_meme(category)
            
            if result.get("success") and result.get("file_path"):
                image_path = result["file_path"]
                actual_category = result.get("category", category or "misc")
        
        # 如果本地没有，尝试URL
        if not image_path:
            url_result = get_url_by_keyword(keyword or category or "")
            if url_result.get("success") and url_result.get("url"):
                # 下载URL图片
                temp_file = download_image(url_result["url"])
                image_path = str(temp_file)
                actual_category = url_result.get("category", category or "misc")
        
        if not image_path:
            return {
                "success": False,
                "message_id": None,
                "category": actual_category,
                "title": None,
                "error": "没有找到可用的表情包"
            }
        
        # 3. 生成标题和互动文案
        title = generate_title(actual_category, keyword, is_url=(temp_file is not None))
        interactive_text = generate_interactive_message(actual_category)
        
        # 4. 选择颜色
        color_map = {
            "panda": "grey",
            "cats": "blue",
            "dogs": "orange",
            "anime": "purple",
            "wuxia": "red",
            "animals": "green",
            "programmer": "blue",
            "misc": "blue"
        }
        color = color_map.get(actual_category, "blue")
        
        # 5. 发送卡片消息
        result = send_feishu_card(target, image_path, title, interactive_text, color)
        
        return {
            "success": result["success"],
            "message_id": result.get("message_id"),
            "category": actual_category,
            "title": title,
            "error": result.get("error")
        }
        
    except Exception as e:
        return {
            "success": False,
            "message_id": None,
            "category": category,
            "title": None,
            "error": str(e)
        }
    
    finally:
        # 清理临时文件
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except:
                pass


# 便捷函数
def send_panda(target: str) -> dict:
    """发送熊猫头"""
    return send_meme_feishu(target, category="panda")


def send_cat(target: str) -> dict:
    """发送猫咪"""
    return send_meme_feishu(target, category="cats")


def send_dog(target: str) -> dict:
    """发送狗狗"""
    return send_meme_feishu(target, category="dogs")


def send_anime(target: str) -> dict:
    """发送二次元"""
    return send_meme_feishu(target, category="anime")


def send_programmer(target: str) -> dict:
    """发送程序员梗"""
    return send_meme_feishu(target, category="programmer")


def send_wuxia(target: str) -> dict:
    """发送武侠"""
    return send_meme_feishu(target, category="wuxia")


def send_random(target: str) -> dict:
    """发送随机表情包"""
    return send_meme_feishu(target, category=None)


def send_by_keyword(target: str, keyword: str) -> dict:
    """根据关键词发送"""
    return send_meme_feishu(target, keyword=keyword)


if __name__ == "__main__":
    # 测试
    import json
    
    print("测试飞书表情包发送:")
    print(f"Feishu Card 脚本路径: {FEISHU_CARD_SCRIPT}")
    print(f"脚本存在: {FEISHU_CARD_SCRIPT.exists()}")
    
    print("\n测试标题生成:")
    for cat in ["panda", "cats", "anime", "programmer"]:
        print(f"  {cat}: {generate_title(cat)}")
