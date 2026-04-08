# core/tools/web_tool.py
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def web_search(query: str) -> str:
    """当用户询问最新的新闻、当前日期、或者本地文档中不存在的通用知识时，使用此工具。"""
    print(f"\n[🛠️ 工具] 正在全网搜索实时信息: '{query}'...")
    search = DuckDuckGoSearchRun()
    try:
        result = search.invoke(query)
        return f"网络搜索结果:\n{result}"
    except Exception as e:
        return f"网络搜索失败: {str(e)}"