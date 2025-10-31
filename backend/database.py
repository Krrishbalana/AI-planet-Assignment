"""
Database configuration and models
PostgreSQL connection using SQLAlchemy
"""
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from datetime import datetime
import os

# Database URL with SQLite fallback for easy development
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Default to SQLite for local development
    DATABASE_URL = "sqlite:///./workflow_db.sqlite"
    print("ℹ️  No DATABASE_URL found, using SQLite: ./workflow_db.sqlite")

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_engine_info() -> str:
    """Get database engine information"""
    if DATABASE_URL.startswith("sqlite"):
        return f"SQLite (local file)"
    elif DATABASE_URL.startswith("postgresql"):
        return f"PostgreSQL"
    else:
        return f"Database connected"

# UUID type that works with both SQLite and PostgreSQL
class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value

# Database Models
class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), nullable=False)
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
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(GUID(), ForeignKey("workflows.id", ondelete="CASCADE"))
    node_id = Column(String, nullable=False)
    node_type = Column(String, nullable=False)  # userQuery, knowledgeBase, llmEngine, output
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    config = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="nodes")

class WorkflowEdge(Base):
    __tablename__ = "workflow_edges"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(GUID(), ForeignKey("workflows.id", ondelete="CASCADE"))
    edge_id = Column(String, nullable=False)
    source_node_id = Column(String, nullable=False)
    target_node_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    workflow = relationship("Workflow", back_populates="edges")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(GUID(), ForeignKey("workflows.id", ondelete="CASCADE"))
    user_id = Column(GUID(), nullable=False)
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
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(GUID(), ForeignKey("workflows.id", ondelete="CASCADE"))
    user_id = Column(GUID())
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
