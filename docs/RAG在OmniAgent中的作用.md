# RAG 在 OmniAgent 项目中的作用 - 完整讲解

## 🎯 什么是 RAG？

**RAG = Retrieval-Augmented Generation（检索增强生成）**

简单说：**让 AI 能够查询你的私有知识库，给出更准确的回答**

---

## 🤔 为什么需要 RAG？

### **问题1：AI 的知识有限**

```
用户：我们公司的请假制度是什么？
AI（没有 RAG）：抱歉，我不知道你们公司的具体制度。

用户：我们公司的请假制度是什么？
AI（有 RAG）：根据公司员工手册，请假制度如下：
              1. 病假：每年10天，需提供医院证明
              2. 年假：工作满1年享有5天年假
              3. 事假：需提前3天申请...
              （从知识库中检索到的内容）
```

### **问题2：AI 的知识会过时**

```
用户：2026年4月的最新产品功能是什么？
AI（没有 RAG）：我的知识截止到2025年8月，无法回答。

用户：2026年4月的最新产品功能是什么？
AI（有 RAG）：根据最新的产品文档，2026年4月新增功能包括：
              1. 智能语音助手
              2. 多模态对话
              3. 自定义工作流...
              （从最新文档中检索）
```

---

## 🔍 RAG 在 OmniAgent 中的完整流程

### **流程图**

