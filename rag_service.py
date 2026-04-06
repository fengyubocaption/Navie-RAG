# rag_service.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
import qwen_utils

print(">>> [系统] 正在初始化 RAG 知识库与检索链...")

# 1. 模拟长文档（后续你可以换成从文件读取）
raw_text = """
# 第一章：LangChain 简介
LangChain 是一个用于构建大语言模型应用的框架。它的核心理念是“链”，通过 LCEL 语言将不同的组件连接起来。

# 第二章：FastAPI 的优势
FastAPI 是一个现代、快速（高性能）的 Web 框架，用于构建 API。
将两者结合，可以极其优雅地把本地的 AI 脚本转化为生产级别的微服务。

# 第三章：高阶技巧
LCEL 天然支持异步操作，与 FastAPI 结合能实现极高的并发能力。
在 RAG 系统中，文档的切分策略至关重要。合理的切分能保留上下文的语义完整性，从而提高向量检索的准确度。
"""

# 2. 使用你刚才学到的高级切分策略
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", "。", "！", "？", ".", "?", "!", " ", ""]
)
texts = text_splitter.split_text(raw_text)

# 3. 初始化向量库和检索器
embeddings = DashScopeEmbeddings(model="text-embedding-v2")
vectorstore = FAISS.from_texts(texts, embeddings)
retriever = vectorstore.as_retriever()

# 4. 初始化模型与 Prompt
llm = qwen_utils.get_qwen_llm()
prompt = ChatPromptTemplate.from_template(
    "请严格根据以下背景资料回答问题。背景资料:\n{context}\n\n用户问题: {question}"
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 5. 组装全局 LCEL 链
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
print(">>> [系统] RAG 核心服务初始化完毕！")

# 6. 对外暴露一个极简的调用接口
async def process_question(question: str) -> str:
    """供 main.py 调用的核心业务函数"""
    return await rag_chain.ainvoke(question)