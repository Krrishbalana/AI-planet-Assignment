/**
 * API Client for Backend Communication
 * Centralized HTTP client with error handling
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface ApiError {
  message: string;
  detail?: string;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error: ApiError = await response.json().catch(() => ({
          message: `HTTP ${response.status}: ${response.statusText}`,
        }));
        throw new Error(error.detail || error.message || "API request failed");
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error("An unexpected error occurred");
    }
  }

  // Health check
  async healthCheck() {
    return this.request<{ status: string }>("/health");
  }

  // Workflow APIs
  async createWorkflow(data: {
    name: string;
    description?: string;
    user_id: string;
    nodes: any[];
    edges: any[];
    is_valid?: boolean;
  }) {
    return this.request<{ id: string; message: string }>("/api/workflows", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getWorkflow(workflowId: string) {
    return this.request(`/api/workflows/${workflowId}`);
  }

  async updateWorkflow(workflowId: string, data: any) {
    return this.request<{ message: string }>(`/api/workflows/${workflowId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteWorkflow(workflowId: string) {
    return this.request<{ message: string }>(`/api/workflows/${workflowId}`, {
      method: "DELETE",
    });
  }

  async listUserWorkflows(userId: string) {
    return this.request<any[]>(`/api/workflows/user/${userId}`);
  }

  // Chat APIs
  async sendMessage(data: {
    workflow_id: string;
    user_id: string;
    message: string;
  }) {
    return this.request<{ response: string; sources: string[] }>(
      "/api/chat/message",
      {
        method: "POST",
        body: JSON.stringify(data),
      }
    );
  }

  async getChatHistory(workflowId: string, limit: number = 50) {
    return this.request<any[]>(
      `/api/chat/history/${workflowId}?limit=${limit}`
    );
  }

  async clearChatHistory(workflowId: string) {
    return this.request<{ message: string }>(
      `/api/chat/history/${workflowId}`,
      {
        method: "DELETE",
      }
    );
  }

  // LLM APIs
  async generateLLM(data: {
    prompt: string;
    model?: string;
    temperature?: number;
    max_tokens?: number;
    system_prompt?: string;
    context?: string[];
  }) {
    return this.request<{ response: string; model: string; tokens_used: number }>(
      "/api/llm/generate",
      {
        method: "POST",
        body: JSON.stringify(data),
      }
    );
  }

  async listModels() {
    return this.request<{ models: any[] }>("/api/llm/models");
  }

  // Document APIs
  async uploadDocument(
    file: File,
    workflowId?: string,
    userId?: string
  ) {
    const formData = new FormData();
    formData.append("file", file);
    if (workflowId) formData.append("workflow_id", workflowId);
    if (userId) formData.append("user_id", userId);

    const url = `${this.baseURL}/api/documents/upload`;
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        message: "Upload failed",
      }));
      throw new Error(error.detail || error.message);
    }

    return await response.json();
  }

  async processDocument(documentId: string) {
    return this.request<{ message: string; chunks: number }>(
      `/api/documents/${documentId}/process`,
      {
        method: "POST",
      }
    );
  }

  async getDocument(documentId: string) {
    return this.request(`/api/documents/${documentId}`);
  }

  async listWorkflowDocuments(workflowId: string) {
    return this.request<any[]>(`/api/documents/workflow/${workflowId}`);
  }

  async deleteDocument(documentId: string) {
    return this.request<{ message: string }>(`/api/documents/${documentId}`, {
      method: "DELETE",
    });
  }
}

// Export singleton instance
export const api = new ApiClient(API_BASE_URL);

// Export types for convenience
export type { ApiError };
