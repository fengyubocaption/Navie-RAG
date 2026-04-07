# rag_service.py
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.globals import set_debug

import qwen_utils
from document_loader import load_and_split_document

# 打开debug模式
set_debug(True)

# ==========================================
# 第一部分：全局初始化 (整个服务器生命周期只执行一次)
# ==========================================
print(">>> [系统] 正在初始化 RAG 知识库 (全局构建)...")

# 1. 预先切分文档并构建向量库（启动时一次性花完建库的时间和钱）
split_docs = load_and_split_document("sample.md")
embeddings = DashScopeEmbeddings(model="text-embedding-v2")
vectorstore = FAISS.from_documents(split_docs, embeddings)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. 全局复用的大模型和 Prompt
llm = qwen_utils.get_qwen_llm()
prompt = ChatPromptTemplate.from_template(
    "请严格根据以下背景资料回答问题。如果资料中没有相关信息，请明确回答不知道。\n\n背景资料:\n{context}\n\n用户问题: {question}"
)

print(">>> [系统] 基础组件初始化完毕！")


# ==========================================
# 第二部分：策略工厂函数
# ==========================================
def create_multi_query_retriever(llm, base_retriever):
    return MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm)


def create_hyde_retriever(llm, base_retriever):
    hyde_prompt = ChatPromptTemplate.from_template(
        """你是一个专业的文档撰写助手。请针对用户提出的问题，写一段字数约 200 字的伪造回答。
        要求：使用陈述句，包含专业术语，逻辑自洽。

        用户问题: {question}
        伪造回答:"""
    )
    hyde_chain = hyde_prompt | llm | StrOutputParser()
    return hyde_chain | base_retriever


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# ==========================================
# 第三部分：核心业务调用 (每次 API 请求都会执行)
# ==========================================
async def process_question(question: str, strategy: str = "naive") -> str:
    """
    接收每次用户的提问，根据策略动态组装轻量级的 LCEL 链并执行。
    """
    # 1. 根据传入的策略，动态选择检索器（复用全局的 base_retriever）
    if strategy == "multi_query":
        current_retriever = create_multi_query_retriever(llm, base_retriever)
    elif strategy == "hyde":
        current_retriever = create_hyde_retriever(llm, base_retriever)
    else:
        current_retriever = base_retriever

    # 2. 动态组装 RAG 链条
    chain = (
            {"context": current_retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    # 3. 真正执行发问请求
    return await chain.ainvoke(question)