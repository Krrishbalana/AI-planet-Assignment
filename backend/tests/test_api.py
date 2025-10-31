"""
Test suite for backend API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_list_llm_models():
    """Test LLM models listing"""
    response = client.get("/api/llm/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0
    assert any(m["id"] == "gpt-4" for m in data["models"])


def test_create_workflow():
    """Test workflow creation"""
    user_id = str(uuid4())
    workflow_data = {
        "name": "Test Workflow",
        "description": "A test workflow",
        "user_id": user_id,
        "nodes": [
            {
                "node_id": "node-1",
                "node_type": "userQuery",
                "position_x": 100.0,
                "position_y": 100.0,
                "config": {}
            },
            {
                "node_id": "node-2",
                "node_type": "output",
                "position_x": 300.0,
                "position_y": 100.0,
                "config": {}
            }
        ],
        "edges": [
            {
                "edge_id": "edge-1",
                "source_node_id": "node-1",
                "target_node_id": "node-2"
            }
        ]
    }
    
    response = client.post("/api/workflows", json=workflow_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "message" in data
    
    # Store workflow ID for other tests
    return data["id"]


def test_get_workflow():
    """Test workflow retrieval"""
    # First create a workflow
    workflow_id = test_create_workflow()
    
    # Then retrieve it
    response = client.get(f"/api/workflows/{workflow_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Workflow"
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1


def test_update_workflow():
    """Test workflow update"""
    # First create a workflow
    workflow_id = test_create_workflow()
    
    # Update it
    update_data = {
        "name": "Updated Workflow",
        "is_valid": True
    }
    response = client.put(f"/api/workflows/{workflow_id}", json=update_data)
    assert response.status_code == 200
    
    # Verify update
    response = client.get(f"/api/workflows/{workflow_id}")
    data = response.json()
    assert data["name"] == "Updated Workflow"
    assert data["is_valid"] == True


def test_delete_workflow():
    """Test workflow deletion"""
    # First create a workflow
    workflow_id = test_create_workflow()
    
    # Delete it
    response = client.delete(f"/api/workflows/{workflow_id}")
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(f"/api/workflows/{workflow_id}")
    assert response.status_code == 404


def test_workflow_not_found():
    """Test 404 for non-existent workflow"""
    fake_id = str(uuid4())
    response = client.get(f"/api/workflows/{fake_id}")
    assert response.status_code == 404


def test_list_user_workflows():
    """Test listing user workflows"""
    user_id = str(uuid4())
    
    # Create a workflow
    workflow_data = {
        "name": "User Test Workflow",
        "user_id": user_id,
        "nodes": [],
        "edges": []
    }
    client.post("/api/workflows", json=workflow_data)
    
    # List workflows for user
    response = client.get(f"/api/workflows/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_chat_history_empty():
    """Test empty chat history"""
    workflow_id = str(uuid4())
    response = client.get(f"/api/chat/history/{workflow_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
