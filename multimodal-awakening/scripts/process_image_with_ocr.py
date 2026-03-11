#!/usr/bin/env python3
"""
图片处理降级方案 - 当模型不支持 vision 时使用
使用 PIL 和 pytesseract/easyocr 进行 OCR
"""

import os
import sys
from pathlib import Path

def process_image_with_ocr(image_path: str) -> dict:
    """
    使用 OCR 提取图片中的文字
    
    Args:
        image_path: 图片文件路径
    
    Returns:
        {
            'success': bool,
            'text': str,  # 提取的文字
            'error': str  # 错误信息（如果有）
        }
    """
    try:
        # 尝试导入 OCR 库
        try:
            import easyocr
            reader = easyocr.Reader(['ch_sim', 'en'])
            result = reader.readtext(image_path)
            text = '\n'.join([item[1] for item in result])
            return {
                'success': True,
                'text': text,
                'method': 'easyocr'
            }
        except ImportError:
            pass
        
        # 降级到 pytesseract
        try:
            from PIL import Image
            import pytesseract
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            return {
                'success': True,
                'text': text,
                'method': 'pytesseract'
            }
        except ImportError:
            pass
        
        # 最终降级：返回图片基本信息
        from PIL import Image
        with Image.open(image_path) as img:
            return {
                'success': True,
                'text': f'[图片信息] 格式: {img.format}, 尺寸: {img.size}, 模式: {img.mode}',
                'method': 'basic_info',
                'note': '未安装 OCR 库，仅返回图片基本信息。如需文字识别，请安装 easyocr 或 pytesseract。'
            }
            
    except Exception as e:
        return {
            'success': False,
            'text': '',
            'error': str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python process_image_with_ocr.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = process_image_with_ocr(image_path)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
