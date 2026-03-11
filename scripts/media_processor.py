#!/usr/bin/env python3
"""
Multimodal Awakening - 通用媒体处理器
不依赖任何特定渠道工具，仅使用通用工具或 Python 脚本
"""

import os
import re
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# 媒体类型映射
MEDIA_TYPE_MAP = {
    # 图片
    '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
    '.webp': 'image', '.bmp': 'image', '.svg': 'image',
    
    # 音频
    '.mp3': 'audio', '.wav': 'audio', '.ogg': 'audio', '.m4a': 'audio',
    '.flac': 'audio', '.aac': 'audio',
    
    # PDF
    '.pdf': 'pdf',
    
    # 表格
    '.xlsx': 'sheet', '.xls': 'sheet', '.csv': 'sheet', '.tsv': 'sheet',
    
    # 代码文件
    '.py': 'code', '.js': 'code', '.ts': 'code', '.java': 'code',
    '.cpp': 'code', '.c': 'code', '.h': 'code', '.go': 'code',
    '.rs': 'code', '.rb': 'code', '.php': 'code', '.swift': 'code',
    '.kt': 'code', '.scala': 'code', '.r': 'code', '.m': 'code',
    '.json': 'code', '.xml': 'code', '.yaml': 'code', '.yml': 'code',
    '.toml': 'code', '.ini': 'code', '.conf': 'code',
    
    # 视频
    '.mp4': 'video', '.avi': 'video', '.mov': 'video', '.mkv': 'video',
    '.webm': 'video', '.flv': 'video'
}


def extract_media_refs(text: str) -> List[Tuple[str, str]]:
    """
    从文本中提取所有媒体引用
    格式: [media:type:location]
    
    Returns:
        List[Tuple[type, path]]: 媒体类型和路径的列表
    """
    pattern = r'\[media:([a-z]+):([^\]]+)\]'
    matches = re.findall(pattern, text)
    return [(m[0], m[1]) for m in matches]


def detect_media_type(file_path: str) -> Optional[str]:
    """
    根据文件扩展名检测媒体类型
    """
    ext = Path(file_path).suffix.lower()
    return MEDIA_TYPE_MAP.get(ext)


def generate_analysis_prompt(media_type: str, user_text: str = "") -> str:
    """
    根据媒体类型和用户输入生成分析 prompt
    """
    prompts = {
        'image': """请详细分析这张图片：
1. 图片类型（截图、照片、文档等）
2. 主要内容和物体
3. 文字内容（OCR）
4. 布局和视觉特征
5. 其他显著特征

请尽可能详细。""",

        'audio': """请转写这段音频内容，并提供：
1. 完整转写文本
2. 内容摘要
3. 关键信息提取
4. 说话人识别（如果可能）""",

        'pdf': """请分析这份 PDF 文档：
1. 文档主题和结构
2. 主要内容和结论
3. 关键数据和表格
4. 文档摘要（200字以内）""",

        'sheet': """请分析这个表格数据：
1. 数据概述（行列数、字段说明）
2. 统计摘要（数值列的基本统计）
3. 数据质量（缺失值、异常值）
4. 分析洞察和建议""",

        'code': """请分析这段代码：
1. 代码功能概述
2. 关键逻辑和算法
3. 代码质量评估
4. 潜在问题和改进建议""",

        'video': """请分析这个视频：
1. 视频内容概述
2. 关键场景识别
3. 视频摘要
4. 时间戳标记的重要事件"""
    }
    
    base_prompt = prompts.get(media_type, "请分析这个文件的内容")
    
    if user_text:
        return f"{base_prompt}\n\n用户的具体问题：{user_text}"
    
    return base_prompt


