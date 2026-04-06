# main.py
from fastapi import FastAPI, HTTPException
import uvicorn

from schemas import AskRequest, AskResponse
from rag_service import process_question

app = FastAPI(title="LangChain RAG API", description="模块化的本地文档问答接口")


@app.post("/api/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    接收用户提问，调用 RAG 业务层处理，返回结果。
    """
    try:
        # FastAPI 这一层根本不关心 LangChain 的细节，直接要结果
        answer = await process_question(request.question)
        return AskResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部处理错误: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)