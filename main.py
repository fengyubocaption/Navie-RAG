# main.py
from fastapi import FastAPI, HTTPException
import uvicorn

from core.schemas import AskRequest, AskResponse, IngestRequest, IngestResponse
from core.rag_service import process_question, ingest_knowledge

app = FastAPI(title="LangChain RAG API", description="模块化的本地文档问答接口")


@app.post("/api/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    接收用户提问，调用 RAG 业务层处理，返回结果。
    """
    try:
        answer = await process_question(request.question, request.strategy)
        return AskResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部处理错误: {str(e)}")


@app.post("/api/ingest", response_model=IngestResponse)
async def api_ingest_file(request: IngestRequest):
    """
    动态数据入库接口：传入 file 目录下的文件名或文件夹名，将其切分并存入数据库。
    """
    try:
        chunks_count = await ingest_knowledge(request.target_name)
        return IngestResponse(
            message=f"入库成功！已将 {request.target_name} 解析并存入数据库。",
            chunks_added=chunks_count
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"入库处理错误: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8888)