```
┌─────────────────────────────────────────────────────────┐
│  第1步：用户上传文档到知识库                             │
│  - PDF、Word、TXT、Markdown 等                          │
│  - 例如：公司员工手册.pdf                                │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第2步：文档解析和分块                                   │
│  - 提取文本内容                                          │
│  - 分割成小块（Chunk），每块约500字                      │
│                                                          │
│  原始文档：                                              │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 员工手册                                          │ │
│  │ 第一章：请假制度                                  │ │
│  │ 1. 病假：每年10天...                              │ │
│  │ 2. 年假：工作满1年...                             │ │
│  │ 第二章：薪资制度                                  │ │
│  │ 1. 基本工资...                                    │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  分块后：                                                │
│  Chunk 1: "第一章：请假制度 1. 病假：每年10天..."       │
│  Chunk 2: "2. 年假：工作满1年享有5天年假..."            │
│  Chunk 3: "第二章：薪资制度 1. 基本工资..."             │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第3步：生成向量嵌入（Embedding）                        │
│  - 将文本转换为数字向量                                  │
│  - 使用 Embedding 模型（如 text-embedding-3-small）     │
│                                                          │
│  Chunk 1: "请假制度 病假每年10天..."                    │
│      ↓                                                   │
│  Vector: [0.23, -0.45, 0.67, 0.12, ...]  (1536维向量)  │
│                                                          │
│  Chunk 2: "年假工作满1年享有5天..."                     │
│      ↓                                                   │
│  Vector: [0.18, -0.52, 0.71, 0.09, ...]                │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第4步：存储到向量数据库                                 │
│  - ChromaDB（本项目使用）                                │
│  - 或 Milvus、Elasticsearch                             │
│                                                          │
│  ChromaDB 数据库：                                       │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Chunk ID │ Content          │ Vector            │ │
│  │ chunk_1  │ "请假制度..."    │ [0.23, -0.45...] │ │
│  │ chunk_2  │ "年假制度..."    │ [0.18, -0.52...] │ │
│  │ chunk_3  │ "薪资制度..."    │ [0.31, -0.28...] │ │
│  └───────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第5步：用户提问                                         │
│  用户：我想请病假，需要什么流程？                        │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第6步：查询重写（Query Rewrite）                        │
│  - 将用户问题改写成多个相关查询                          │
│  - 提高召回率                                            │
│                                                          │
│  原始问题："我想请病假，需要什么流程？"                  │
│      ↓                                                   │
│  重写后：                                                │
│  1. "病假申请流程"                                       │
│  2. "请病假需要什么材料"                                 │
│  3. "病假制度规定"                                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第7步：向量检索（Vector Search）                        │
│  - 将问题转换为向量                                      │
│  - 在向量数据库中搜索相似的文档块                        │
│                                                          │
│  问题向量：[0.25, -0.48, 0.69, 0.11, ...]              │
│      ↓                                                   │
│  计算相似度（余弦相似度）：                              │
│  - chunk_1: 0.92 ← 最相似                               │
│  - chunk_2: 0.75                                        │
│  - chunk_3: 0.31                                        │
│      ↓                                                   │
│  返回 Top 10 最相似的文档块                              │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第8步：重排序（Rerank）                                 │
│  - 使用更精确的模型对检索结果重新排序                    │
│  - 过滤掉不相关的结果                                    │
│                                                          │
│  检索结果（10个）                                        │
│      ↓                                                   │
│  重排序后（按相关性）：                                  │
│  1. "病假制度：每年10天，需提供医院证明..." (0.95)      │
│  2. "病假申请流程：1.填写请假单 2.上传证明..." (0.88)   │
│  3. "年假制度..." (0.45) ← 不相关，过滤掉               │
│      ↓                                                   │
│  保留 Top 3 最相关的结果                                 │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第9步：构建提示词（Prompt）                             │
│  - 将检索到的知识库内容插入到提示词中                    │
│                                                          │
│  系统提示词：                                            │
│  """                                                     │
│  你是一个智能助手，请根据以下知识库内容回答用户问题。   │
│                                                          │
│  知识库内容：                                            │
│  1. 病假制度：每年10天，需提供医院证明...               │
│  2. 病假申请流程：1.填写请假单 2.上传证明...            │
│                                                          │
│  用户问题：我想请病假，需要什么流程？                    │
│                                                          │
│  请基于知识库内容回答，不要编造信息。                    │
│  """                                                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  第10步：AI 生成回答                                     │
│  - 调用大语言模型（通义千问）                            │
│  - 基于知识库内容生成准确回答                            │
│                                                          │
│  AI 回答：                                               │
│  """                                                     │
│  根据公司员工手册，请病假的流程如下：                    │
│                                                          │
│  1. 填写请假申请单                                       │
│  2. 上传医院开具的病假证明                               │
│  3. 提交给直属主管审批                                   │
│  4. 人事部门备案                                         │
│                                                          │
│  注意事项：                                              │
│  - 每年病假额度为10天                                    │
│  - 需提前1天申请（紧急情况除外）                         │
│  - 病假证明需加盖医院公章                                │
│  """                                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 OmniAgent 中的 RAG 实现

### **核心文件**

```
src/backend/agentchat/services/rag/
├── embedding.py        ← 文本向量化
├── vector_db.py        ← 向量数据库操作（ChromaDB）
├── es_client.py        ← 关键词搜索（Elasticsearch）
├── retrieval.py        ← 文档检索
├── rerank.py           ← 结果重排序
├── handler.py          ← RAG 流程编排
└── doc_parser/         ← 文档解析（PDF、Word等）
```

---

### **1. 文档上传和处理**

**前端页面**：`src/frontend/src/pages/knowledge/knowledge.vue`

用户操作：
1. 点击"创建知识库"
2. 上传文档（PDF、Word、TXT 等）
3. 系统自动处理

**后端处理流程**：

```python
# src/backend/agentchat/api/v1/knowledge_file.py

@router.post("/knowledge/file/upload")
async def upload_file(file: UploadFile):
    # 1. 保存文件到 MinIO
    file_url = await minio_client.upload(file)
    
    # 2. 解析文档内容
    text_content = await doc_parser.parse(file)
    
    # 3. 分块（Chunking）
    chunks = text_splitter.split(text_content, chunk_size=500)
    
    # 4. 生成向量嵌入
    embeddings = await get_embedding(chunks)
    
    # 5. 存储到向量数据库
    await milvus_client.insert(knowledge_id, chunks, embeddings)
    
    return {"status": "success"}
```

---

### **2. 向量化（Embedding）**

**代码**：`src/backend/agentchat/services/rag/embedding.py`

```python
from openai import AsyncOpenAI

