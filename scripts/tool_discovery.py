#!/usr/bin/env python3
"""
工具发现与适配模块 (Tool Discovery & Adaptation)
自动检测当前 OpenClaw 环境可用的工具
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Optional


class ToolDiscovery:
    """
    自动发现当前 OpenClaw 环境可用的工具
    """
    
    # 通用层工具列表（不依赖特定渠道）
    CORE_TOOLS = {
        'read', 'write', 'edit', 'exec', 'process',
        'image', 'pdf', 'web_search', 'web_fetch', 'browser'
    }
    
    # 媒体处理工具
    MEDIA_TOOLS = {
        'image': {'input_types': ['image'], 'description': 'Vision analysis'},
        'pdf': {'input_types': ['pdf'], 'description': 'PDF extraction'},
    }
    
    # 工具到媒体类型的映射
    TOOL_MEDIA_MAP = {
        'image': ['image'],
        'pdf': ['pdf'],
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化工具发现器
        
        Args:
            config_path: OpenClaw 配置文件路径，默认自动查找
        """
        self.config = self._load_config(config_path)
        self.available_tools: Set[str] = set()
        self.media_capabilities: Dict[str, Dict] = {}
        self._discover_tools()
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载 OpenClaw 配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # 自动查找配置文件
        possible_paths = [
            os.path.expanduser('~/.openclaw/openclaw.json'),
            os.path.expanduser('~/.config/openclaw/openclaw.json'),
            '/etc/openclaw/openclaw.json',
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        
        return {}
    
    def _discover_tools(self):
        """发现可用工具"""
        # 1. 从 tools.profile 获取基础工具集
        profile = self.config.get('tools', {}).get('profile', 'full')
        self.available_tools.update(self._get_profile_tools(profile))
        
        # 2. 检查显式允许的工具
        allow_list = self.config.get('tools', {}).get('allow', [])
        if allow_list:
            self.available_tools.update(allow_list)
        
        # 3. 从模型配置发现媒体能力
        self._discover_media_capabilities()
        
        # 4. 检查 web 工具
        if self.config.get('tools', {}).get('web', {}).get('search', {}).get('enabled'):
            self.available_tools.add('web_search')
        if self.config.get('tools', {}).get('web', {}).get('fetch', {}).get('enabled'):
            self.available_tools.add('web_fetch')
    
    def _get_profile_tools(self, profile: str) -> Set[str]:
        """根据 profile 获取基础工具集"""
        profile_tools = {
            'minimal': {'read', 'write', 'edit'},
            'coding': {'read', 'write', 'edit', 'exec', 'process'},
            'messaging': {'read', 'write', 'edit', 'message'},
            'full': {'read', 'write', 'edit', 'exec', 'process', 'image', 'pdf', 
                     'web_search', 'web_fetch', 'browser', 'canvas'}
        }
        return profile_tools.get(profile, profile_tools['full'])
    
    def _discover_media_capabilities(self):
        """从模型配置发现媒体处理能力"""
        models_config = self.config.get('models', {}).get('providers', {})
        
        for provider_name, provider_config in models_config.items():
            for model in provider_config.get('models', []):
                input_types = model.get('input', [])
                model_id = f"{provider_name}/{model['id']}"
                
                # 检查是否支持图片输入
                if 'image' in input_types:
                    self.media_capabilities['image'] = {
                        'available': True,
                        'models': [model_id],
                        'tool': 'image'
                    }
                    self.available_tools.add('image')
    
    def get_available_tools(self) -> Set[str]:
        """获取所有可用工具"""
        return self.available_tools.copy()
    
    def has_tool(self, tool_name: str) -> bool:
        """检查特定工具是否可用"""
        return tool_name in self.available_tools
    
    def get_media_processors(self) -> Dict[str, Dict]:
        """
        获取可用的媒体处理器
        
        Returns:
            Dict[media_type, processor_info]
        """
        processors = {}
        
        # 图片处理
        if self.has_tool('image') or 'image' in self.media_capabilities:
            processors['image'] = {
                'tool': 'image',
                'available': True,
                'description': '使用 Vision 模型分析图片'
            }
        else:
            processors['image'] = {
                'tool': 'python_script',
                'available': True,
                'description': '使用 Python + PIL/OCR 处理图片',
                'fallback': True
            }
        
        # PDF 处理
        if self.has_tool('pdf'):
            processors['pdf'] = {
                'tool': 'pdf',
                'available': True,
                'description': '使用 pdf 工具提取内容'
            }
        else:
            processors['pdf'] = {
                'tool': 'python_script',
                'available': True,
                'description': '使用 Python + PyPDF2/pdfplumber 处理 PDF',
                'fallback': True
            }
        
        # 音频处理 - 始终使用 Python 方案（通用）
        processors['audio'] = {
            'tool': 'python_script',
            'available': True,
            'description': '使用 Python + Whisper 转写音频'
        }
        
        # 表格处理 - 始终使用 Python 方案（通用）
        processors['sheet'] = {
            'tool': 'python_script',
            'available': True,
            'description': '使用 Python + pandas 分析表格'
        }
        
        # 视频处理 - 始终使用 Python 方案（通用）
        processors['video'] = {
            'tool': 'python_script',
            'available': True,
            'description': '使用 Python + ffmpeg 处理视频'
        }
        
        return processors
    
    def get_tool_adapter(self, media_type: str) -> Dict:
        """
        获取指定媒体类型的工具适配器
        
        优先使用原生工具，其次使用 Python 脚本
        """
        adapters = {
            'image': {
                'priority': ['image', 'python_script'],
                'native_tool': 'image',
                'fallback_script': 'process_image_with_pil.py'
            },
            'pdf': {
                'priority': ['pdf', 'python_script'],
                'native_tool': 'pdf',
                'fallback_script': 'process_pdf_with_pypdf.py'
            },
            'audio': {
                'priority': ['python_script'],  # 通用方案
                'fallback_script': 'transcribe_with_whisper.py'
            },
            'sheet': {
                'priority': ['python_script'],  # 通用方案
                'fallback_script': 'analyze_sheet_with_pandas.py'
            },
            'video': {
                'priority': ['python_script'],  # 通用方案
                'fallback_script': 'extract_video_frames.py'
            },
            'code': {
                'priority': ['read', 'python_script'],
                'native_tool': 'read'
            }
        }
        
        adapter = adapters.get(media_type, {})
        
        # 检查每个优先工具是否可用
        for tool in adapter.get('priority', []):
            if tool == 'python_script' or self.has_tool(tool):
                return {
                    'tool': tool,
                    'available': True,
                    'script': adapter.get('fallback_script') if tool == 'python_script' else None
                }
        
        return {'tool': None, 'available': False}
    
    def generate_adapter_report(self) -> str:
        """生成适配报告"""
        lines = ["=== MCA 工具适配报告 ===\n"]
        
        lines.append(f"配置文件: {self.config.get('path', '自动检测')}")
        lines.append(f"工具配置 Profile: {self.config.get('tools', {}).get('profile', 'default')}")
        lines.append("")
        
        lines.append("可用工具列表:")
        for tool in sorted(self.available_tools):
            lines.append(f"  ✓ {tool}")
        
        lines.append("\n媒体处理器配置:")
        for media_type, info in self.get_media_processors().items():
            status = "原生" if not info.get('fallback') else "降级"
            lines.append(f"  {media_type}: {info['tool']} ({status})")
            lines.append(f"    {info['description']}")
        
        return "\n".join(lines)


# 全局单例
tool_discovery = None

def get_tool_discovery() -> ToolDiscovery:
    """获取工具发现器实例（懒加载）"""
    global tool_discovery
    if tool_discovery is None:
        tool_discovery = ToolDiscovery()
    return tool_discovery


# 便捷函数
def get_available_tools() -> Set[str]:
    """获取可用工具列表"""
    return get_tool_discovery().get_available_tools()

def has_tool(tool_name: str) -> bool:
    """检查工具是否可用"""
    return get_tool_discovery().has_tool(tool_name)

def get_media_processor(media_type: str) -> Dict:
    """获取媒体处理器"""
    return get_tool_discovery().get_tool_adapter(media_type)


if __name__ == "__main__":
    # 测试
    discovery = ToolDiscovery()
    print(discovery.generate_adapter_report())