class MediaProcessor:
    """
    通用媒体处理器 - 不依赖特定渠道工具
    """
    
    def __init__(self):
        self.processors = {
            'image': self.process_image,
            'audio': self.process_audio,
            'pdf': self.process_pdf,
            'sheet': self.process_sheet,
            'code': self.process_code,
            'video': self.process_video
        }
    
    def process(self, media_type: str, file_path: str, user_text: str = "") -> Dict:
        """
        处理媒体文件
        """
        processor = self.processors.get(media_type)
        if not processor:
            return {
                'success': False,
                'error': f'不支持的媒体类型: {media_type}'
            }
        
        if not os.path.exists(file_path):
            return {
                'success': False,
                'error': f'文件不存在: {file_path}'
            }
        
        try:
            return processor(file_path, user_text)
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_image(self, file_path: str, user_text: str = "") -> Dict:
        """
        处理图片 - 使用通用的 image 工具
        """
        prompt = generate_analysis_prompt('image', user_text)
        
        # 返回工具调用参数，实际调用由 Agent 执行
        return {
            'success': True,
            'type': 'image',
            'tool': 'image',
            'params': {
                'image': file_path,
                'prompt': prompt
            }
        }
    
    def process_audio(self, file_path: str, user_text: str = "") -> Dict:
        """
        处理音频 - 使用 Python + Whisper
        """
        # 这里返回处理指令，实际执行由 Agent 调用 Python 脚本
        return {
            'success': True,
            'type': 'audio',
            'tool': 'python_script',
            'script_hint': '使用 whisper 模型转写音频',
            'params': {
                'file_path': file_path,
                'language': 'zh'
            }
        }
    
    def process_pdf(self, file_path: str, user_text: str = "") -> Dict:
        """
        处理 PDF - 使用通用的 pdf 工具
        """
        prompt = generate_analysis_prompt('pdf', user_text)
        
        return {
            'success': True,
            'type': 'pdf',
            'tool': 'pdf',
            'params': {
                'pdf': file_path,
                'prompt': prompt
            }
        }
    
    def process_sheet(self, file_path: str, user_text: str = "") -> Dict:
        """
        处理表格 - 使用 Python + pandas
        """
        return {
            'success': True,
            'type': 'sheet',
            'tool': 'python_script',
            'script_hint': '使用 pandas 读取并分析表格',
            'params': {
                'file_path': file_path
            }
        }
    
    def process_code(self, file_path: str, user_text: str = "") -> Dict:
        """
        处理代码文件 - 使用通用的 read 工具
        """
        prompt = generate_analysis_prompt('code', user_text)
        
        return {
            'success': True,
            'type': 'code',
            'tool': 'read_then_analyze',
            'params': {
                'file_path': file_path,
                'prompt': prompt
            }
        }
    
    def process_video(self, file_path: str, user_text: str = "") -> Dict:
        """
        处理视频 - 提取关键帧后使用 image 工具
        """
        return {
            'success': True,
            'type': 'video',
            'tool': 'video_extract_then_analyze',
            'steps': [
                '使用 ffmpeg 提取关键帧',
                '使用 image 工具分析关键帧'
            ],
            'params': {
                'file_path': file_path,
                'fps': 1  # 每秒提取1帧
            }
        }


def process_message_with_media(message_text: str) -> List[Dict]:
    """
    处理包含媒体引用的消息
    
    Args:
        message_text: 消息文本，可能包含 [media:type:path] 标记
    
    Returns:
        处理结果列表
    """
    media_refs = extract_media_refs(message_text)
    
    if not media_refs:
        return []
    
    # 提取用户文本（去掉媒体标记后的内容）
    user_text = re.sub(r'\[media:[a-z]+:[^\]]+\]', '', message_text).strip()
    
    processor = MediaProcessor()
    results = []
    
    for media_type, file_path in media_refs:
        result = processor.process(media_type, file_path, user_text)
        results.append(result)
    
    return results


# 测试
if __name__ == "__main__":
    # 测试用例
    test_messages = [
        "[media:image:file:///tmp/test.jpg] 请分析这张图片",
        "[media:pdf:file:///tmp/doc.pdf]",
        "[media:audio:file:///tmp/voice.ogg] 转写这段语音",
        "[media:sheet:file:///tmp/data.xlsx] 分析这个数据",
        "普通文本消息，没有媒体"
    ]
    
    for msg in test_messages:
        print(f"\n消息: {msg}")
        results = process_message_with_media(msg)
        if results:
            for r in results:
                print(f"  处理结果: {json.dumps(r, indent=2, ensure_ascii=False)}")
        else:
            print("  没有检测到媒体")
