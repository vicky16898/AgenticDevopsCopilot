from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from app.rag.qdrant import qdrant_manager
from app.core.config import settings
import uuid

class RAGIngestor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        self.client = qdrant_manager.get_client()
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        qdrant_manager.ensure_collection_exists()

    def ingest_files(self, files: List[Dict[str, str]]):
        """
        Ingests a list of files (from RepoParser) into Qdrant.
        files: List of dicts with 'path', 'content', 'extension'
        """
        documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

        for file in files:
            chunks = text_splitter.split_text(file["content"])
            for i, chunk in enumerate(chunks):
                documents.append(Document(
                    page_content=chunk,
                    metadata={
                        "source": file["path"],
                        "extension": file.get("extension", ""),
                        "chunk_index": i
                    }
                ))
        
        if not documents:
            return {"status": "skipped", "count": 0}

        # Generate embeddings
        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]
        ids = [str(uuid.uuid4()) for _ in documents]

        embeddings = self.embeddings.embed_documents(texts)

        # Upsert to Qdrant
        points = []
        from qdrant_client.http import models

        for i in range(len(ids)):
            points.append(models.PointStruct(
                id=ids[i],
                vector=embeddings[i],
                payload=metadatas[i] | {"page_content": texts[i]}
            ))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return {"status": "success", "count": len(points)}

rag_ingestor = RAGIngestor()
