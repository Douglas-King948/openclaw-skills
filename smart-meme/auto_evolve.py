#!/usr/bin/env python3
"""
Auto Evolve - 全自动进化触发器
由 Cron 定时调用，无需人工干预
"""

import subprocess
import sys
from pathlib import Path

def run_evolver():
    """运行进化分析"""
    evolver_path = Path(__file__).parent.parent / "evolver" / "index.js"
    
    try:
        # 运行 evolver（使用 'run' 参数）
        result = subprocess.run(
            ["node", str(evolver_path), "run"],
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
            cwd=str(evolver_path.parent)
        )
        
        print("Evolver output:")
        print(result.stdout)
        
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        
        # evolver 返回 0 表示成功
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("Timeout: Evolve task took too long")
        return False
    except Exception as e:
        print(f"Execution failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Auto Evolve - Starting...")
    print("=" * 50)
    
    success = run_evolver()
    
    if success:
        print("[OK] Evolve completed")
        sys.exit(0)
    else:
        print("[ERROR] Evolve failed")
        sys.exit(1)
