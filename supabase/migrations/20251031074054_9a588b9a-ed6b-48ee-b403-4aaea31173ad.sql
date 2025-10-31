-- Create workflows table to store user-created workflow definitions
CREATE TABLE IF NOT EXISTS public.workflows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  name TEXT NOT NULL,
  description TEXT,
  is_valid BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create workflow_nodes table to store individual components in a workflow
CREATE TABLE IF NOT EXISTS public.workflow_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES public.workflows(id) ON DELETE CASCADE NOT NULL,
  node_id TEXT NOT NULL,
  node_type TEXT NOT NULL CHECK (node_type IN ('userQuery', 'knowledgeBase', 'llmEngine', 'output')),
  position_x FLOAT NOT NULL,
  position_y FLOAT NOT NULL,
  config JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create workflow_edges table to store connections between nodes
CREATE TABLE IF NOT EXISTS public.workflow_edges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES public.workflows(id) ON DELETE CASCADE NOT NULL,
  edge_id TEXT NOT NULL,
  source_node_id TEXT NOT NULL,
  target_node_id TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create documents table for knowledge base uploads
CREATE TABLE IF NOT EXISTS public.documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES public.workflows(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id),
  filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_size INTEGER,
  mime_type TEXT,
  processed BOOLEAN DEFAULT false,
  embedding_count INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create chat_history table for conversation logs
CREATE TABLE IF NOT EXISTS public.chat_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES public.workflows(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES auth.users(id),
  message TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security
ALTER TABLE public.workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workflow_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workflow_edges ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;

-- RLS Policies for workflows
CREATE POLICY "Users can view their own workflows"
  ON public.workflows FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own workflows"
  ON public.workflows FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own workflows"
  ON public.workflows FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own workflows"
  ON public.workflows FOR DELETE
  USING (auth.uid() = user_id);

-- RLS Policies for workflow_nodes
CREATE POLICY "Users can view nodes in their workflows"
  ON public.workflow_nodes FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_nodes.workflow_id
    AND workflows.user_id = auth.uid()
  ));

CREATE POLICY "Users can create nodes in their workflows"
  ON public.workflow_nodes FOR INSERT
  WITH CHECK (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_nodes.workflow_id
    AND workflows.user_id = auth.uid()
  ));

CREATE POLICY "Users can update nodes in their workflows"
  ON public.workflow_nodes FOR UPDATE
  USING (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_nodes.workflow_id
    AND workflows.user_id = auth.uid()
  ));

CREATE POLICY "Users can delete nodes in their workflows"
  ON public.workflow_nodes FOR DELETE
  USING (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_nodes.workflow_id
    AND workflows.user_id = auth.uid()
  ));

-- RLS Policies for workflow_edges
CREATE POLICY "Users can view edges in their workflows"
  ON public.workflow_edges FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_edges.workflow_id
    AND workflows.user_id = auth.uid()
  ));

CREATE POLICY "Users can create edges in their workflows"
  ON public.workflow_edges FOR INSERT
  WITH CHECK (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_edges.workflow_id
    AND workflows.user_id = auth.uid()
  ));

CREATE POLICY "Users can update edges in their workflows"
  ON public.workflow_edges FOR UPDATE
  USING (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_edges.workflow_id
    AND workflows.user_id = auth.uid()
  ));

CREATE POLICY "Users can delete edges in their workflows"
  ON public.workflow_edges FOR DELETE
  USING (EXISTS (
    SELECT 1 FROM public.workflows
    WHERE workflows.id = workflow_edges.workflow_id
    AND workflows.user_id = auth.uid()
  ));

-- RLS Policies for documents
CREATE POLICY "Users can view their own documents"
  ON public.documents FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own documents"
  ON public.documents FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own documents"
  ON public.documents FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own documents"
  ON public.documents FOR DELETE
  USING (auth.uid() = user_id);

-- RLS Policies for chat_history
CREATE POLICY "Users can view their own chat history"
  ON public.chat_history FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own chat messages"
  ON public.chat_history FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Create indexes for performance
CREATE INDEX idx_workflows_user_id ON public.workflows(user_id);
CREATE INDEX idx_workflow_nodes_workflow_id ON public.workflow_nodes(workflow_id);
CREATE INDEX idx_workflow_edges_workflow_id ON public.workflow_edges(workflow_id);
CREATE INDEX idx_documents_workflow_id ON public.documents(workflow_id);
CREATE INDEX idx_documents_user_id ON public.documents(user_id);
CREATE INDEX idx_chat_history_workflow_id ON public.chat_history(workflow_id);
CREATE INDEX idx_chat_history_created_at ON public.chat_history(created_at);

-- Create trigger function for updating updated_at timestamp
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = timezone('utc'::text, now());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for workflows
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON public.workflows
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_updated_at();