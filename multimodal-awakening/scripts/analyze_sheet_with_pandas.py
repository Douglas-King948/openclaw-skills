#!/usr/bin/env python3
"""
表格处理脚本 - 使用 pandas 分析 Excel/CSV
"""

import os
import sys
import json
from pathlib import Path

def analyze_sheet(file_path: str) -> dict:
    """
    分析表格文件
    """
    try:
        import pandas as pd
        
        # 读取文件
        ext = Path(file_path).suffix.lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            return {
                'success': False,
                'error': f'不支持的文件格式: {ext}'
            }
        
        # 基本信息
        info = {
            'success': True,
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        }
        
        # 数值列统计
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            info['numeric_summary'] = df[numeric_cols].describe().to_dict()
        
        # 缺失值统计
        missing = df.isnull().sum()
        if missing.any():
            info['missing_values'] = missing[missing > 0].to_dict()
        
        # 样本数据
        info['sample_data'] = df.head(5).to_dict('records')
        
        # 生成描述
        description = f"""
表格分析结果：

基本信息：
- 行数: {info['rows']}
- 列数: {info['columns']}
- 列名: {', '.join(info['column_names'])}

数据类型：
{chr(10).join([f"  - {col}: {dtype}" for col, dtype in info['dtypes'].items()])}

"""
        
        if 'numeric_summary' in info:
            description += "数值列统计：\n"
            for col, stats in info['numeric_summary'].items():
                description += f"  {col}: 均值={stats.get('mean', 'N/A'):.2f}, 标准差={stats.get('std', 'N/A'):.2f}\n"
        
        info['description'] = description
        
        return info
        
    except ImportError:
        return {
            'success': False,
            'error': '未安装 pandas。请运行: pip install pandas openpyxl'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_sheet_with_pandas.py <表格路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = analyze_sheet(file_path)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
