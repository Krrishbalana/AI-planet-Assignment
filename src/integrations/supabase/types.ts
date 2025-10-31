export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.5";
  };
  public: {
    Tables: {
      chat_history: {
        Row: {
          created_at: string;
          id: string;
          message: string;
          role: string;
          user_id: string | null;
          workflow_id: string;
        };
        Insert: {
          created_at?: string;
          id?: string;
          message: string;
          role: string;
          user_id?: string | null;
          workflow_id: string;
        };
        Update: {
          created_at?: string;
          id?: string;
          message?: string;
          role?: string;
          user_id?: string | null;
          workflow_id?: string;
        };
        Relationships: [
          {
            foreignKeyName: "chat_history_workflow_id_fkey";
            columns: ["workflow_id"];
            isOneToOne: false;
            referencedRelation: "workflows";
            referencedColumns: ["id"];
          }
        ];
      };
      documents: {
        Row: {
          created_at: string;
          embedding_count: number | null;
          file_path: string;
          file_size: number | null;
          filename: string;
          id: string;
          mime_type: string | null;
          processed: boolean | null;
          user_id: string | null;
          workflow_id: string | null;
        };
        Insert: {
          created_at?: string;
          embedding_count?: number | null;
          file_path: string;
          file_size?: number | null;
          filename: string;
          id?: string;
          mime_type?: string | null;
          processed?: boolean | null;
          user_id?: string | null;
          workflow_id?: string | null;
        };
        Update: {
          created_at?: string;
          embedding_count?: number | null;
          file_path?: string;
          file_size?: number | null;
          filename?: string;
          id?: string;
          mime_type?: string | null;
          processed?: boolean | null;
          user_id?: string | null;
          workflow_id?: string | null;
        };
        Relationships: [
          {
            foreignKeyName: "documents_workflow_id_fkey";
            columns: ["workflow_id"];
            isOneToOne: false;
            referencedRelation: "workflows";
            referencedColumns: ["id"];
          }
        ];
      };
      workflow_edges: {
        Row: {
          created_at: string;
          edge_id: string;
          id: string;
          source_node_id: string;
          target_node_id: string;
          workflow_id: string;
        };
        Insert: {
          created_at?: string;
          edge_id: string;
          id?: string;
          source_node_id: string;
          target_node_id: string;
          workflow_id: string;
        };
        Update: {
          created_at?: string;
          edge_id?: string;
          id?: string;
          source_node_id?: string;
          target_node_id?: string;
          workflow_id?: string;
        };
        Relationships: [
          {
            foreignKeyName: "workflow_edges_workflow_id_fkey";
            columns: ["workflow_id"];
            isOneToOne: false;
            referencedRelation: "workflows";
            referencedColumns: ["id"];
          }
        ];
      };
      workflow_nodes: {
        Row: {
          config: Json | null;
          created_at: string;
          id: string;
          node_id: string;
          node_type: string;
          position_x: number;
          position_y: number;
          workflow_id: string;
        };
        Insert: {
          config?: Json | null;
          created_at?: string;
          id?: string;
          node_id: string;
          node_type: string;
          position_x: number;
          position_y: number;
          workflow_id: string;
        };
        Update: {
          config?: Json | null;
          created_at?: string;
          id?: string;
          node_id?: string;
          node_type?: string;
          position_x?: number;
          position_y?: number;
          workflow_id?: string;
        };
        Relationships: [
          {
            foreignKeyName: "workflow_nodes_workflow_id_fkey";
            columns: ["workflow_id"];
            isOneToOne: false;
            referencedRelation: "workflows";
            referencedColumns: ["id"];
          }
        ];
      };
      workflows: {
        Row: {
          created_at: string;
          description: string | null;
          id: string;
          is_valid: boolean | null;
          name: string;
          updated_at: string;
          user_id: string | null;
        };
        Insert: {
          created_at?: string;
          description?: string | null;
          id?: string;
          is_valid?: boolean | null;
          name: string;
          updated_at?: string;
          user_id?: string | null;
        };
        Update: {
          created_at?: string;
          description?: string | null;
          id?: string;
          is_valid?: boolean | null;
          name?: string;
          updated_at?: string;
          user_id?: string | null;
        };
        Relationships: [];
      };
    };
    Views: {
      [_ in never]: never;
    };
    Functions: {
      [_ in never]: never;
    };
    Enums: {
      [_ in never]: never;
    };
    CompositeTypes: {
      [_ in never]: never;
    };
  };
};

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">;

type DefaultSchema = DatabaseWithoutInternals[Extract<
  keyof Database,
  "public"
>];

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals;
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals;
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R;
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
      DefaultSchema["Views"])
  ? (DefaultSchema["Tables"] &
      DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
      Row: infer R;
    }
    ? R
    : never
  : never;

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals;
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals;
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I;
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
  ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
      Insert: infer I;
    }
    ? I
    : never
  : never;

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals;
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals;
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U;
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
  ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
      Update: infer U;
    }
    ? U
    : never
  : never;

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals;
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals;
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
  ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
  : never;

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals;
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals;
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
  ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
  : never;

export const Constants = {
  public: {
    Enums: {},
  },
} as const;
