"""
Workflow management endpoints
Create, read, update, delete workflows
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from database import get_db, Workflow, WorkflowNode, WorkflowEdge

router = APIRouter()

class NodeCreate(BaseModel):
    node_id: str
    node_type: str
    position_x: float
    position_y: float
    config: Dict[str, Any] = {}

class EdgeCreate(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: UUID
    nodes: List[NodeCreate] = []
    edges: List[EdgeCreate] = []

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    nodes: Optional[List[NodeCreate]] = None
    edges: Optional[List[EdgeCreate]] = None
    is_valid: Optional[bool] = None

@router.post("/")
async def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    """Create a new workflow"""
    db_workflow = Workflow(
        user_id=workflow.user_id,
        name=workflow.name,
        description=workflow.description
    )
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    
    # Add nodes
    for node in workflow.nodes:
        db_node = WorkflowNode(
            workflow_id=db_workflow.id,
            node_id=node.node_id,
            node_type=node.node_type,
            position_x=node.position_x,
            position_y=node.position_y,
            config=node.config
        )
        db.add(db_node)
    
    # Add edges
    for edge in workflow.edges:
        db_edge = WorkflowEdge(
            workflow_id=db_workflow.id,
            edge_id=edge.edge_id,
            source_node_id=edge.source_node_id,
            target_node_id=edge.target_node_id
        )
        db.add(db_edge)
    
    db.commit()
    return {"id": str(db_workflow.id), "message": "Workflow created successfully"}

@router.get("/{workflow_id}")
async def get_workflow(workflow_id: UUID, db: Session = Depends(get_db)):
    """Get a specific workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {
        "id": str(workflow.id),
        "name": workflow.name,
        "description": workflow.description,
        "is_valid": workflow.is_valid,
        "nodes": [
            {
                "id": str(node.id),
                "node_id": node.node_id,
                "type": node.node_type,
                "position": {"x": node.position_x, "y": node.position_y},
                "config": node.config
            }
            for node in workflow.nodes
        ],
        "edges": [
            {
                "id": str(edge.id),
                "edge_id": edge.edge_id,
                "source": edge.source_node_id,
                "target": edge.target_node_id
            }
            for edge in workflow.edges
        ],
        "created_at": workflow.created_at.isoformat(),
        "updated_at": workflow.updated_at.isoformat()
    }

@router.get("/user/{user_id}")
async def list_user_workflows(user_id: UUID, db: Session = Depends(get_db)):
    """List all workflows for a user"""
    workflows = db.query(Workflow).filter(Workflow.user_id == user_id).all()
    return [
        {
            "id": str(w.id),
            "name": w.name,
            "description": w.description,
            "is_valid": w.is_valid,
            "created_at": w.created_at.isoformat()
        }
        for w in workflows
    ]

@router.put("/{workflow_id}")
async def update_workflow(
    workflow_id: UUID,
    workflow: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """Update a workflow"""
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if workflow.name:
        db_workflow.name = workflow.name
    if workflow.description is not None:
        db_workflow.description = workflow.description
    if workflow.is_valid is not None:
        db_workflow.is_valid = workflow.is_valid
    
    # Update nodes if provided
    if workflow.nodes is not None:
        # Delete existing nodes
        db.query(WorkflowNode).filter(WorkflowNode.workflow_id == workflow_id).delete()
        # Add new nodes
        for node in workflow.nodes:
            db_node = WorkflowNode(
                workflow_id=workflow_id,
                node_id=node.node_id,
                node_type=node.node_type,
                position_x=node.position_x,
                position_y=node.position_y,
                config=node.config
            )
            db.add(db_node)
    
    # Update edges if provided
    if workflow.edges is not None:
        # Delete existing edges
        db.query(WorkflowEdge).filter(WorkflowEdge.workflow_id == workflow_id).delete()
        # Add new edges
        for edge in workflow.edges:
            db_edge = WorkflowEdge(
                workflow_id=workflow_id,
                edge_id=edge.edge_id,
                source_node_id=edge.source_node_id,
                target_node_id=edge.target_node_id
            )
            db.add(db_edge)
    
    db.commit()
    return {"message": "Workflow updated successfully"}

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: UUID, db: Session = Depends(get_db)):
    """Delete a workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    db.delete(workflow)
    db.commit()
    return {"message": "Workflow deleted successfully"}
