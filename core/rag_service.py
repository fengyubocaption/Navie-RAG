# rag_service.py
import os

from . import qwen_utils
from .chains import build_rag_chain
from .document_loader import load_and_split_path
from .retriever import vectorstore, get_retriever_by_strategy
from config import settings


# 全局初始化一次 LLM
llm = qwen_utils.get_qwen_llm()


async def process_question(question: str, strategy: str = "naive") -> str:
    """
    业务入口：接收提问 -> 拿检索器 -> 组装链条 -> 执行解答
    """
    # 1. 拿工具：根据用户策略获取对应的检索器
    retriever = get_retriever_by_strategy(strategy, llm)

    # 2. 上流水线：组装完整的 RAG 处理链
    chain = build_rag_chain(retriever, llm)

    # 3. 按下开关：开始执行
    return await chain.ainvoke(question)


async def ingest_knowledge(target_name: str) -> int:
    """
    接收文件名或目录名，切分并追加写入向量数据库
    """
    # 1. 拼接绝对路径（默认去 file 目录下找）
    target_path = os.path.join(settings.FILE_DIR, target_name)

    # 2. 加载并切分文档
    docs = load_and_split_path(target_path)

    # 3. 追加存入 Milvus 持久化数据库
    print(f">>> [检索层] 正在将 {len(docs)} 个文本块追加写入 Milvus...")
    vectorstore.add_documents(docs)
    print(">>> [检索层] 写入完成！")

    # 注意：这里 Milvus 的数据已经实时更新了，向量检索立刻生效。
    # 但内存中的 BM25 需要重启服务才能重新统计词频。

    return len(docs)