# qwen_utils.py
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi

load_dotenv()

def get_qwen_llm(model_name="qwen-max"):
    # 可以在这里添加其他的统一配置参数
    return ChatTongyi(model=model_name)