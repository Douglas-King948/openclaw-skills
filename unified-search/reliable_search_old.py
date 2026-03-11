"""
最终搜索方案 - 纯Python实现
使用多种技术绕过限制
"""

import json
import ssl
import urllib.request
import urllib.parse
from typing import Dict, List


def search_searx(query: str, instance: str = "search.sapti.me") -> Dict:
    """
    使用 SearX 公共实例搜索
    SearX 是尊重隐私的元搜索引擎
    """
    try:
        # 使用 SearX 公共实例
        url = f"https://{instance}/search?q={urllib.parse.quote(query)}&format=json"
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        response = urllib.request.urlopen(req, context=ctx, timeout=20)
        data = json.loads(response.read().decode())
        
        results = []
        for item in data.get("results", [])[:5]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")[:200],
                "source": "searx"
            })
        
        return {
            "success": True,
            "backend": "searx",
            "results": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_wikipedia(query: str) -> Dict:
    """
    使用 Wikipedia API 搜索
    免费，无需API Key
    """
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json&srlimit=5"
        
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "OpenClaw/1.0 (research@example.com)")
        
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode())
        
        results = []
        for item in data.get("query", {}).get("search", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
            results.append({
                "title": title,
                "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                "snippet": snippet[:200],
                "source": "wikipedia"
            })
        
        return {
            "success": True,
            "backend": "wikipedia",
            "results": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_github_topic(topic: str) -> Dict:
    """
    使用 GitHub Topics API 搜索
    免费，无需API Key
    """
    try:
        url = f"https://api.github.com/search/repositories?q=topic:{urllib.parse.quote(topic)}&sort=stars&order=desc&per_page=5"
        
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "OpenClaw/1.0")
        
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode())
        
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("full_name", ""),
                "url": item.get("html_url", ""),
                "snippet": item.get("description", "") or "No description",
                "stars": item.get("stargazers_count", 0),
                "source": "github"
            })
        
        return {
            "success": True,
            "backend": "github-api",
            "results": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


class ReliableSearch:
    """可靠的搜索工具"""
    
    def search(self, query: str, source: str = "auto") -> Dict:
        """
        搜索 - 自动选择可用方案
        """
        # 先尝试 GitHub（代码/仓库搜索）
        if source in ("auto", "github"):
            result = search_github_topic(query.replace(" ", "-").lower())
            if result.get("success") and result.get("results"):
                return result
        
        # 尝试 Wikipedia（知识搜索）
        if source in ("auto", "wiki"):
            result = search_wikipedia(query)
            if result.get("success") and result.get("results"):
                return result
        
        # 尝试 SearX
        if source in ("auto", "searx"):
            result = search_searx(query)
            if result.get("success"):
                return result
        
        return {
            "success": False,
            "error": "All search methods failed"
        }


# 便捷函数
def search(query: str, source: str = "auto") -> Dict:
    """搜索入口"""
    searcher = ReliableSearch()
    return searcher.search(query, source)


if __name__ == "__main__":
    # 测试
    print("Testing Wikipedia search...")
    result = search("Python programming", source="wiki")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:800])