# 使用 OpenAI 兼容的 Embedding 模型
embedding_client = AsyncOpenAI(
    base_url=app_settings.multi_models.embedding.base_url,
    api_key=app_settings.multi_models.embedding.api_key
)

async def get_embedding(query: str):
    """将文本转换为向量"""
    response = await embedding_client.embeddings.create(
        model="text-embedding-3-small",  # 或其他模型
        input=query
    )
    return response.data[0].embedding  # 返回 1536 维向量
```

**示例**：

```python
# 输入
text = "病假制度：每年10天，需提供医院证明"

# 输出
vector = [0.23, -0.45, 0.67, 0.12, ..., 0.89]  # 1536 个数字
```

---

### **3. 向量数据库存储**

**代码**：`src/backend/agentchat/services/rag/vector_db.py`

```python
import chromadb

class VectorDBClient:
    def __init__(self):
        # 连接 ChromaDB 服务器
        self._client = chromadb.HttpClient(
            host="127.0.0.1",
            port=8000
        )
    
    async def insert(self, collection_name, chunks):
        """插入文档到向量数据库"""
        collection = self._client.get_or_create_collection(collection_name)
        
        # 生成向量
        embeddings = await get_embedding(chunks)
        
        # 存储
        collection.add(
            documents=chunks,      # 原始文本
            embeddings=embeddings, # 向量
            ids=[f"chunk_{i}" for i in range(len(chunks))]
        )
    
    async def search(self, query, knowledge_id):
        """向量检索"""
        collection = self._client.get_collection(knowledge_id)
        
        # 将查询转换为向量
        query_embedding = await get_embedding(query)
        
        # 搜索最相似的文档
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=10  # 返回 Top 10
        )
        
        return results
```

---

### **4. 查询重写**

**代码**：`src/backend/agentchat/services/rewrite/query_write.py`

```python
class QueryRewriter:
    async def rewrite(self, query: str):
        """将用户问题改写成多个相关查询"""
        
        prompt = f"""
        将以下问题改写成3个相关的搜索查询：
        
        原始问题：{query}
        
        改写后的查询（每行一个）：
        """
        
        response = await llm.generate(prompt)
        
        # 解析返回的多个查询
        queries = response.strip().split("\n")
        
        return queries

# 示例
original = "我想请病假，需要什么流程？"
rewritten = [
    "病假申请流程",
    "请病假需要什么材料",
    "病假制度规定"
]
```

---

### **5. 混合检索**

**代码**：`src/backend/agentchat/services/rag/retrieval.py`

```python
class MixRetrival:
    @classmethod
    async def mix_retrival_documents(cls, query_list, knowledges_id):
        """混合检索：向量搜索 + 关键词搜索"""
        
        # 1. 向量搜索（语义相似）
        milvus_docs = []
        for query in query_list:
            docs = await milvus_client.search(query, knowledges_id)
            milvus_docs.extend(docs)
        
        # 2. 关键词搜索（精确匹配）
        es_docs = []
        for query in query_list:
            docs = await es_client.search(query, knowledges_id)
            es_docs.extend(docs)
        
        # 3. 合并结果
        all_docs = milvus_docs + es_docs
        
        # 4. 去重
        unique_docs = remove_duplicates(all_docs)
        
        return unique_docs
```

**为什么要混合检索？**

| 检索方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| 向量搜索 | 理解语义，找相似内容 | 可能漏掉精确关键词 | "请假流程是什么" |
| 关键词搜索 | 精确匹配 | 不理解语义 | "病假10天" |
| 混合检索 | 结合两者优点 | 计算量大 | 最佳实践 |

---

### **6. 重排序（Rerank）**

**代码**：`src/backend/agentchat/services/rag/rerank.py`

```python
class Reranker:
    @classmethod
    async def rerank_documents(cls, query: str, documents: list):
        """使用更精确的模型重新排序"""
        
        # 使用 Rerank 模型计算相关性分数
        scores = []
        for doc in documents:
            score = await rerank_model.score(query, doc)
            scores.append(score)
        
        # 按分数排序
        ranked_docs = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 过滤低分文档
        filtered_docs = [
            doc for doc, score in ranked_docs
            if score >= 0.5  # 阈值
        ]
        
        return filtered_docs
