"""
Workflow execution service
Orchestrate component execution based on workflow definition
"""
from typing import Dict, Any, List
from database import Workflow
from services.vector_store import VectorStore
from services.llm_service import LLMService

class WorkflowExecutor:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_service = LLMService()
    
    async def execute(self, workflow: Workflow, user_query: str) -> Dict[str, Any]:
        """Execute a workflow with a user query"""
        # Build execution graph
        nodes = {node.node_id: node for node in workflow.nodes}
        edges = workflow.edges
        
        # Find start node (userQuery)
        start_nodes = [n for n in workflow.nodes if n.node_type == "userQuery"]
        if not start_nodes:
            raise ValueError("No user query node found")
        
        # Execute workflow
        context = {"query": user_query, "sources": []}
        current_node_id = start_nodes[0].node_id
        
        while current_node_id:
            node = nodes.get(current_node_id)
            if not node:
                break
            
            # Execute node
            context = await self._execute_node(node, context, str(workflow.id))
            
            # Find next node
            next_edges = [e for e in edges if e.source_node_id == current_node_id]
            current_node_id = next_edges[0].target_node_id if next_edges else None
        
        return {
            "response": context.get("response", "No response generated"),
            "sources": context.get("sources", [])
        }
    
    async def _execute_node(
        self,
        node: Any,
        context: Dict[str, Any],
        workflow_id: str
    ) -> Dict[str, Any]:
        """Execute a single node"""
        
        if node.node_type == "userQuery":
            # User query is already in context
            return context
        
        elif node.node_type == "knowledgeBase":
            # Retrieve relevant documents
            config = node.config or {}
            if config.get("passContext", True):
                results = await self.vector_store.search(
                    context["query"],
                    n_results=5
                )
                context["knowledge"] = [r["text"] for r in results]
                context["sources"].extend([r["metadata"] for r in results])
            return context
        
        elif node.node_type == "llmEngine":
            # Generate response using LLM
            config = node.config or {}
            
            response = await self.llm_service.generate(
                prompt=context["query"],
                model=config.get("model", "gpt-4"),
                temperature=config.get("temperature", 0.7),
                system_prompt=config.get("systemPrompt"),
                context=context.get("knowledge")
            )
            
            context["response"] = response["response"]
            return context
        
        elif node.node_type == "output":
            # Output is handled by the chat interface
            return context
        
        return context
