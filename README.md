# 🚀 企业级 RAG 知识问答微服务 (FastAPI + LangChain)

这是一个基于检索增强生成 (RAG) 技术的智能问答 API 服务。它能够读取本地的多格式文档，构建私有知识库，并利用大语言模型提供精准、具有上下文依据的问答能力。

## ✨ 核心特性

* **🤖 强力大模型接入**：底层集成通义千问 (Qwen) 大语言模型与高质量文本向量化模型。
* **📚 多模态文档解析**：支持 `.pdf`、`.md`、`.txt` 等多种本地文件格式的自动加载与语义切分。
* **⚡ 高性能异步 API**：基于 FastAPI 构建，天然支持异步非阻塞调用，自带 Swagger 交互式接口文档。
* **🧠 极速向量检索**：采用 FAISS 内存级向量数据库，实现毫秒级相似度检索。
* **🐳 现代化容器部署**：提供完整的 `Dockerfile` 与 `docker-compose.yml`，支持一键云原生部署。
* **🧩 优雅的代码解耦**：采用经典的分层架构设计（路由层、业务层、数据访问层、模型层）。

---

## 📂 项目结构

```text
├── main.py                # FastAPI 路由主入口
├── rag_service.py         # RAG 核心业务逻辑层 (大模型调度、检索链 LCEL)
├── document_loader.py     # 数据加载层 (PDF/MD/TXT 解析与文本切分)
├── schemas.py             # 数据校验层 (Pydantic 请求与响应模型)
├── qwen_utils.py          # LLM 工具类 (处理通义千问 API 鉴权与初始化)
├── test_loader.py         # 独立的文档切分测试脚本
├── requirements.txt       # 项目核心依赖清单
├── Dockerfile             # 容器构建指令文件
├── docker-compose.yml     # 容器编排配置文件
└── .dockerignore          # Docker 构建黑名单
```

## 🐳 快速启动 (Docker 部署) **推荐**

使用 Docker Compose 是运行本项目最优雅、最省心的方式。你不需要在本地安装配置任何 Python 环境，只需两步即可将完整的 RAG 微服务部署就绪。

### 第一步：配置环境变量 (API Key)
在项目的根目录下新建一个名为 `.env` 的文件，并将你的大模型 API 密钥填入其中。

```ini
# .env 文件内容示例
DASHSCOPE_API_KEY=sk-你的真实通义千问API密钥
```

### 第二步：一键构建与启动

```ini
docker compose up -d
```