# schemas.py
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(..., description="用户的提问")

class AskResponse(BaseModel):
    answer: str = Field(..., description="大模型结合文档生成的回答")