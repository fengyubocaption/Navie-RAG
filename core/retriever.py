# core/retriever.py
import jieba
from langchain_community.vectorstores import Milvus
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import MultiQueryRetriever, ContextualCompressionRetriever, EnsembleRetriever
from langchain_community.document_compressors import DashScopeRerank
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import settings
from .document_loader import load_and_split_path

# ==========================================
# 全局初始化：秒级启动架构
# ==========================================
print(">>> [检索层] 正在连接持久化向量库与初始化内存词表...")

# 1. 快速加载本地文本 (仅用于喂给纯内存的 BM25，纯本地 I/O 不费 Token)
split_docs = load_and_split_path(settings.DATA_DIR)

# 2. 核心改变：直接实例化连接现有的 Milvus 数据库，而不是每次重建！
embeddings = DashScopeEmbeddings(model="text-embedding-v2")
vectorstore = Milvus(
    embedding_function=embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
    collection_name="rag_collection",
    auto_id=True
)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

# 3. 初始化内存级 BM25
bm25_retriever = BM25Retriever.from_documents(split_docs, preprocess_func=jieba.lcut)
bm25_retriever.k = 6
print(">>> [检索层] 基础双路检索器就绪！(Milvus 直连成功)")

# ==========================================
# 策略工厂函数
# ==========================================
def get_retriever_by_strategy(strategy: str, llm):
    """
    根据策略名称，动态返回组装好的高级检索器
    """
    if strategy == "multi_query":
        return MultiQueryRetriever.from_llm(retriever=vector_retriever, llm=llm)

    elif strategy == "hyde":
        hyde_prompt = ChatPromptTemplate.from_template(
            "你是一个专业的文档撰写助手。请针对用户提出的问题，写一段字数约 200 字的伪造回答。\n要求：使用陈述句，包含专业术语，逻辑自洽。\n\n用户问题: {question}\n伪造回答:"
        )
        hyde_chain = hyde_prompt | llm | StrOutputParser()
        return hyde_chain | vector_retriever

    elif strategy == "hybrid":
        ensemble = EnsembleRetriever(retrievers=[bm25_retriever, vector_retriever], weights=[0.5, 0.5])
        compressor = DashScopeRerank(model="qwen3-vl-rerank", top_n=3)
        return ContextualCompressionRetriever(base_compressor=compressor, base_retriever=ensemble)

    elif strategy == "ultimate":
        ensemble = EnsembleRetriever(retrievers=[bm25_retriever, vector_retriever], weights=[0.4, 0.6])
        mq_hybrid = MultiQueryRetriever.from_llm(retriever=ensemble, llm=llm)
        compressor = DashScopeRerank(model="qwen-reranker", top_n=3)
        return ContextualCompressionRetriever(base_compressor=compressor, base_retriever=mq_hybrid)

    return vector_retriever