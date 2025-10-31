import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Upload } from 'lucide-react';

interface ConfigPanelProps {
  selectedNode: any;
  onConfigChange: (nodeId: string, config: any) => void;
}

export const ConfigPanel = ({ selectedNode, onConfigChange }: ConfigPanelProps) => {
  if (!selectedNode) {
    return (
      <div className="w-80 bg-card border-l border-border p-4">
        <div className="text-center text-muted-foreground mt-8">
          <p>Select a component to configure</p>
        </div>
      </div>
    );
  }

  const handleChange = (key: string, value: any) => {
    onConfigChange(selectedNode.id, {
      ...selectedNode.data.config,
      [key]: value,
    });
  };

  const renderConfig = () => {
    switch (selectedNode.data.type) {
      case 'userQuery':
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="placeholder">Placeholder Text</Label>
              <Input
                id="placeholder"
                value={selectedNode.data.config?.placeholder || ''}
                onChange={(e) => handleChange('placeholder', e.target.value)}
                placeholder="Enter your question..."
              />
            </div>
          </div>
        );

      case 'knowledgeBase':
        return (
          <div className="space-y-4">
            <div>
              <Label>Document Upload</Label>
              <Button variant="outline" className="w-full mt-2">
                <Upload className="w-4 h-4 mr-2" />
                Upload Documents
              </Button>
            </div>
            <div>
              <Label htmlFor="chunkSize">Chunk Size</Label>
              <Input
                id="chunkSize"
                type="number"
                value={selectedNode.data.config?.chunkSize || 1000}
                onChange={(e) => handleChange('chunkSize', parseInt(e.target.value))}
              />
            </div>
            <div>
              <Label htmlFor="chunkOverlap">Chunk Overlap</Label>
              <Input
                id="chunkOverlap"
                type="number"
                value={selectedNode.data.config?.chunkOverlap || 200}
                onChange={(e) => handleChange('chunkOverlap', parseInt(e.target.value))}
              />
            </div>
            <div className="flex items-center justify-between">
              <Label htmlFor="passContext">Pass Context to LLM</Label>
              <Switch
                id="passContext"
                checked={selectedNode.data.config?.passContext ?? true}
                onCheckedChange={(checked) => handleChange('passContext', checked)}
              />
            </div>
          </div>
        );

      case 'llmEngine':
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="model">Model</Label>
              <Select
                value={selectedNode.data.config?.model || 'gpt-4'}
                onValueChange={(value) => handleChange('model', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select model" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="gpt-4">GPT-4</SelectItem>
                  <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                  <SelectItem value="gemini-pro">Gemini Pro</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="temperature">Temperature</Label>
              <Input
                id="temperature"
                type="number"
                min="0"
                max="2"
                step="0.1"
                value={selectedNode.data.config?.temperature || 0.7}
                onChange={(e) => handleChange('temperature', parseFloat(e.target.value))}
              />
            </div>
            <div>
              <Label htmlFor="systemPrompt">System Prompt</Label>
              <Textarea
                id="systemPrompt"
                value={selectedNode.data.config?.systemPrompt || ''}
                onChange={(e) => handleChange('systemPrompt', e.target.value)}
                placeholder="You are a helpful assistant..."
                rows={4}
              />
            </div>
            <div className="flex items-center justify-between">
              <Label htmlFor="useWebSearch">Enable Web Search</Label>
              <Switch
                id="useWebSearch"
                checked={selectedNode.data.config?.useWebSearch ?? false}
                onCheckedChange={(checked) => handleChange('useWebSearch', checked)}
              />
            </div>
          </div>
        );

      case 'output':
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="displayMode">Display Mode</Label>
              <Select
                value={selectedNode.data.config?.displayMode || 'chat'}
                onValueChange={(value) => handleChange('displayMode', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select display mode" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="chat">Chat Interface</SelectItem>
                  <SelectItem value="panel">Panel View</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-80 bg-card border-l border-border p-4 overflow-y-auto">
      <h2 className="text-lg font-semibold mb-4 text-foreground">
        {selectedNode.data.label} Configuration
      </h2>
      <Card className="p-4 bg-card/50 border-border">
        {renderConfig()}
      </Card>
    </div>
  );
};
