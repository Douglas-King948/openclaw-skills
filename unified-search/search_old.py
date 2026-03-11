"""
Unified Search - 统一搜索引擎
聚合 DuckDuckGo、Tavily、Brave 多个后端，自动故障转移
"""

import asyncio
import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("unified-search")


@dataclass
class SearchResult:
    """统一搜索结果格式"""
    title: str
    url: str
    snippet: str
    source: str
    score: float = 0.0


class SearchBackend(ABC):
    """搜索后端抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = True
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """执行搜索，返回结果列表"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查后端是否可用"""
        pass


class DuckDuckGoBackend(SearchBackend):
    """DuckDuckGo搜索后端 - 使用requests直接搜索"""

    def __init__(self):
        super().__init__("DuckDuckGo")

    def is_available(self) -> bool:
        return True

    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        try:
            import requests
            from bs4 import BeautifulSoup

            # 使用 requests 直接搜索 DuckDuckGo
            url = f'https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers))

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []

                # 查找搜索结果
                for result in soup.find_all('div', class_='result')[:max_results]:
                    title = result.find('h2').get_text(strip=True) if result.find('h2') else ''
                    href = result.find('a', class_='result__a')['href'] if result.find('a', class_='result__a') else ''
                    snippet = result.find('a', class_='result__snippet').get_text(strip=True) if result.find('a', class_='result__snippet') else ''

                    if title and href:
                        results.append(
                            SearchResult(
                                title=title,
                                url=href,
                                snippet=snippet,
                                source=self.name
                            )
                        )

                logger.info(f'📦 DuckDuckGo found {len(results)} results')
                return results
            else:
                logger.warning(f'DuckDuckGo HTTP error: {response.status_code}')
                return []

        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")
            import traceback
            logger.warning(traceback.format_exc())
            return []


class TavilyBackend(SearchBackend):
    """Tavily搜索后端 - 高质量，1000次/月免费"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("Tavily")
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
    
    def is_available(self) -> bool:
        return self.api_key is not None
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        if not self.api_key:
            return []
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "max_results": max_results,
                        "include_answer": False
                    },
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status != 200:
                        logger.warning(f"Tavily API error: {resp.status}")
                        return []
                    
                    data = await resp.json()
                    results = data.get("results", [])
                    
                    return [
                        SearchResult(
                            title=r.get("title", ""),
                            url=r.get("url", ""),
                            snippet=r.get("content", ""),
                            source=self.name,
                            score=r.get("score", 0.0)
                        )
                        for r in results
                    ]
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}")
            return []


class BraveBackend(SearchBackend):
    """Brave搜索后端 - 2000次/月免费"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("Brave")
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
    
    def is_available(self) -> bool:
        return self.api_key is not None
    
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        if not self.api_key:
            return []
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers={"X-Subscription-Token": self.api_key},
                    params={"q": query, "count": max_results},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status != 200:
                        logger.warning(f"Brave API error: {resp.status}")
                        return []
                    
                    data = await resp.json()
                    results = data.get("web", {}).get("results", [])
                    
                    return [
                        SearchResult(
                            title=r.get("title", ""),
                            url=r.get("url", ""),
                            snippet=r.get("description", ""),
                            source=self.name
                        )
                        for r in results
                    ]
        except Exception as e:
            logger.warning(f"Brave search failed: {e}")
            return []


class KimiNativeBackend(SearchBackend):
    """Kimi 原生搜索后端 - 已删除，保留为占位符"""

    def __init__(self):
        super().__init__("Kimi Native")
        self.available = False
        logger.warning("Kimi Native search backend not available - skill was removed")

    def is_available(self) -> bool:
        return self.available

    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        logger.warning("Kimi Native search is not available")
        return []


class MultiSearchEngineBackend(SearchBackend):
    """多搜索引擎后端 - 已删除，保留为占位符"""

    def __init__(self):
        super().__init__("Multi Search Engine")
        self.available = False
        logger.warning("Multi Search Engine backend not available - skill was removed")

    def is_available(self) -> bool:
        return self.available

    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        logger.warning("Multi Search Engine is not available")
        return []


