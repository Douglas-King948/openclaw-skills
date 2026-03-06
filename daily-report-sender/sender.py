"""
Daily Report Sender - 飞书日报发送器 v3.1
完全独立的技能，支持20种随机风格
"""

import os
import json
import ssl
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import random

# 导入风格库
try:
    from style_library import (
        STYLE_LIBRARY, get_random_style, get_style_by_id,
        format_report_with_style, ReportStyle
    )
except ImportError:
    # 备用简单风格
    class ReportStyle:
        def __init__(self, id, name, icon, keywords, color, title_template, 
                     header_template, footer_template, description):
            self.id = id
            self.name = name
            self.icon = icon
            self.keywords = keywords
            self.color = color
            self.title_template = title_template
            self.header_template = header_template
            self.footer_template = footer_template
            self.description = description
    
    STYLE_LIBRARY = []
    def get_random_style(exclude_ids=None):
        return None
    def get_style_by_id(style_id):
        return None
    def format_report_with_style(items, style):
        return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])

# 禁用SSL验证
ssl._create_default_https_context = ssl._create_unverified_context

# ============ 配置 ============
DEFAULT_TARGET = "ou_f35e74b14ff44420bdd4ede905c3b587"
APP_ID = "cli_a903ccc2bb791bde"
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
DAILY_IMAGE_DIR = Path(__file__).parent / "daily_images"
STYLE_HISTORY_FILE = Path(__file__).parent / "style_history.json"

# 创建目录
DAILY_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# ============ URL源配置 ============
MEME_URLS = {
    "celebrating": [
        "https://pic.re/image?q=celebration",
        "https://pic.re/image?q=happy",
        "https://pic.re/image?q=party",
    ],
    "working": [
        "https://pic.re/image?q=computer",
        "https://pic.re/image?q=work",
        "https://pic.re/image?q=coding",
    ],
    "thinking": [
        "https://pic.re/image?q=thinking",
        "https://pic.re/image?q=cat",
        "https://cataas.com/cat/cute",
    ],
    "wuxia": [
        "https://pic.re/image?q=samurai",
        "https://pic.re/image?q=ninja",
        "https://picsum.photos/400/300",
    ],
    "cthulhu": [
        "https://pic.re/image?q=cthulhu",
        "https://pic.re/image?q=lovecraft",
        "https://pic.re/image?q=eldritch",
        "https://pic.re/image?q=cosmic+horror",
        "https://pic.re/image?q=tentacles",
        "https://pic.re/image?q=dark+fantasy",
    ],
}


