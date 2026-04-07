# 进阶 RAG 架构与工业级生产实践指南

## 一、 RAG 系统的演进路径
检索增强生成（RAG）已经从最初的 Naive 模式演进到了 Modular RAG 阶段。Naive RAG 主要依赖简单的“检索-生成”循环，而 Advanced RAG 引入了预检索处理（Pre-retrieval）和后检索处理（Post-retrieval）。

### 1.1 检索前的查询转换 (Query Transformation)
查询转换的核心在于解决用户提问与文档语义不匹配的问题。常见策略包括：
- **Multi-Query**: 使用 LLM 生成多个视角的变体问题。
- **HyDE (Hypothetical Document Embeddings)**: 生成假设性回答，利用“回答对回答”的相似度提升召回率。
- **Step-back Prompting**: 从具体问题回退到更抽象的概念，获取背景知识。

### 1.2 检索后的漏斗过滤
在检索到 Top-K 个文档块后，系统通常会经过一个“重排序（Rerank）”过程。Rerank 模型（如 gte-rerank 或 BGE-Reranker）会计算 Query 与每一个 Document 的精细匹配得分。这解决了向量检索虽然快但不够精准的问题。

---

## 二、 向量数据库深度对比：FAISS vs Milvus vs Pinecone

在选择向量数据库时，开发者需要权衡可扩展性、延迟和成本。

| 特性 | FAISS | Milvus | Pinecone |
| :--- | :--- | :--- | :--- |
| **持久化** | 需手动 save_local | 原生支持分布式存储 | 全托管云服务 |
| **并发能力** | 较低（内存型） | 极高（分布式架构） | 极高 |
| **算法支持** | HNSW, IVF, Flat | HNSW, DiskANN, IVF | 优化版 HNSW |
| **适用场景** | 个人项目、单机演示 | 企业级海量数据、高并发 | 快速上手、免运维 |

### 2.1 索引算法 HNSW 的原理
HNSW (Hierarchical Navigable Small World) 是目前最主流的向量索引算法。它通过构建多层图结构，实现了在海量高维向量空间中的对数级时间复杂度查找。相比于传统的 IVF（倒排文件索引），HNSW 在内存占用上较高，但检索速度和精度达到了最佳平衡。

---

## 三、 混合检索 (Hybrid Search) 的必要性

### 3.1 词义与字面的博弈
向量检索（Dense Retrieval）基于语义，能理解“苹果”和“水果”的关系；但它对“型号”、“专有名词”、“错误码”极不敏感。例如，搜“Error_Code_502”时，向量检索可能找回一堆关于“网络连接异常”的文字，却漏掉了记录该具体代码的文档。

### 3.2 BM25 算法的角色
BM25 是一种基于词频（TF）和逆文档频率（IDF）的经典评分算法。在混合检索中，BM25 负责捕捉关键词的精确匹配。通过 RRF (Reciprocal Rank Fusion) 算法，我们可以将向量分数和 BM25 分数融合，确保召回结果既有深度（语义）又有精度（字面）。

---

## 四、 RAG 系统评估标准：RAGAs 框架

没有评估，就没有优化。RAGAs 提出了四个核心指标：
1. **Faithfulness (忠实度)**: 回答是否严格来源于检索到的 Context？防止模型产生幻觉。
2. **Answer Relevancy (回答相关性)**: 回答是否真正解决了用户的 Question？
3. **Context Precision (检索精度)**: 检索到的 Top-K 文档里，有用的信息占比多少？
4. **Context Recall (检索召回率)**: 正确答案所需的关键点，是否都在检索结果中？

---

## 五、 部署与性能调优技巧

### 5.1 Docker 容器化最佳实践
在部署 FastAPI + LangChain 应用时，应利用 Docker 的多阶段构建（Multi-stage Build）来减小镜像体积。基础镜像建议使用 `python:3.10-slim`。

### 5.2 并发处理与异步 IO
由于 RAG 系统涉及多次网络 IO（调用 Embedding API、数据库查询、调用 LLM），必须使用 Python 的 `async/await` 机制。使用 `uvicorn` 时，建议调整 `--workers` 参数以匹配 CPU 核心数，提升吞吐量。

### 5.3 故障码参考手册 (示例数据)
- **ERR_001**: API 密钥无效或过期。
- **ERR_002**: 向量数据库连接超时，请检查 Docker 网络设置。
- **ERR_003**: 输入文本超过 Embedding 模型最大长度限制（通常为 512 或 1024 tokens）。