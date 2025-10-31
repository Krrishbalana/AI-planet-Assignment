"""
Vector store service using ChromaDB
Store and retrieve document embeddings
"""
import os
import chromadb
from typing import List, Dict, Any
from openai import AsyncOpenAI


class VectorStore:
    def __init__(self):
        # Use the new PersistentClient API (no Settings class anymore)
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = "documents"

        # Ensure collection exists
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using OpenAI"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        client = AsyncOpenAI(api_key=api_key)
        embeddings = []

        for text in texts:
            response = await client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            embeddings.append(response.data[0].embedding)

        return embeddings

    async def store_embeddings(
        self,
        document_id: str,
        texts: List[str],
        embeddings: List[List[float]]
    ):
        """Store embeddings in ChromaDB"""
        ids = [f"{document_id}_{i}" for i in range(len(texts))]
        metadatas = [{"document_id": document_id, "chunk_index": i} for i in range(len(texts))]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

    async def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        # Get query embedding
        query_embedding = await self.create_embeddings([query])

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        # Format response
        return [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]

    async def delete_document(self, document_id: str):
        """Delete all chunks for a document"""
        results = self.collection.get(where={"document_id": document_id})
        if results and "ids" in results and results["ids"]:
            self.collection.delete(ids=results["ids"])
