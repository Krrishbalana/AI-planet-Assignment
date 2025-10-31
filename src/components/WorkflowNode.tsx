import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { MessageSquare, Database, Brain, MessageCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export type NodeData = {
  label: string;
  type: 'userQuery' | 'knowledgeBase' | 'llmEngine' | 'output';
  config?: Record<string, any>;
};

const nodeIcons = {
  userQuery: MessageSquare,
  knowledgeBase: Database,
  llmEngine: Brain,
  output: MessageCircle,
};

const nodeColors = {
  userQuery: 'from-blue-500/20 to-blue-600/20 border-blue-500/50',
  knowledgeBase: 'from-green-500/20 to-green-600/20 border-green-500/50',
  llmEngine: 'from-purple-500/20 to-purple-600/20 border-purple-500/50',
  output: 'from-orange-500/20 to-orange-600/20 border-orange-500/50',
};

const iconColors = {
  userQuery: 'text-blue-400',
  knowledgeBase: 'text-green-400',
  llmEngine: 'text-purple-400',
  output: 'text-orange-400',
};

const WorkflowNode = ({ data, selected }: NodeProps<NodeData>) => {
  const Icon = nodeIcons[data.type];
  
  return (
    <div
      className={cn(
        'px-6 py-4 shadow-lg rounded-lg bg-gradient-to-br backdrop-blur-sm border-2 transition-all duration-200 min-w-[180px]',
        nodeColors[data.type],
        selected ? 'ring-2 ring-primary shadow-primary/50' : ''
      )}
    >
      {data.type !== 'userQuery' && (
        <Handle
          type="target"
          position={Position.Left}
          className="!bg-primary !border-primary"
        />
      )}
      
      <div className="flex items-center gap-3">
        <Icon className={cn('w-5 h-5', iconColors[data.type])} />
        <div className="font-medium text-sm text-foreground">{data.label}</div>
      </div>
      
      {data.type !== 'output' && (
        <Handle
          type="source"
          position={Position.Right}
          className="!bg-primary !border-primary"
        />
      )}
    </div>
  );
};

export default memo(WorkflowNode);
