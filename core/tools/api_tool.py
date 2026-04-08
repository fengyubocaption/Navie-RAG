# core/tools/api_tool.py
import requests
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class UserQueryInput(BaseModel):
    user_id: int = Field(..., description="用户的唯一数字 ID，例如 1, 2, 3")


@tool(args_schema=UserQueryInput)
def fetch_external_user_profile(user_id: int) -> str:
    """当需要获取远端系统用户的详细资料（如邮箱、公司名称、电话）时，调用此 API 工具。"""
    print(f"\n[🛠️ 工具] 正在通过 API 获取 ID={user_id} 的用户资料...")
    try:
        url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            # 清洗数据，只给 Agent 返回最有用的信息
            summary = (
                f"姓名: {data.get('name')}\n"
                f"邮箱: {data.get('email')}\n"
                f"公司: {data['company'].get('name')}\n"
                f"城市: {data['address'].get('city')}"
            )
            return summary
        return f"未找到 ID 为 {user_id} 的用户。"
    except Exception as e:
        return f"API 调用报错: {str(e)}"