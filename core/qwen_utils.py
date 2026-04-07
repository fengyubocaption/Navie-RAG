# qwen_utils.py
import os
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi

from config.settings import BASE_DIR


load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_qwen_llm(model_name="qwen-max"):
    # 可以在这里添加其他的统一配置参数
    return ChatTongyi(model=model_name)