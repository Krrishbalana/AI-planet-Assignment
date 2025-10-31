import { useCallback, useRef, useState } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  BackgroundVariant,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  ReactFlowProvider,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { ComponentLibrary } from './ComponentLibrary';
import { ConfigPanel } from './ConfigPanel';
import { ChatInterface } from './ChatInterface';
import { BackendStatus } from './BackendStatus';
import WorkflowNode, { NodeData } from './WorkflowNode';
import { Button } from './ui/button';
import { Play, MessageSquare, Save } from 'lucide-react';
import { toast } from 'sonner';
import { api } from '@/lib/api';

const nodeTypes = {
  custom: WorkflowNode,
};

const initialNodes: Node<NodeData>[] = [];
const initialEdges: Edge[] = [];

export const WorkflowBuilder = () => {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<Node<NodeData> | null>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      if (!reactFlowWrapper.current || !reactFlowInstance) return;

      const type = event.dataTransfer.getData('application/reactflow');
      if (!type) return;

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const labels: Record<string, string> = {
        userQuery: 'User Query',
        knowledgeBase: 'Knowledge Base',
        llmEngine: 'LLM Engine',
        output: 'Output',
      };

      const newNode: Node<NodeData> = {
        id: `${type}-${Date.now()}`,
        type: 'custom',
        position,
        data: {
          label: labels[type as keyof typeof labels],
          type: type as NodeData['type'],
          config: {},
        },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes]
  );

  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  const onNodeClick = useCallback((_event: React.MouseEvent, node: Node<NodeData>) => {
    setSelectedNode(node);
  }, []);

  const onConfigChange = useCallback(
    (nodeId: string, config: any) => {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === nodeId) {
            return {
              ...node,
              data: {
                ...node.data,
                config,
              },
            };
          }
          return node;
        })
      );
    },
    [setNodes]
  );

  const validateWorkflow = () => {
    if (nodes.length === 0) {
      toast.error('Add components to build a workflow');
      return false;
    }

    const hasUserQuery = nodes.some((n) => n.data.type === 'userQuery');
    const hasOutput = nodes.some((n) => n.data.type === 'output');

    if (!hasUserQuery) {
      toast.error('Workflow must have a User Query component');
      return false;
    }

    if (!hasOutput) {
      toast.error('Workflow must have an Output component');
      return false;
    }

    toast.success('Workflow is valid!');
    return true;
  };

  const handleSaveWorkflow = async () => {
    if (!validateWorkflow()) return;

    setIsSaving(true);
    try {
      // Temporary user ID (in real app, get from auth)
      const userId = "00000000-0000-0000-0000-000000000001";
      
      // Transform nodes and edges to API format
      const apiNodes = nodes.map(node => ({
        node_id: node.id,
        node_type: node.data.type,
        position_x: node.position.x,
        position_y: node.position.y,
        config: node.data.config || {},
      }));

      const apiEdges = edges.map(edge => ({
        edge_id: edge.id,
        source_node_id: edge.source,
        target_node_id: edge.target,
      }));

      if (workflowId) {
        // Update existing workflow
        await api.updateWorkflow(workflowId, {
          nodes: apiNodes,
          edges: apiEdges,
          is_valid: true,
        });
        toast.success('Workflow updated successfully!');
      } else {
        // Create new workflow
        const response = await api.createWorkflow({
          name: `Workflow ${new Date().toLocaleDateString()}`,
          description: 'AI Workflow',
          user_id: userId,
          nodes: apiNodes,
          edges: apiEdges,
          is_valid: true,
        });
        setWorkflowId(response.id);
        toast.success('Workflow saved successfully!');
      }
    } catch (error) {
      console.error('Save error:', error);
      toast.error(
        error instanceof Error
          ? error.message
          : 'Failed to save workflow. Make sure the backend is running.'
      );
    } finally {
      setIsSaving(false);
    }
  };

  const handleBuildStack = async () => {
    await handleSaveWorkflow();
  };

  const handleChatWithStack = () => {
    if (!workflowId) {
      toast.error('Please save the workflow first (click Build Stack)');
      return;
    }
    if (validateWorkflow()) {
      setChatOpen(true);
    }
  };

  return (
    <div className="flex h-screen bg-background">
      <div className="w-80 border-r border-border flex flex-col">
        <ComponentLibrary onDragStart={onDragStart} />
        <div className="p-4 border-t border-border">
          <BackendStatus />
        </div>
      </div>

      <div className="flex-1 flex flex-col">
        <div className="h-16 bg-card border-b border-border px-6 flex items-center justify-between">
          <h1 className="text-xl font-bold text-foreground">
            Workflow Builder
            {workflowId && <span className="text-sm text-muted-foreground ml-2">(Saved)</span>}
          </h1>
          <div className="flex gap-2">
            <Button onClick={handleBuildStack} variant="outline" disabled={isSaving}>
              <Play className="w-4 h-4 mr-2" />
              {isSaving ? 'Saving...' : 'Build Stack'}
            </Button>
            <Button onClick={handleChatWithStack}>
              <MessageSquare className="w-4 h-4 mr-2" />
              Chat with Stack
            </Button>
          </div>
        </div>

        <div ref={reactFlowWrapper} className="flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onInit={setReactFlowInstance}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            fitView
            className="bg-background"
          >
            <Controls />
            <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
          </ReactFlow>
        </div>
      </div>

      <ConfigPanel selectedNode={selectedNode} onConfigChange={onConfigChange} />

      <ChatInterface 
        open={chatOpen} 
        onOpenChange={setChatOpen} 
        workflowId={workflowId || undefined}
      />
    </div>
  );
};

export const WorkflowBuilderWrapper = () => (
  <ReactFlowProvider>
    <WorkflowBuilder />
  </ReactFlowProvider>
);
