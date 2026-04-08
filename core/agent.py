# core/agent.py
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage

from core import qwen_utils
from core.tools import AGENT_TOOLS

llm = qwen_utils.get_qwen_llm()


async def run_research_agent(question: str) -> str:
    """
    组装并运行研究助手 Agent，返回最终综合解答
    """
    system_msg = SystemMessage(
        "你是一个高级研究分析师。任务是综合本地私有文档和互联网信息来回答问题。\n"
        "【决策逻辑】\n"
        "1. 若问题偏向私有知识，优先调用 search_local_files。\n"
        "2. 若问题涉及外部时效性事实，调用 web_search。\n"
        "3. 若需对比，可依次调用两者。\n"
        "【输出要求】\n"
        "务必在回答末尾明确标注信息来源，例如：[来源：本地文档] 或 [来源：网络搜索]。"
    )

    agent = create_agent(model=llm, tools=AGENT_TOOLS)
    inputs = {"messages": [system_msg, HumanMessage(question)]}

    print(f">>> [业务层] 研究助手启动，目标任务: {question}")

    # 注意：API 接口通常需要直接返回完整结果，所以这里用 invoke 而不是 stream
    response = await agent.ainvoke(inputs)

    # 从状态机最后一条消息中提取大模型的最终回答
    final_answer = response["messages"][-1].content
    return final_answer