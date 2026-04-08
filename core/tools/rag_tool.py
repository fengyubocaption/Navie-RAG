# core/tools/rag_tool.py
from langchain_core.tools import tool
from core import qwen_utils
from core.retriever import get_retriever_by_strategy

# 共享 LLM 实例
llm = qwen_utils.get_qwen_llm()


@tool
def search_local_files(query: str) -> str:
    """当用户询问关于公司内部文档、技术方案或已上传的私有资料时，必须使用此工具。"""
    print(f"\n[🛠️ 工具] 正在调用本地 RAG 检索: '{query}'...")

    # 复用你最强的 ultimate 检索策略
    retriever = get_retriever_by_strategy("ultimate", llm)
    docs = retriever.invoke(query)

    if not docs:
        return "本地知识库中未找到相关内容。"

    # 格式化输出，方便 Agent 阅读
    context = "\n\n".join([f"文档片段:\n{doc.page_content}" for doc in docs])
    return f"本地检索结果:\n{context}"