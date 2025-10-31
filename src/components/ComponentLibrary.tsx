import { MessageSquare, Database, Brain, MessageCircle } from 'lucide-react';
import { Card } from '@/components/ui/card';

const components = [
  {
    type: 'userQuery',
    label: 'User Query',
    icon: MessageSquare,
    description: 'Entry point for user queries',
    color: 'text-blue-400',
  },
  {
    type: 'knowledgeBase',
    label: 'Knowledge Base',
    icon: Database,
    description: 'Upload & process documents',
    color: 'text-green-400',
  },
  {
    type: 'llmEngine',
    label: 'LLM Engine',
    icon: Brain,
    description: 'AI model processing',
    color: 'text-purple-400',
  },
  {
    type: 'output',
    label: 'Output',
    icon: MessageCircle,
    description: 'Display responses',
    color: 'text-orange-400',
  },
];

interface ComponentLibraryProps {
  onDragStart: (event: React.DragEvent, nodeType: string) => void;
}

export const ComponentLibrary = ({ onDragStart }: ComponentLibraryProps) => {
  return (
    <div className="flex-1 bg-card p-4 space-y-3 overflow-y-auto">
      <h2 className="text-lg font-semibold mb-4 text-foreground">Components</h2>
      {components.map((component) => {
        const Icon = component.icon;
        return (
          <Card
            key={component.type}
            draggable
            onDragStart={(e) => onDragStart(e, component.type)}
            className="p-4 cursor-move hover:bg-accent/50 transition-colors border-border/50"
          >
            <div className="flex items-start gap-3">
              <Icon className={`w-5 h-5 mt-0.5 ${component.color}`} />
              <div className="flex-1">
                <h3 className="font-medium text-sm text-foreground">{component.label}</h3>
                <p className="text-xs text-muted-foreground mt-1">
                  {component.description}
                </p>
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
};
