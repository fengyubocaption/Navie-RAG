# schemas.py
from pydantic import BaseModel, Field

# ==========================================
# 1. 基础问答 (RAG)
# ==========================================
class AskRequest(BaseModel):
    question: str = Field(..., description="用户的提问内容", examples=["DeepSeek-V3 的核心架构是什么？"])
    strategy: str = Field(
        default="naive",
        description="检索策略。可选: naive, multi_query, hyde, hybrid, ultimate"
    )

class AskResponse(BaseModel):
    answer: str = Field(..., description="大模型结合本地私有知识库生成的最终回答")


# ==========================================
# 2. 知识库管理 (Ingest)
# ==========================================
class IngestRequest(BaseModel):
    target_name: str = Field(..., description="目标文件名或文件夹名", examples=["sample.md", "new_folder"])

class IngestResponse(BaseModel):
    message: str = Field(..., description="执行结果的提示信息")
    chunks_added: int = Field(..., description="成功切分并添加入库的文本块数量")


# ==========================================
# 3. Agent 智能研究 (Research)
# ==========================================
class ResearchRequest(BaseModel):
    question: str = Field(..., description="需要综合调研的复杂问题", examples=["对比一下本地文档中的指标和网上的最新评价。"])

class ResearchResponse(BaseModel):
    answer: str = Field(..., description="Agent 综合多方工具给出的深度研究报告")