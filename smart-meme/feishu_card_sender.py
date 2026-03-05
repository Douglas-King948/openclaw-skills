#!/usr/bin/env python3
"""
Smart Meme - 飞书卡片发送器 (Python 版)
完全独立的飞书卡片发送能力，无需依赖外部 Node.js 脚本
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any

# 标记模块可用
FEISHU_CARD_AVAILABLE = True

# Token 缓存
_token_cache = None
TOKEN_CACHE_FILE = Path.home() / ".openclaw" / "cache" / "feishu_token.json"
IMAGE_KEY_CACHE_FILE = Path.home() / ".openclaw" / "cache" / "feishu_image_keys.json"


def _load_env():
    """加载环境变量"""
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key, value)


def get_access_token() -> str:
    """
    获取飞书 access token
    带缓存机制，避免频繁请求
    """
    global _token_cache
    
    # 检查内存缓存
    if _token_cache and _token_cache.get('expires', 0) > time.time():
        return _token_cache['token']
    
    # 检查文件缓存
    try:
        if TOKEN_CACHE_FILE.exists():
            with open(TOKEN_CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('expires', 0) > time.time():
                    _token_cache = data
                    return data['token']
    except Exception:
        pass
    
    # 加载环境变量
    _load_env()
    
    app_id = os.environ.get('FEISHU_APP_ID')
    app_secret = os.environ.get('FEISHU_APP_SECRET')
    
    if not app_id or not app_secret:
        raise ValueError("缺少 FEISHU_APP_ID 或 FEISHU_APP_SECRET 环境变量")
    
    # 请求新 token
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'app_id': app_id, 'app_secret': app_secret}).encode()
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    
    if result.get('code') != 0:
        raise Exception(f"获取 token 失败: {result.get('msg')}")
    
    token = result['app_access_token']
    expires = time.time() + (result.get('expire', 7200) - 300) * 1000  # 提前5分钟过期
    
    _token_cache = {'token': token, 'expires': expires}
    
    # 保存到文件
    try:
        TOKEN_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_token_cache, f)
    except Exception:
        pass
    
    return token


def upload_image(image_path: str) -> str:
    """
    上传图片到飞书，获取 image_key
    
    Args:
        image_path: 本地图片路径
        
    Returns:
        image_key: 飞书图片标识
    """
    # 检查缓存
    import hashlib
    
    with open(image_path, 'rb') as f:
        file_buffer = f.read()
    
    file_hash = hashlib.md5(file_buffer).hexdigest()
    
    # 检查图片缓存
    try:
        if IMAGE_KEY_CACHE_FILE.exists():
            with open(IMAGE_KEY_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                if file_hash in cache:
                    return cache[file_hash]
    except Exception:
        cache = {}
    
    # 上传图片
    token = get_access_token()
    url = 'https://open.feishu.cn/open-apis/im/v1/images'
    
    boundary = '----FormBoundary' + str(int(time.time()))
    
    # 构建 multipart form data
    body = []
    body.append(f'--{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="image_type"')
    body.append(b'')
    body.append(b'message')
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="image"; filename="{Path(image_path).name}"'.encode())
    body.append(b'Content-Type: image/jpeg')
    body.append(b'')
    body.append(file_buffer)
    body.append(f'--{boundary}--'.encode())
    
    data = b'\r\n'.join(body)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    
    if result.get('code') != 0:
        raise Exception(f"上传图片失败: {result.get('msg')}")
    
    image_key = result['data']['image_key']
    
    # 保存缓存
    try:
        cache = {}
        if IMAGE_KEY_CACHE_FILE.exists():
            with open(IMAGE_KEY_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        cache[file_hash] = image_key
        IMAGE_KEY_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(IMAGE_KEY_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f)
    except Exception:
        pass
    
    return image_key


def send_feishu_card(
    target: str,
    image_path: str,
    title: str = "",
    text: str = "",
    color: str = "blue"
) -> Dict[str, Any]:
    """
    发送飞书卡片消息（带图片）
    
    Args:
        target: 目标用户或群聊 ID (ou_xxx 或 oc_xxx)
        image_path: 本地图片路径
        title: 卡片标题
        text: 卡片正文
        color: 标题颜色 (blue/orange/red/green)
        
    Returns:
        {"success": bool, "message_id": str|None, "error": str|None}
    """
    try:
        # 上传图片获取 image_key
        image_key = upload_image(image_path)
        
        # 构建卡片内容 - 使用正确的飞书卡片格式
        elements = []
        
        # 添加图片
        elements.append({
            "tag": "img",
            "img_key": image_key,
            "alt": {
                "tag": "plain_text",
                "content": "表情包"
            }
        })
        
        # 添加文本
        if text:
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": text
                }
            })
        
        card = {
            "config": {
                "wide_screen_mode": True
            },
            "elements": elements
        }
        
        # 添加 header
        if title:
            card["header"] = {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": color
            }
        
        # 发送卡片
        token = get_access_token()
        
        # 判断是用户还是群聊
        if target.startswith('ou_'):
            receive_id_type = 'open_id'
        elif target.startswith('oc_'):
            receive_id_type = 'chat_id'
        else:
            receive_id_type = 'open_id'
        
        url = 'https://open.feishu.cn/open-apis/im/v1/messages'
        
        data = json.dumps({
            "receive_id": target,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }).encode()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        req = urllib.request.Request(f'{url}?receive_id_type={receive_id_type}', 
                                     data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        
        if result.get('code') != 0:
            return {
                "success": False,
                "message_id": None,
                "error": f"发送失败: {result.get('msg')}"
            }
        
        return {
            "success": True,
            "message_id": result.get('data', {}).get('message_id'),
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "message_id": None,
            "error": str(e)
        }


if __name__ == '__main__':
    # 测试
    import tempfile
    
    # 下载测试图片
    test_url = 'https://pic.re/image?q=monkey'
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(test_url, headers=headers)
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        image_data = resp.read()
    
    temp_path = Path(tempfile.gettempdir()) / 'test_monkey.jpg'
    with open(temp_path, 'wb') as f:
        f.write(image_data)
    
    # 发送测试
    result = send_feishu_card(
        target='ou_f35e74b14ff44420bdd4ede905c3b587',
        image_path=str(temp_path),
        title='🐵 马喽驾到！(Python版)',
        text='完全独立的飞书卡片发送～',
        color='orange'
    )
    
    print('Result:', result)
