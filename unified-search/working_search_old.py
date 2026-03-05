"""
搜索解决方案 - 本地可用方案
"""

import json
import subprocess
from typing import Dict, List

def search_with_gh_repo(query: str) -> Dict:
    """
    使用 gh CLI 搜索 GitHub 仓库
    不需要 API Key！
    """
    try:
        # 搜索仓库
        result = subprocess.run(
            ["gh", "search", "repos", query, "--limit", "5", "--json", "name,description,url,stargazersCount"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                "success": True,
                "backend": "gh-cli",
                "results": [
                    {
                        "title": item.get("name", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("description", "") or "No description",
                        "stars": item.get("stargazersCount", 0)
                    }
                    for item in data
                ]
            }
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_with_curl_ddg(query: str) -> Dict:
    """
    使用 curl 访问 DuckDuckGo HTML 版本
    不需要 API！
    """
    import subprocess
    import re
    
    try:
        # 使用 curl 获取 DuckDuckGo HTML
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        
        result = subprocess.run(
            ["curl", "-s", "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=15
        )
        
        if result.returncode == 0:
            html = result.stdout
            
            # 简单的正则提取结果
            results = []
            # 提取链接和标题
            links = re.findall(r'class="result__a" href="([^"]+)"[^>]*>([^<]+)', html)
            snippets = re.findall(r'class="result__snippet"[^>]*>([^<]+)', html)
            
            for i, (url, title) in enumerate(links[:5]):
                snippet = snippets[i] if i < len(snippets) else ""
                results.append({
                    "title": title.strip(),
                    "url": url,
                    "snippet": snippet.strip()[:150]
                })
            
            return {
                "success": True,
                "backend": "duckduckgo-html",
                "results": results
            }
        else:
            return {"success": False, "error": "curl failed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_local_readme(skills_dir: str, query: str) -> Dict:
    """
    搜索本地技能 README
    """
    from pathlib import Path
    
    results = []
    skills_path = Path(skills_dir)
    
    for skill_dir in skills_path.iterdir():
        if skill_dir.is_dir():
            readme = skill_dir / "SKILL.md"
            if readme.exists():
                content = readme.read_text(encoding="utf-8", errors="ignore").lower()
                if query.lower() in content:
                    # 提取描述
                    desc = ""
                    for line in content.split("\n")[:20]:
                        if "description" in line or line.strip().startswith("-"):
                            desc = line.strip()
                            break
                    
                    results.append({
                        "title": skill_dir.name,
                        "url": str(readme),
                        "snippet": desc or "Local skill",
                        "source": "local"
                    })
    
    return {
        "success": True,
        "backend": "local",
        "results": results
    }


class WorkingSearch:
    """可用的搜索工具集合"""
    
    def __init__(self, skills_dir: str = "D:/openclaw/skills"):
        self.skills_dir = skills_dir
    
    def search(self, query: str, source: str = "auto") -> Dict:
        """
        搜索 - 自动选择可用方案
        
        Args:
            query: 搜索关键词
            source: 来源 (gh/curl/local/auto)
        """
        if source == "auto":
            # 优先尝试 GitHub CLI
            result = search_with_gh_repo(query)
            if result.get("success"):
                return result
            
            # 然后尝试 curl + DDG
            result = search_with_curl_ddg(query)
            if result.get("success"):
                return result
            
            # 最后搜索本地
            return search_local_readme(self.skills_dir, query)
        
        elif source == "gh":
            return search_with_gh_repo(query)
        elif source == "curl":
            return search_with_curl_ddg(query)
        elif source == "local":
            return search_local_readme(self.skills_dir, query)
        
        return {"success": False, "error": "Unknown source"}


# 便捷函数
def search(query: str, source: str = "auto") -> Dict:
    """搜索入口"""
    searcher = WorkingSearch()
    return searcher.search(query, source)


if __name__ == "__main__":
    # 测试
    print("Testing GitHub CLI search...")
    result = search("OpenClaw skills", source="gh")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
