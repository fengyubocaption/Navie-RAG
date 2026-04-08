# main.py
from fastapi import FastAPI, HTTPException
import uvicorn

from core.schemas import (
    AskRequest, AskResponse,
    IngestRequest, IngestResponse,
    ResearchRequest, ResearchResponse
)
from core.rag_service import process_question, ingest_knowledge
from core.agent import run_research_agent

app = FastAPI(
    title="LangChain RAG & Agent API",
    description="企业级本地知识库与智能研究助手接口",
    version="2.0.0"
)

# 基础问答接口
@app.post("/api/ask", response_model=AskResponse, tags=["1. RAG 本地问答"])
async def ask_rag(request: AskRequest):
    """
    标准 RAG 接口：仅依赖本地私有知识库进行解答，处理速度快。
    """
    try:
        answer = await process_question(request.question, request.strategy)
        return AskResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG 处理异常: {str(e)}")


# 知识库管理接口
@app.post("/api/ingest", response_model=IngestResponse, tags=["2. 知识库管理"])
async def ingest_docs(request: IngestRequest):
    """
    动态入库接口：将 file 目录下的指定文件或文件夹切分并存入 Milvus 向量库。
    """
    try:
        chunks_count = await ingest_knowledge(request.target_name)
        return IngestResponse(
            message=f"入库成功！[{request.target_name}] 已存入向量网络。",
            chunks_added=chunks_count
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"未找到目标文件: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"入库处理异常: {str(e)}")


# 智能体助手接口
@app.post("/api/research", response_model=ResearchResponse, tags=["3. Agent 智能体"])
async def ask_agent(request: ResearchRequest):
    """
    高级智能体接口：自动感知上下文，按需路由调用本地 RAG 工具或全网搜索引擎。
    """
    try:
        answer = await run_research_agent(request.question)
        return ResearchResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent 执行异常: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8888)