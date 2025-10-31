"""
Vector store service using ChromaDB
Store and retrieve document embeddings
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import os

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        self.collection_name = "documents"
    
    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using OpenAI"""
        # Import OpenAI here to avoid circular imports
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        embeddings = []
        for text in texts:
            response = await openai.Embedding.acreate(
                model="text-embedding-ada-002",
                input=text
            )
            embeddings.append(response['data'][0]['embedding'])
        
        return embeddings
    
    async def store_embeddings(
        self,
        document_id: str,
        texts: List[str],
        embeddings: List[List[float]]
    ):
        """Store embeddings in ChromaDB"""
        collection = self.client.get_or_create_collection(
            name=self.collection_name
        )
        
        ids = [f"{document_id}_{i}" for i in range(len(texts))]
        metadatas = [{"document_id": document_id, "chunk_index": i} for i in range(len(texts))]
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
    
    async def search(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        collection = self.client.get_collection(name=self.collection_name)
        
        # Get query embedding
        query_embedding = await self.create_embeddings([query])
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        return [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(results['documents'][0], results['metadatas'][0])
        ]
    
    async def delete_document(self, document_id: str):
        """Delete all chunks for a document"""
        collection = self.client.get_collection(name=self.collection_name)
        
        # Get all IDs for this document
        results = collection.get(
            where={"document_id": document_id}
        )
        
        if results['ids']:
            collection.delete(ids=results['ids'])
