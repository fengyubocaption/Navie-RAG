# core/document_loader.py
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_path(target_path: str):
    """
    通用加载器：支持传入单文件路径，或文件夹路径
    """
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"找不到指定路径: {target_path}")

    all_documents = []
    print(f">>> [数据层] 开始解析路径: {target_path}")

    # 1. 统一收集要处理的文件路径
    files_to_process = []
    if os.path.isfile(target_path):
        files_to_process.append(target_path)
    else:
        for root, _, files in os.walk(target_path):
            for file in files:
                files_to_process.append(os.path.join(root, file))

    # 2. 遍历加载
    for file_path in files_to_process:
        file_extension = os.path.splitext(file_path)[1].lower()
        try:
            if file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_extension == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
            elif file_extension == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")
            else:
                print(f"  [跳过] 不支持的文件: {file_path}")
                continue

            docs = loader.load()
            all_documents.extend(docs)
            print(f"  [成功] 已加载: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  [失败] 无法解析 {file_path}, 错误: {str(e)}")

    if not all_documents:
        raise ValueError(f"在 {target_path} 中没有找到任何支持提取的文本！")

    # 3. 统一语义切分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100,
        separators=["\n\n", "\n", "。", "！", "？", ".", "?", "!", " ", ""]
    )
    split_docs = text_splitter.split_documents(all_documents)
    print(f">>> [数据层] 切分完毕，共产生 {len(split_docs)} 个文本块。")

    return split_docs