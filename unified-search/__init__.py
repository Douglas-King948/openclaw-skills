"""
Unified Search - 全球统一搜索引擎
聚合国内外多个搜索源，自动选择最优引擎
"""

from .global_search import (
    GlobalSearch,
    search,
    search_all,
    # 单个引擎类
    WikipediaSearch,
    WikipediaChineseSearch,
    GitHubSearch,
    StackOverflowSearch,
    RedditSearch,
    NpmSearch,
    PyPISearch,
    BaiduBaikeSearch,
    ZhihuSearch,
    GiteeSearch,
    SearXSearch,
)

__version__ = "2.0.0"
__all__ = [
    "GlobalSearch",
    "search",
    "search_all",
    "WikipediaSearch",
    "WikipediaChineseSearch",
    "GitHubSearch",
    "StackOverflowSearch",
    "RedditSearch",
    "NpmSearch",
    "PyPISearch",
    "BaiduBaikeSearch",
    "ZhihuSearch",
    "GiteeSearch",
    "SearXSearch",
]
