"""
Document processing endpoints
Upload, process, and embed documents
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from uuid import UUID
import os
import aiofiles

from database import get_db, Document
from services.document_processor import DocumentProcessor
from services.vector_store import VectorStore

router = APIRouter()
document_processor = DocumentProcessor()
vector_store = VectorStore()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    workflow_id: UUID = None,
    user_id: UUID = None,
    db: Session = Depends(get_db)
):
    """Upload a document for processing"""
    try:
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Create document record
        document = Document(
            workflow_id=workflow_id,
            user_id=user_id,
            filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            mime_type=file.content_type
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return {
            "id": str(document.id),
            "filename": file.filename,
            "message": "Document uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{document_id}/process")
async def process_document(document_id: UUID, db: Session = Depends(get_db)):
    """Process a document and create embeddings"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Extract text from document
        text = document_processor.extract_text(document.file_path)
        
        # Chunk text
        chunks = document_processor.chunk_text(text)
        
        # Create embeddings
        embeddings = await vector_store.create_embeddings(chunks)
        
        # Store in vector database
        await vector_store.store_embeddings(
            str(document_id),
            chunks,
            embeddings
        )
        
        # Update document status
        document.processed = True
        document.embedding_count = len(chunks)
        db.commit()
        
        return {
            "message": "Document processed successfully",
            "chunks": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}")
async def get_document(document_id: UUID, db: Session = Depends(get_db)):
    """Get document information"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "id": str(document.id),
        "filename": document.filename,
        "file_size": document.file_size,
        "processed": document.processed,
        "embedding_count": document.embedding_count,
        "created_at": document.created_at.isoformat()
    }

@router.get("/workflow/{workflow_id}")
async def list_workflow_documents(workflow_id: UUID, db: Session = Depends(get_db)):
    """List all documents for a workflow"""
    documents = db.query(Document).filter(Document.workflow_id == workflow_id).all()
    return [
        {
            "id": str(d.id),
            "filename": d.filename,
            "processed": d.processed,
            "created_at": d.created_at.isoformat()
        }
        for d in documents
    ]

@router.delete("/{document_id}")
async def delete_document(document_id: UUID, db: Session = Depends(get_db)):
    """Delete a document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete from vector store
    await vector_store.delete_document(str(document_id))
    
    # Delete record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
