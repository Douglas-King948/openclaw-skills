"""
Unified Search - Multiple Search Backends
修复版 - 添加更多可靠后端
"""

import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    source: str

class BingSearchBackend:
    """Bing Search - 需要 API Key"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        import os
        import urllib.request
        
        api_key = os.environ.get("BING_API_KEY")
        if not api_key:
            return {"success": False, "error": "BING_API_KEY not set"}
        
        url = f"https://api.bing.microsoft.com/v7.0/search?q={urllib.parse.quote(query)}&count={max_results}"
        
        req = urllib.request.Request(url)
        req.add_header("Ocp-Apim-Subscription-Key", api_key)
        
        try:
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("webPages", {}).get("value", []):
                results.append(SearchResult(
                    title=item.get("name", ""),
                    url=item.get("url", ""),
                    snippet=item.get("snippet", ""),
                    source="bing"
                ))
            
            return {
                "success": True,
                "results": [r.__dict__ for r in results],
                "total": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class SerpApiBackend:
    """SerpAPI - Google搜索结果"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        import os
        import urllib.request
        
        api_key = os.environ.get("SERPAPI_KEY")
        if not api_key:
            return {"success": False, "error": "SERPAPI_KEY not set"}
        
        url = f"https://serpapi.com/search?q={urllib.parse.quote(query)}&api_key={api_key}"
        
        try:
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("organic_results", [])[:max_results]:
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    source="serpapi"
                ))
            
            return {
                "success": True,
                "results": [r.__dict__ for r in results],
                "total": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class JinaSearchBackend:
    """Jina AI Reader - 免费网页搜索和阅读"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        import urllib.request
        
        url = f"https://s.jina.ai/{urllib.parse.quote(query)}"
        
        try:
            req = urllib.request.Request(url)
            req.add_header("Accept", "application/json")
            
            response = urllib.request.urlopen(req, timeout=15)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("data", [])[:max_results]:
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("content", "")[:200],
                    source="jina"
                ))
            
            return {
                "success": True,
                "results": [r.__dict__ for r in results],
                "total": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class YouSearchBackend:
    """You.com Search - 免费API可用"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        import os
        import urllib.request
        
        api_key = os.environ.get("YDC_API_KEY")
        if not api_key:
            return {"success": False, "error": "YDC_API_KEY not set"}
        
        url = "https://api.ydc-index.io/search"
        params = f"?query={urllib.parse.quote(query)}&count={max_results}"
        
        req = urllib.request.Request(url + params)
        req.add_header("X-API-Key", api_key)
        
        try:
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("hits", []):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("description", ""),
                    source="you"
                ))
            
            return {
                "success": True,
                "results": [r.__dict__ for r in results],
                "total": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class ExaSearchBackend:
    """Exa AI Search - 语义搜索"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        import os
        import urllib.request
        
        api_key = os.environ.get("EXA_API_KEY")
        if not api_key:
            return {"success": False, "error": "EXA_API_KEY not set"}
        
        url = "https://api.exa.ai/search"
        
        data = json.dumps({
            "query": query,
            "num_results": max_results,
            "use_autoprompt": True
        }).encode()
        
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("x-api-key", api_key)
        
        try:
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("results", []):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("text", "")[:200],
                    source="exa"
                ))
            
            return {
                "success": True,
                "results": [r.__dict__ for r in results],
                "total": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class UnifiedSearch:
    """统一搜索引擎 - 自动故障转移"""
    
    def __init__(self):
        self.backends = {
            "jina": JinaSearchBackend(),      # 免费，优先
            "bing": BingSearchBackend(),      # 需要 API Key
            "you": YouSearchBackend(),        # 需要 API Key
            "exa": ExaSearchBackend(),        # 需要 API Key
            "serpapi": SerpApiBackend(),      # 需要 API Key
        }
    
    def search(self, query: str, backend: str = None, max_results: int = 5) -> Dict:
        """
        搜索 - 自动选择可用后端
        
        Args:
            query: 搜索关键词
            backend: 指定后端 (jina/bing/you/exa/serpapi)，None则自动选择
            max_results: 最大结果数
        """
        if backend and backend in self.backends:
            # 使用指定后端
            result = self.backends[backend].search(query, max_results)
            if result.get("success"):
                return result
        
        # 自动尝试所有后端
        for name, backend_obj in self.backends.items():
            print(f"Trying {name}...")
            result = backend_obj.search(query, max_results)
            if result.get("success"):
                result["backend_used"] = name
                return result
            time.sleep(0.5)  # 避免请求过快
        
        return {
            "success": False,
            "error": "All search backends failed"
        }


# 便捷函数
def search(query: str, backend: str = None, max_results: int = 5) -> Dict:
    """统一搜索接口"""
    searcher = UnifiedSearch()
    return searcher.search(query, backend, max_results)


if __name__ == "__main__":
    # 测试
    result = search("OpenClaw skills github", max_results=3)
    print(json.dumps(result, indent=2, ensure_ascii=False))
