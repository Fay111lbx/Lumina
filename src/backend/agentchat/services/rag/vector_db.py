"""向量数据库客户端"""
from typing import List, Dict, Any
from agentchat.settings import app_settings
from loguru import logger


class VectorDBClient:
    """向量数据库客户端基类"""

    def __init__(self):
        self.mode = app_settings.rag.vector_db.get('mode', 'chroma')
        self.host = app_settings.rag.vector_db.get('host', '127.0.0.1')
        self.port = app_settings.rag.vector_db.get('port', '8000')
        self._client = None
        self._init_client()

    def _init_client(self):
        """初始化向量数据库客户端"""
        if self.mode == "chroma":
            self._init_chroma()
        elif self.mode == "standalone":
            self._init_milvus()
        elif self.mode == "lite":
            self._init_milvus_lite()
        else:
            logger.warning(f"Unknown vector_db mode: {self.mode}, using chroma as default")
            self._init_chroma()

    def _init_chroma(self):
        """初始化 ChromaDB"""
        try:
            import chromadb

            # 使用 HttpClient 连接 ChromaDB 服务器
            self._client = chromadb.HttpClient(
                host=self.host,
                port=int(self.port)
            )
            logger.success(f"ChromaDB initialized with server mode: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB server: {e}")
            logger.info("Falling back to persistent client mode")
            try:
                import os
                persist_directory = os.path.join(os.getcwd(), "data", "chroma_db")
                os.makedirs(persist_directory, exist_ok=True)
                self._client = chromadb.PersistentClient(path=persist_directory)
                logger.success(f"ChromaDB initialized with persistent storage: {persist_directory}")
            except Exception as e2:
                logger.error(f"Failed to initialize ChromaDB: {e2}")
                self._client = None

    def _init_milvus(self):
        """初始化 Milvus"""
        try:
            from pymilvus import connections, Collection
            connections.connect(host=self.host, port=self.port)
            logger.success(f"Milvus client initialized: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to initialize Milvus: {e}")
            self._client = None

    def _init_milvus_lite(self):
        """初始化 Milvus Lite"""
        try:
            from pymilvus import MilvusClient
            self._client = MilvusClient(f"http://{self.host}:{self.port}")
            logger.success(f"Milvus Lite client initialized: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to initialize Milvus Lite: {e}")
            self._client = None

    async def search(self, query: str, knowledge_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索文档"""
        try:
            if self.mode == "chroma":
                return await self._search_chroma(query, knowledge_id, limit)
            elif self.mode in ["standalone", "lite"]:
                return await self._search_milvus(query, knowledge_id, limit)
            return []
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def search_summary(self, query: str, knowledge_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """搜索文档摘要"""
        # 目前与普通搜索相同，可以根据需要扩展
        return await self.search(query, knowledge_id, limit)

    async def _search_chroma(self, query: str, collection_name: str, limit: int) -> List[Dict[str, Any]]:
        """ChromaDB 搜索"""
        try:
            collection = self._client.get_or_create_collection(name=collection_name)
            results = collection.query(
                query_texts=[query],
                n_results=limit
            )

            documents = []
            if results and results.get('documents'):
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'content': doc,
                        'metadata': results.get('metadatas', [[]])[0][i] if results.get('metadatas') else {},
                        'distance': results.get('distances', [[]])[0][i] if results.get('distances') else 0
                    })
            return documents
        except Exception as e:
            logger.error(f"ChromaDB search failed: {e}")
            return []

    async def _search_milvus(self, query: str, collection_name: str, limit: int) -> List[Dict[str, Any]]:
        """Milvus 搜索"""
        try:
            from pymilvus import Collection
            collection = Collection(collection_name)
            # 这里需要先将 query 转换为向量，暂时返回空列表
            logger.warning("Milvus search not fully implemented, need embedding conversion")
            return []
        except Exception as e:
            logger.error(f"Milvus search failed: {e}")
            return []

    async def insert(self, collection_name: str, chunks: List[Dict[str, Any]]):
        """插入文档"""
        try:
            if self.mode == "chroma":
                await self._insert_chroma(collection_name, chunks)
            elif self.mode in ["standalone", "lite"]:
                await self._insert_milvus(collection_name, chunks)
        except Exception as e:
            logger.error(f"Insert failed: {e}")

    async def _insert_chroma(self, collection_name: str, chunks: List[Dict[str, Any]]):
        """ChromaDB 插入"""
        try:
            collection = self._client.get_or_create_collection(name=collection_name)

            documents = []
            metadatas = []
            ids = []

            for i, chunk in enumerate(chunks):
                documents.append(chunk.get('content', ''))
                metadatas.append(chunk.get('metadata', {}))
                ids.append(chunk.get('id', f"{collection_name}_{i}"))

            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.success(f"Inserted {len(chunks)} chunks into ChromaDB collection: {collection_name}")
        except Exception as e:
            logger.error(f"ChromaDB insert failed: {e}")

    async def _insert_milvus(self, collection_name: str, chunks: List[Dict[str, Any]]):
        """Milvus 插入"""
        try:
            from pymilvus import Collection
            collection = Collection(collection_name)
            # 这里需要处理向量数据，暂时不实现
            logger.warning("Milvus insert not fully implemented")
        except Exception as e:
            logger.error(f"Milvus insert failed: {e}")

    async def delete_by_file_id(self, file_id: str, knowledge_id: str):
        """根据文件ID删除文档"""
        try:
            if self.mode == "chroma":
                await self._delete_chroma(file_id, knowledge_id)
            elif self.mode in ["standalone", "lite"]:
                await self._delete_milvus(file_id, knowledge_id)
        except Exception as e:
            logger.error(f"Delete failed: {e}")

    async def _delete_chroma(self, file_id: str, collection_name: str):
        """ChromaDB 删除"""
        try:
            collection = self._client.get_or_create_collection(name=collection_name)
            # 根据 metadata 中的 file_id 删除
            collection.delete(
                where={"file_id": file_id}
            )
            logger.success(f"Deleted documents with file_id={file_id} from ChromaDB collection: {collection_name}")
        except Exception as e:
            logger.error(f"ChromaDB delete failed: {e}")

    async def _delete_milvus(self, file_id: str, collection_name: str):
        """Milvus 删除"""
        try:
            from pymilvus import Collection
            collection = Collection(collection_name)
            # 根据表达式删除
            expr = f'file_id == "{file_id}"'
            collection.delete(expr)
            logger.success(f"Deleted documents with file_id={file_id} from Milvus collection: {collection_name}")
        except Exception as e:
            logger.error(f"Milvus delete failed: {e}")


# 创建全局客户端实例
milvus_client = VectorDBClient()