# ============ 飞书API ============
class FeishuAPI:
    """飞书API客户端"""
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    _token_cache = None
    _token_expire = 0
    
    @classmethod
    def get_access_token(cls) -> str:
        """获取access token（带缓存）"""
        import time
        
        # 检查缓存
        if cls._token_cache and time.time() < cls._token_expire:
            return cls._token_cache
        
        # 从环境变量获取secret
        app_secret = os.environ.get("FEISHU_APP_SECRET", "")
        if not app_secret:
            raise ValueError("FEISHU_APP_SECRET not set")
        
        url = f"{cls.BASE_URL}/auth/v3/tenant_access_token/internal"
        data = json.dumps({"app_id": APP_ID, "app_secret": app_secret}).encode()
        
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            if result.get("code") == 0:
                cls._token_cache = result["tenant_access_token"]
                cls._token_expire = time.time() + result.get("expire", 7200) - 60
                return cls._token_cache
            else:
                raise Exception(f"Token error: {result}")
    
    @classmethod
    def upload_image(cls, image_path: str) -> str:
        """上传图片到飞书，返回image_key"""
        import mimetypes
        
        token = cls.get_access_token()
        
        # 读取图片
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # 构建multipart form
        boundary = "----FormBoundary" + str(random.randint(100000, 999999))
        
        # 文件部分
        filename = Path(image_path).name
        mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        
        body = []
        body.append(f"--{boundary}".encode())
        body.append(b"Content-Disposition: form-data; name=\"image_type\"")
        body.append(b"")
        body.append(b"message")
        
        body.append(f"--{boundary}".encode())
        body.append(f'Content-Disposition: form-data; name=\"image\"; filename=\"{filename}\"'.encode())
        body.append(f"Content-Type: {mime_type}".encode())
        body.append(b"")
        body.append(image_data)
        
        body.append(f"--{boundary}--".encode())
        
        data = b"\r\n".join(body)
        
        # 发送请求
        url = f"{cls.BASE_URL}/im/v1/images"
        req = urllib.request.Request(
            url, data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            if result.get("code") == 0:
                return result["data"]["image_key"]
            else:
                raise Exception(f"Upload failed: {result}")
    
    @classmethod
    def send_interactive_card(cls, target: str, title: str, content: str, 
                              image_key: str = None, color: str = "blue") -> Dict:
        """发送交互卡片"""
        token = cls.get_access_token()
        
        # 构建卡片内容
        elements = []
        
        # 添加图片
        if image_key:
            elements.append({
                "tag": "img",
                "img_key": image_key,
                "alt": {"tag": "plain_text", "content": "image"}
            })
        
        # 添加文本（使用markdown支持加粗）
        elements.append({
            "tag": "markdown",
            "content": content
        })
        
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": color
            },
            "elements": elements
        }
        
        # 确定接收者类型
        if target.startswith("oc_"):
            receive_id_type = "chat_id"
        else:
            receive_id_type = "open_id"
        
        # 发送
        url = f"{cls.BASE_URL}/im/v1/messages?receive_id_type={receive_id_type}"
        data = json.dumps({
            "receive_id": target,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }).encode()
        
        req = urllib.request.Request(
            url, data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result


# ============ 图片下载 ============
def download_image(url: str, save_path: Path) -> bool:
    """下载图片"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(save_path, "wb") as f:
                f.write(resp.read())
        
        # 验证
        if save_path.exists() and save_path.stat().st_size > 1024:
            return True
        save_path.unlink(missing_ok=True)
        return False
    except Exception as e:
        print(f"Download error: {e}")
        return False


def get_daily_image(keywords: List[str]) -> Optional[Path]:
    """根据关键词获取每日图片"""
    today = datetime.now().strftime("%Y%m%d")
    today_dir = DAILY_IMAGE_DIR / today
    today_dir.mkdir(exist_ok=True)
    
    # 检查已有图片
    existing = list(today_dir.glob("*.jpg")) + list(today_dir.glob("*.png"))
    if existing:
        return existing[0]
    
    # 下载新图片（尝试每个关键词）
    for keyword in keywords[:3]:  # 最多试3个关键词
        url = f"https://pic.re/image?q={keyword}"
        ext = ".png"
        save_path = today_dir / f"daily_{random.randint(1000,9999)}{ext}"
        
        print(f"Downloading: {url}")
        if download_image(url, save_path):
            print(f"Saved: {save_path}")
            return save_path
    
    return None


def get_used_styles() -> List[str]:
    """获取最近使用过的风格ID"""
    try:
        if STYLE_HISTORY_FILE.exists():
            with open(STYLE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
                # 返回最近5天使用过的风格
                return history.get('recent', [])
    except Exception:
        pass
    return []


def record_style_usage(style_id: str):
    """记录风格使用"""
    try:
        history = {'recent': []}
        if STYLE_HISTORY_FILE.exists():
            with open(STYLE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        recent = history.get('recent', [])
        recent.append(style_id)
        # 只保留最近30条记录
        history['recent'] = recent[-30:]
        
        with open(STYLE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Failed to record style usage: {e}")


def send_daily_report_with_style(
    items: List[str],
    target: str = DEFAULT_TARGET,
    style_id: str = None
) -> Dict:
    """
    使用随机风格发送日报
    
    Args:
        items: 日报内容列表
        target: 飞书用户ID
        style_id: 指定风格ID（None则随机）
    
    Returns:
        发送结果
    """
    try:
        # 1. 选择风格
        if style_id:
            style = get_style_by_id(style_id)
        else:
            # 随机选择，避免最近用过的
            used_styles = get_used_styles()
            style = get_random_style(exclude_ids=used_styles)
        
        if not style:
            return {"success": False, "error": "No style available"}
        
        print(f"Selected style: {style.id}")
        
        # 2. 下载图片
        print("Step 1: Downloading image...")
        image_path = get_daily_image(style.keywords)
        if not image_path:
            return {"success": False, "error": "Failed to download image"}
        print(f"Image ready: {image_path}")
        
        # 3. 上传图片到飞书
        print("Step 2: Uploading to Feishu...")
        image_key = FeishuAPI.upload_image(str(image_path))
        print(f"Image uploaded: {image_key}")
        
        # 4. 格式化内容
        print("Step 3: Formatting content...")
        content = format_report_with_style(items, style)
        title = style.title_template.format(name=datetime.now().strftime('%m/%d'))
        
        # 5. 发送卡片
        print("Step 4: Sending card...")
        result = FeishuAPI.send_interactive_card(
            target=target,
            title=title,
            content=content,
            image_key=image_key,
            color=style.color
        )
        
        if result.get("code") == 0:
            # 记录风格使用
            record_style_usage(style.id)
            
            return {
                "success": True,
                "message_id": result["data"]["message_id"],
                "image_key": image_key,
                "image_path": str(image_path),
                "style": {
                    "id": style.id,
                    "name": style.name,
                    "icon": style.icon,
                    "color": style.color
                }
            }
        else:
            return {"success": False, "error": result.get("msg", "Unknown error")}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# 保持向后兼容
send_daily_report = send_daily_report_with_style


# ============ 主函数 ============
def send_daily_report(
    title: str,
    items: List[str],
    mood: str = "working",
    target: str = DEFAULT_TARGET,
    color: str = "blue"
) -> Dict:
    """
    发送日报 - 完整独立流程
    
    Args:
        title: 日报标题
        items: 日报内容列表
        mood: 心情主题
        target: 飞书用户ID
        color: 卡片颜色 (blue/red/green/orange/purple)
    
    Returns:
        发送结果
    """
    try:
        # 1. 下载图片
        print("Step 1: Downloading image...")
        image_path = get_daily_image(mood)
        if not image_path:
            return {"success": False, "error": "Failed to download image"}
        print(f"Image ready: {image_path}")
        
        # 2. 上传图片到飞书
        print("Step 2: Uploading to Feishu...")
        image_key = FeishuAPI.upload_image(str(image_path))
        print(f"Image uploaded: {image_key}")
        
        # 3. 格式化内容
        print("Step 3: Formatting content...")
        if mood == "cthulhu":
            content = format_cthulhu_report(items)
        else:
            content = format_content(items, mood)
        
        # 4. 发送卡片
        print("Step 4: Sending card...")
        result = FeishuAPI.send_interactive_card(
            target=target,
            title=title,
            content=content,
            image_key=image_key,
            color=color
        )
        
        if result.get("code") == 0:
            return {
                "success": True,
                "message_id": result["data"]["message_id"],
                "image_key": image_key,
                "image_path": str(image_path)
            }
        else:
            return {"success": False, "error": result.get("msg", "Unknown error")}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============ 格式化函数 ============
def format_content(items: List[str], mood: str = "working") -> str:
    """格式化日报内容"""
    lines = []
    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines)


def format_cthulhu_report(items: List[str]) -> str:
    """克苏鲁风格格式化"""
    lines = ["**来自深渊的呼唤...**", ""]
    for item in items:
        lines.append(f"◈ {item}")
    return "\n".join(lines)


# ============ 便捷函数 ============
def send_work_report(items: List[str], target: str = DEFAULT_TARGET) -> Dict:
    """工作日报"""
    title = f"💻 工作日报 - {datetime.now().strftime('%m/%d')}"
    return send_daily_report(title, items, "working", target, "blue")


def send_celebration_report(items: List[str], target: str = DEFAULT_TARGET) -> Dict:
    """庆祝日报"""
    title = f"🎉 里程碑报告 - {datetime.now().strftime('%m/%d')}"
    return send_daily_report(title, items, "celebrating", target, "purple")


if __name__ == "__main__":
    # 测试
    result = send_daily_report(
        title="🧪 测试日报",
        items=["测试下载图片", "测试上传飞书", "测试发送卡片"],
        mood="celebrating",
        color="green"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
