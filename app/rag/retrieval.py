from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from app.rag.qdrant import qdrant_manager
from app.core.config import settings

class RAGRetriever:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        self.client = qdrant_manager.get_client()
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def get_vector_store(self):
        return Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )

    def get_retriever(self, search_kwargs: dict = {"k": 4}):
        vector_store = self.get_vector_store()
        return vector_store.as_retriever(search_kwargs=search_kwargs)

rag_retriever = RAGRetriever()
