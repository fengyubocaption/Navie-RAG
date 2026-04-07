# schemas.py
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(..., description="用户的提问")
    strategy: str = Field("naive", description="RAG 策略，可选: naive, multi_query, hyde, hybrid, ultimate")

class AskResponse(BaseModel):
    answer: str = Field(..., description="大模型结合文档生成的回答")

class IngestRequest(BaseModel):
    target_name: str = Field(..., description="要处理的文件名或文件夹名，例如 \"sample.md\" 或 \"new_folder\"")

class IngestResponse(BaseModel):
    message: str = Field(..., description="处理结果的详细信息")
    chunks_added: int = Field(..., description="成功添加的文档块数量")
