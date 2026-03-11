#!/usr/bin/env python3
"""
PDF 处理降级方案 - 当 pdf 工具不可用时使用
"""

import os
import sys
import json
from pathlib import Path

def process_pdf_with_pypdf(pdf_path: str) -> dict:
    """
    使用 PyPDF2 提取 PDF 文本
    """
    try:
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                
                return {
                    'success': True,
                    'text': text[:5000],  # 限制长度
                    'pages': len(reader.pages),
                    'method': 'PyPDF2'
                }
        except ImportError:
            pass
        
        # 降级到 pdfplumber
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    text += "\n"
                
                return {
                    'success': True,
                    'text': text[:5000],
                    'pages': len(pdf.pages),
                    'method': 'pdfplumber'
                }
        except ImportError:
            pass
        
        return {
            'success': False,
            'error': '未安装 PDF 处理库。请安装 PyPDF2 或 pdfplumber：pip install PyPDF2 pdfplumber'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python process_pdf_with_pypdf.py <PDF路径>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    result = process_pdf_with_pypdf(pdf_path)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
