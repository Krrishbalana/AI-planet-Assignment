"""
Chat interface endpoints
Handle user queries and workflow execution
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from uuid import UUID

from database import get_db, ChatHistory, Workflow
from services.workflow_executor import WorkflowExecutor

router = APIRouter()
workflow_executor = WorkflowExecutor()

class ChatMessage(BaseModel):
    workflow_id: UUID
    user_id: UUID
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

@router.post("/message")
async def send_message(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
) -> ChatResponse:
    """Send a message and execute the workflow"""
    # Get workflow
    workflow = db.query(Workflow).filter(Workflow.id == chat_message.workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if not workflow.is_valid:
        raise HTTPException(status_code=400, detail="Workflow is not valid")
    
    # Save user message
    user_message = ChatHistory(
        workflow_id=chat_message.workflow_id,
        user_id=chat_message.user_id,
        message=chat_message.message,
        role="user"
    )
    db.add(user_message)
    db.commit()
    
    try:
        # Execute workflow
        result = await workflow_executor.execute(
            workflow=workflow,
            user_query=chat_message.message
        )
        
        # Save assistant response
        assistant_message = ChatHistory(
            workflow_id=chat_message.workflow_id,
            user_id=chat_message.user_id,
            message=result["response"],
            role="assistant"
        )
        db.add(assistant_message)
        db.commit()
        
        return ChatResponse(
            response=result["response"],
            sources=result.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{workflow_id}")
async def get_chat_history(
    workflow_id: UUID,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history for a workflow"""
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.workflow_id == workflow_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    
    return [
        {
            "id": str(msg.id),
            "message": msg.message,
            "role": msg.role,
            "created_at": msg.created_at.isoformat()
        }
        for msg in reversed(history)
    ]

@router.delete("/history/{workflow_id}")
async def clear_chat_history(workflow_id: UUID, db: Session = Depends(get_db)):
    """Clear chat history for a workflow"""
    db.query(ChatHistory).filter(ChatHistory.workflow_id == workflow_id).delete()
    db.commit()
    return {"message": "Chat history cleared successfully"}
