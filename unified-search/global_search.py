"""
全球搜索引擎大全 - 实用可用版本
删除不可用的，添加全球范围的
"""

import json
import urllib.request
import urllib.parse
import ssl
from typing import Dict, List, Optional

# 禁用SSL验证（某些国内网站需要）
ssl._create_default_https_context = ssl._create_unverified_context


class SearchEngine:
    """搜索引擎基类"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        raise NotImplementedError


# ==================== 国外搜索引擎 ====================

class WikipediaSearch(SearchEngine):
    """维基百科搜索 - 稳定可用"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json&srlimit={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "OpenClaw/1.0")
            
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
                    "source": "wikipedia-en"
                })
            
            return {"success": True, "backend": "wikipedia-en", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


class WikipediaChineseSearch(SearchEngine):
    """中文维基百科"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            url = f"https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json&srlimit={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "OpenClaw/1.0")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("query", {}).get("search", []):
                title = item.get("title", "")
                snippet = item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                results.append({
                    "title": title,
                    "url": f"https://zh.wikipedia.org/wiki/{urllib.parse.quote(title)}",
                    "snippet": snippet[:200],
                    "source": "wikipedia-zh"
                })
            
            return {"success": True, "backend": "wikipedia-zh", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GitHubSearch(SearchEngine):
    """GitHub 仓库搜索 - 免费API"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "OpenClaw/1.0")
            req.add_header("Accept", "application/vnd.github.v3+json")
            
            response = urllib.request.urlopen(req, timeout=15)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("full_name", ""),
                    "url": item.get("html_url", ""),
                    "snippet": item.get("description", "") or "No description",
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language", "Unknown"),
                    "source": "github"
                })
            
            return {"success": True, "backend": "github", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


class NpmSearch(SearchEngine):
    """NPM 包搜索 - JavaScript/Node.js"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            url = f"https://registry.npmjs.org/-/v1/search?text={urllib.parse.quote(query)}&size={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "OpenClaw/1.0")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("objects", []):
                pkg = item.get("package", {})
                results.append({
                    "title": pkg.get("name", ""),
                    "url": pkg.get("links", {}).get("npm", ""),
                    "snippet": pkg.get("description", ""),
                    "version": pkg.get("version", ""),
                    "source": "npm"
                })
            
            return {"success": True, "backend": "npm", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


class PyPISearch(SearchEngine):
    """PyPI 包搜索 - Python"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            url = f"https://pypi.org/pypi/{urllib.parse.quote(query)}/json"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "OpenClaw/1.0")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            info = data.get("info", {})
            results = [{
                "title": info.get("name", ""),
                "url": info.get("project_url", ""),
                "snippet": info.get("summary", ""),
                "version": info.get("version", ""),
                "source": "pypi"
            }]
            
            return {"success": True, "backend": "pypi", "results": results}
        except Exception as e:
            # 如果直接搜索失败，尝试搜索页面
            return {"success": False, "error": str(e)}


class StackOverflowSearch(SearchEngine):
    """Stack Overflow 搜索 - 程序员问答"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            # Stack Exchange API
            url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={urllib.parse.quote(query)}&site=stackoverflow&pagesize={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "OpenClaw/1.0")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title", "").replace("&quot;", '"').replace("&amp;", "&"),
                    "url": item.get("link", ""),
                    "snippet": f"Score: {item.get('score', 0)}, Answers: {item.get('answer_count', 0)}",
                    "source": "stackoverflow"
                })
            
            return {"success": True, "backend": "stackoverflow", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


class RedditSearch(SearchEngine):
    """Reddit 搜索 - 社区讨论"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            # Reddit JSON API（无需认证，只读）
            url = f"https://www.reddit.com/search.json?q={urllib.parse.quote(query)}&limit={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 OpenClaw/1.0")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for post in data.get("data", {}).get("children", []):
                item = post.get("data", {})
                results.append({
                    "title": item.get("title", ""),
                    "url": f"https://www.reddit.com{item.get('permalink', '')}",
                    "snippet": item.get("selftext", "")[:200],
                    "subreddit": item.get("subreddit", ""),
                    "source": "reddit"
                })
            
            return {"success": True, "backend": "reddit", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==================== 国内搜索引擎 ====================

class BaiduBaikeSearch(SearchEngine):
    """百度百科搜索"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            # 百度百科API
            url = f"https://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key={urllib.parse.quote(query)}&bk_length=600"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            req.add_header("Referer", "https://baike.baidu.com/")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            if data.get("key"):
                results = [{
                    "title": data.get("key", ""),
                    "url": f"https://baike.baidu.com/item/{urllib.parse.quote(query)}",
                    "snippet": data.get("desc", "")[:200],
                    "source": "baidu-baike"
                }]
                return {"success": True, "backend": "baidu-baike", "results": results}
            else:
                return {"success": False, "error": "No results found"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ZhihuSearch(SearchEngine):
    """知乎搜索 - 中文问答"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            # 知乎搜索API（模拟）
            url = f"https://www.zhihu.com/api/v4/search_v3?t=general&q={urllib.parse.quote(query)}&correction=1&offset=0&limit={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            req.add_header("Referer", "https://www.zhihu.com/search?type=content")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data.get("data", []):
                if item.get("type") == "search_result":
                    obj = item.get("object", {})
                    results.append({
                        "title": obj.get("title", "").replace("<em>", "").replace("</em>", ""),
                        "url": obj.get("url", ""),
                        "snippet": obj.get("excerpt", "").replace("<em>", "").replace("</em>", "")[:200],
                        "source": "zhihu"
                    })
            
            return {"success": True, "backend": "zhihu", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GiteeSearch(SearchEngine):
    """Gitee 码云搜索 - 国内GitHub"""
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        try:
            url = f"https://gitee.com/api/v5/search/repositories?q={urllib.parse.quote(query)}&sort=stars_count&order=desc&page=1&per_page={max_results}"
            
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "OpenClaw/1.0")
            
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            results = []
            for item in data:
                results.append({
                    "title": item.get("full_name", ""),
                    "url": item.get("html_url", ""),
                    "snippet": item.get("description", "") or "No description",
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language", "Unknown"),
                    "source": "gitee"
                })
            
            return {"success": True, "backend": "gitee", "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==================== 元搜索引擎 ====================

class SearXSearch(SearchEngine):
    """SearX 元搜索引擎 - 聚合多个引擎"""
    
    INSTANCES = [
        "search.sapti.me",
        "search.bus-hit.me",
        "searx.fmac.xyz",
    ]
    
    def search(self, query: str, max_results: int = 5) -> Dict:
        for instance in self.INSTANCES:
            try:
                url = f"https://{instance}/search?q={urllib.parse.quote(query)}&format=json"
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                req = urllib.request.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
                
                response = urllib.request.urlopen(req, context=ctx, timeout=15)
                data = json.loads(response.read().decode())
                
                results = []
                for item in data.get("results", [])[:max_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("content", "")[:200],
                        "source": f"searx-{instance}"
                    })
                
                return {"success": True, "backend": f"searx-{instance}", "results": results}
            except Exception:
                continue
        
        return {"success": False, "error": "All SearX instances failed"}


# ==================== 统一入口 ====================

class GlobalSearch:
    """全球搜索引擎统一入口"""
    
    def __init__(self):
        self.engines = {
            # 国外
            "wikipedia-en": WikipediaSearch(),
            "wikipedia-zh": WikipediaChineseSearch(),
            "github": GitHubSearch(),
            "npm": NpmSearch(),
            "pypi": PyPISearch(),
            "stackoverflow": StackOverflowSearch(),
            "reddit": RedditSearch(),
            
            # 国内
            "baidu-baike": BaiduBaikeSearch(),
            "zhihu": ZhihuSearch(),
            "gitee": GiteeSearch(),
            
            # 元搜索
            "searx": SearXSearch(),
        }
    
    def search(self, query: str, engine: str = None, max_results: int = 5) -> Dict:
        """
        全球搜索
        
        Args:
            query: 搜索关键词
            engine: 指定引擎，None则自动选择
            max_results: 最大结果数
        
        Returns:
            搜索结果
        """
        if engine and engine in self.engines:
            return self.engines[engine].search(query, max_results)
        
        # 自动选择引擎（按可靠性排序）
        priority_engines = [
            "wikipedia-zh" if self._is_chinese(query) else "wikipedia-en",
            "github",
            "stackoverflow",
            "baidu-baike",
            "zhihu",
            "gitee",
            "reddit",
            "searx",
        ]
        
        for eng_name in priority_engines:
            result = self.engines[eng_name].search(query, max_results)
            if result.get("success") and result.get("results"):
                result["engine_used"] = eng_name
                return result
        
        return {"success": False, "error": "All search engines failed"}
    
    def _is_chinese(self, text: str) -> bool:
        """检测是否中文查询"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    def list_engines(self) -> List[str]:
        """列出所有可用引擎"""
        return list(self.engines.keys())


# 便捷函数
def search(query: str, engine: str = None, max_results: int = 5) -> Dict:
    """全球搜索入口"""
    searcher = GlobalSearch()
    return searcher.search(query, engine, max_results)


def search_all(query: str, max_results: int = 3) -> Dict:
    """搜索所有引擎，聚合结果"""
    searcher = GlobalSearch()
    all_results = []
    
    # 搜索前5个最可靠的引擎
    priority = ["wikipedia-en", "wikipedia-zh", "github", "stackoverflow", "baidu-baike"]
    
    for eng_name in priority:
        try:
            result = searcher.engines[eng_name].search(query, max_results)
            if result.get("success"):
                for item in result.get("results", [])[:2]:  # 每个引擎取前2条
                    item["engine"] = eng_name
                    all_results.append(item)
        except Exception:
            continue
    
    return {
        "success": len(all_results) > 0,
        "query": query,
        "total_results": len(all_results),
        "results": all_results
    }


if __name__ == "__main__":
    # 测试
    print("Testing Global Search...")
    
    # 测试英文搜索
    print("\n1. Wikipedia EN:")
    r = search("Python programming", engine="wikipedia-en")
    print(f"  Success: {r.get('success')}, Results: {len(r.get('results', []))}")
    
    # 测试中文搜索
    print("\n2. Wikipedia ZH:")
    r = search("人工智能", engine="wikipedia-zh")
    print(f"  Success: {r.get('success')}, Results: {len(r.get('results', []))}")
    
    # 测试GitHub
    print("\n3. GitHub:")
    r = search("machine learning", engine="github")
    print(f"  Success: {r.get('success')}, Results: {len(r.get('results', []))}")
    
    # 测试自动选择
    print("\n4. Auto (中文):")
    r = search("深度学习")
    print(f"  Engine: {r.get('engine_used', 'unknown')}, Success: {r.get('success')}")
    
    print("\nAll engines:", GlobalSearch().list_engines())
