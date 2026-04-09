# locustfile.py
import json
import random
import string
from locust import HttpUser, task, between


def generate_random_session_id():
    """生成随机的会话ID，防止所有并发用户共享同一个记忆"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class AgentStressTestUser(HttpUser):
    # 每个用户在发出下一次请求前，等待 1 到 5 秒（模拟人类思考时间）
    wait_time = between(1, 5)

    def on_start(self):
        """每个虚拟用户启动时执行一次"""
        self.session_id = f"locust_user_{generate_random_session_id()}"
        # 预设几个典型的 RAG/Agent 问题
        self.questions = [
            "上海今天天气怎么样？",
            "请总结一下本地文档里关于大模型检索优化的内容。"
        ]

    @task
    def test_research_endpoint(self):
        """核心压测任务"""
        payload = {
            "question": random.choice(self.questions),
            "session_id": self.session_id
        }

        # 这里的 catch_response=True 允许我们自定义什么时候算“失败”
        with self.client.post(
                "/api/research",
                json=payload,
                timeout=30,  # LLM 响应可能很慢，设置较长的超时时间
                catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")