```

---

### **7. RAG 流程编排**

**代码**：`src/backend/agentchat/services/rag/handler.py`

```python
class RagHandler:
    @classmethod
    async def retrieve_ranked_documents(cls, query, knowledge_ids):
        """完整的 RAG 流程"""
        
        # 1. 查询重写
        rewritten_queries = await cls.query_rewrite(query)
        
        # 2. 混合检索
        retrieved_docs = await cls.mix_retrival_documents(
            rewritten_queries,
            knowledge_ids
        )
        
        # 3. 重排序
        reranked_docs = await Reranker.rerank_documents(
            query,
            retrieved_docs
        )
        
        # 4. 过滤和拼接
        top_docs = reranked_docs[:3]  # 取 Top 3
        final_result = "\n".join(doc.content for doc in top_docs)
        
        return final_result
```

---

### **8. 在对话中使用 RAG**

**代码**：`src/backend/agentchat/api/v1/completion.py`

```python
@router.post("/completion")
async def chat_completion(
    user_input: str,
    agent_id: str,
    knowledge_ids: list
):
    # 1. 如果启用了知识库，先检索相关内容
    knowledge_context = ""
    if knowledge_ids:
        knowledge_context = await RagHandler.retrieve_ranked_documents(
            user_input,
            knowledge_ids
        )
    
    # 2. 构建提示词
    prompt = f"""
    你是一个智能助手。请根据以下知识库内容回答用户问题。
    
    知识库内容：
    {knowledge_context}
    
    用户问题：{user_input}
    
    请基于知识库内容回答，不要编造信息。
    """
    
    # 3. 调用 LLM 生成回答
    response = await llm.generate(prompt)
    
    return response
```

---

## 🎓 RAG 的核心价值

### **1. 让 AI 拥有专业知识**

```
没有 RAG：
用户：我们公司的考勤制度是什么？
AI：我不知道你们公司的具体制度。

有 RAG：
用户：我们公司的考勤制度是什么？
AI：根据公司员工手册，考勤制度如下：
    1. 上班时间：9:00-18:00
    2. 迟到15分钟内不扣款
    3. 月累计迟到3次扣100元...
```

### **2. 知识实时更新**

```
上传新文档 → 自动向量化 → 立即可用
```

### **3. 回答有依据**

```
AI 回答：根据《产品使用手册 v2.3》第5章...
（可以追溯来源）
```

### **4. 支持多种文档格式**

```
✅ PDF
✅ Word (.docx)
✅ TXT
✅ Markdown
✅ Excel
✅ PPT
```

---

## 🎯 总结

### **RAG 在 OmniAgent 中的作用**

1. **知识库管理**：上传、存储、管理企业文档
2. **智能检索**：根据用户问题自动查找相关内容
3. **增强回答**：让 AI 基于真实文档回答，而不是编造
4. **实时更新**：新上传的文档立即生效

### **RAG 的完整流程**

```
文档上传 → 解析分块 → 向量化 → 存储到数据库
    ↓
用户提问 → 查询重写 → 向量检索 → 重排序 → 构建提示词 → AI 生成回答
```

### **关键技术**

- **Embedding**：文本向量化（text-embedding-3-small）
- **向量数据库**：ChromaDB（存储和检索向量）
- **关键词搜索**：Elasticsearch（精确匹配）
- **重排序**：Rerank 模型（提高准确性）
- **LLM**：通义千问（生成最终回答）

---

## 💡 实际应用场景

1. **企业知识库**：员工手册、规章制度、操作指南
2. **客服系统**：产品文档、FAQ、售后政策
3. **技术文档**：API 文档、开发指南、最佳实践
4. **教育培训**：课程资料、学习笔记、考试大纲
5. **法律咨询**：法律条文、案例分析、合同模板

---

现在你明白 RAG 的作用了吗？简单说就是：**让 AI 能够查询你的私有文档，给出准确的回答！**
