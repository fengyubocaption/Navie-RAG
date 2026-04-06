# document_loader.py
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_document(file_path: str):
    """
    通用文档加载器：支持 PDF, TXT, MD 格式
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到文件: {file_path}")

    # 1. 根据后缀名选择对应的加载器
    file_extension = os.path.splitext(file_path)[1].lower()

    print(f">>> [数据层] 正在检测文件类型: {file_extension}")

    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension == ".md":
        loader = UnstructuredMarkdownLoader(file_path)
    elif file_extension == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"暂时不支持的文件格式: {file_extension}")

    # 2. 执行加载
    documents = loader.load()
    print(f">>> [数据层] 已加载来自 {file_path} 的内容")

    # 3. 语义切分 (针对不同格式通用的高级配置)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", "！", "？", ".", "?", "!", " ", ""]
    )

    split_docs = text_splitter.split_documents(documents)
    print(f">>> [数据层] 文档切分完毕，共产生 {len(split_docs)} 个文本块。")

    return split_docs