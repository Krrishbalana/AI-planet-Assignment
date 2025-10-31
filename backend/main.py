"""
FastAPI Backend for No-Code Workflow Builder
Main application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from routers import workflows, documents, chat, llm
from database import engine, Base, get_engine_info

# Create database tables with error handling
try:
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database connected successfully: {get_engine_info()}")
except Exception as e:
    print(f"⚠️  Database connection issue: {e}")
    print("Backend will continue but database operations may fail")

app = FastAPI(
    title="Workflow Builder API",
    description="Backend API for AI-powered workflow builder",
    version="1.0.0"
)

# Configure CORS
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:8080,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(llm.router, prefix="/api/llm", tags=["llm"])

@app.get("/")
async def root():
    return {
        "message": "Workflow Builder API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
