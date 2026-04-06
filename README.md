# 🚀 FastAPI + LangChain RAG API

这是一个基于 **FastAPI** 和 **LangChain (LCEL架构)** 构建的生产级本地文档问答接口（RAG 微服务）。本项目接入了阿里云通义千问大模型，并使用了针对中文环境优化的本地向量检索方案。

## ✨ 核心特性

* **⚡️ 高性能异步并发：** 完美结合 FastAPI 与 LangChain 的 `ainvoke`，实现非阻塞的高效推理。
* **🧠 先进的 RAG 架构：** 采用 LCEL (LangChain Expression Language) 的并行与透传机制构建检索生成链。
* **✂️ 优化的中文切分：** 使用自定义 `separators` 的 `RecursiveCharacterTextSplitter`，优先按段落、短句切分，最大程度保留语义完整性。
* **📦 模块化设计：** 严格遵循高内聚低耦合原则，将数据模型 (Schemas)、业务逻辑 (Services) 和接口路由 (Main) 彻底分离。
* **🔒 安全的数据验证：** 借助 Pydantic 提供严谨的 API 输入/输出数据校验机制。

## 📁 目录结构规划

```text
RAG_Demo/
├── .env.example          # 环境变量示例文件 (请克隆后复制为 .env)
├── .gitignore            # Git 忽略配置文件 (保护敏感信息与本地环境)
├── main.py               # FastAPI 启动入口与 API 路由层
├── schemas.py            # Pydantic 数据验证模型层
├── rag_service.py        # LangChain 核心 RAG 业务逻辑与向量检索层
├── qwen_utils.py         # 大模型初始化工具箱 (统一模型配置)
└── README.md             # 本说明文档