class UnifiedSearch:
    """统一搜索引擎主类"""

    def __init__(self):
        self.backends: List[SearchBackend] = [
            DuckDuckGoBackend(),  # 免费，优先
            TavilyBackend(),      # 高质量
            BraveBackend(),       # 备用
            KimiNativeBackend(),  # Kimi 原生搜索
            MultiSearchEngineBackend(),  # 多搜索引擎
        ]
        
        # 检查可用后端
        self.available_backends = [b for b in self.backends if b.is_available()]
        logger.info(f"Available backends: {[b.name for b in self.available_backends]}")
    
    async def search(
        self,
        query: str,
        backend: Optional[str] = None,
        mode: str = "auto",
        max_results: int = 10,
        timeout: float = 15.0
    ) -> Dict[str, Any]:
        """
        执行统一搜索
        
        Args:
            query: 搜索关键词
            backend: 指定后端名称 (ddg/tavily/brave)
            mode: 搜索模式 (auto/fast/deep)
            max_results: 最大结果数
            timeout: 超时时间（秒）
        """
        
        if not query.strip():
            return {
                "success": False,
                "query": query,
                "results": [],
                "backend_used": "",
                "error": "Empty query"
            }
        
        # 选择后端
        selected_backends = self._select_backends(backend, mode)
        
        if not selected_backends:
            return {
                "success": False,
                "query": query,
                "results": [],
                "backend_used": "",
                "error": "No search backend available"
            }
        
        # 尝试每个后端，直到成功
        for backend in selected_backends:
            try:
                logger.info(f"Trying search with {backend.name}...")
                
                results = await asyncio.wait_for(
                    backend.search(query, max_results),
                    timeout=timeout
                )
                
                if results:
                    logger.info(f"Search successful with {backend.name}, got {len(results)} results")
                    return {
                        "success": True,
                        "query": query,
                        "results": [
                            {
                                "title": r.title,
                                "url": r.url,
                                "snippet": r.snippet,
                                "source": r.source
                            }
                            for r in results
                        ],
                        "backend_used": backend.name,
                        "total_results": len(results)
                    }
                
            except asyncio.TimeoutError:
                logger.warning(f"{backend.name} search timeout")
            except Exception as e:
                logger.warning(f"{backend.name} search error: {e}")
        
        # 所有后端都失败了
        return {
            "success": False,
            "query": query,
            "results": [],
            "backend_used": "",
            "error": "All search backends failed"
        }
    
    def _select_backends(self, backend_name: Optional[str], mode: str) -> List[SearchBackend]:
        """选择要使用的后端"""

        # 如果指定了后端
        if backend_name:
            backend_name = backend_name.lower()
            # 支持简写名称
            name_map = {
                'ddg': 'duckduckgo',
                'duckduckgo': 'duckduckgo',
                'kimi': 'kimi native',
                'kimi native': 'kimi native',
                'multi': 'multi search engine',
                'multi search engine': 'multi search engine',
                'tavily': 'tavily',
                'brave': 'brave'
            }

            target_name = name_map.get(backend_name, backend_name)

            for b in self.available_backends:
                if b.name.lower().replace(" ", "") == target_name.replace(" ", ""):
                    return [b]
            logger.warning(f"Specified backend '{backend_name}' not available")

        # 根据模式选择
        if mode == "fast":
            # 最快优先（DDG）
            return sorted(
                self.available_backends,
                key=lambda b: 0 if b.name == "DuckDuckGo" else 1
            )

        elif mode == "deep":
            # 质量优先（Tavily > Brave > Kimi > DDG > Multi）
            priority = {"Tavily": 0, "Brave": 1, "Kimi Native": 2, "DuckDuckGo": 3, "Multi Search Engine": 4}
            return sorted(
                self.available_backends,
                key=lambda b: priority.get(b.name, 99)
            )

        # auto 模式：默认顺序
        return self.available_backends
    
    def get_status(self) -> Dict:
        """获取搜索系统状态"""
        return {
            "backends": [
                {
                    "name": b.name,
                    "available": b.is_available(),
                    "enabled": b.enabled
                }
                for b in self.backends
            ],
            "available_count": len(self.available_backends)
        }


# 同步版本
def search_sync(
    query: str,
    backend: Optional[str] = None,
    mode: str = "auto",
    max_results: int = 10
) -> Dict[str, Any]:
    """
    同步搜索函数（简化版）

    Args:
        query: 搜索关键词
        backend: 指定后端名称 (ddg/tavily/brave/kimi/multi)
        mode: 搜索模式 (auto/fast/deep)
        max_results: 最大结果数

    Returns:
        搜索结果字典
    """
    try:
        return asyncio.run(search(query, backend, mode, max_results))
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return {
            "success": False,
            "query": query,
            "results": [],
            "backend_used": "",
            "error": str(e)
        }


# 全局实例
_search_engine = None

def get_search_engine() -> UnifiedSearch:
    """获取搜索引擎实例（单例）"""
    global _search_engine
    if _search_engine is None:
        _search_engine = UnifiedSearch()
    return _search_engine


# 便捷函数
async def search(
    query: str,
    backend: Optional[str] = None,
    mode: str = "auto",
    max_results: int = 10
) -> Dict[str, Any]:
    """
    便捷搜索函数
    
    示例:
        result = await search("OpenClaw 最新版本")
        for r in result["results"]:
            print(f"{r['title']}: {r['url']}")
    """
    engine = get_search_engine()
    return await engine.search(query, backend, mode, max_results)


__all__ = ['search', 'get_search_engine', 'UnifiedSearch', 'SearchResult']
