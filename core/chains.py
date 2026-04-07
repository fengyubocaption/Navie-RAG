# chains.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def format_docs(docs):
    """格式化检索到的文档块"""
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(retriever, llm):
    """
    组装最终的问答链条
    """
    prompt = ChatPromptTemplate.from_template(
        "请严格根据以下背景资料回答问题。如果资料中没有相关信息，请明确回答不知道。\n\n"
        "背景资料:\n{context}\n\n"
        "用户问题: {question}"
    )

    chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return chain