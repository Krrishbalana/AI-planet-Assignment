"""
Database configuration and models
PostgreSQL connection using SQLAlchemy
"""
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/workflow_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    is_valid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    nodes = relationship("WorkflowNode", back_populates="workflow", cascade="all, delete-orphan")
    edges = relationship("WorkflowEdge", back_populates="workflow", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="workflow")
    chat_history = relationship("ChatHistory", back_populates="workflow")

class WorkflowNode(Base):
    __tablename__ = "workflow_nodes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"))
    node_id = Column(String, nullable=False)
    node_type = Column(String, nullable=False)  # userQuery, knowledgeBase, llmEngine, output
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    config = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="nodes")

class WorkflowEdge(Base):
    __tablename__ = "workflow_edges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"))
    edge_id = Column(String, nullable=False)
    source_node_id = Column(String, nullable=False)
    target_node_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="edges")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    processed = Column(Boolean, default=False)
    embedding_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="documents")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True))
    message = Column(Text, nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="chat_history")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
