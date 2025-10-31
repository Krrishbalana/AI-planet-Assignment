# Workflow Builder - Backend API

FastAPI backend for the No-Code Workflow Builder application.

## Features

- **Workflow Management**: Create, read, update, delete AI workflows
- **Document Processing**: Upload and process PDFs with PyMuPDF
- **Vector Store**: ChromaDB for semantic search
- **LLM Integration**: OpenAI GPT-4, GPT-3.5, Gemini support
- **Chat Interface**: Execute workflows with natural language queries

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Vector Store**: ChromaDB
- **Document Processing**: PyMuPDF
- **LLM**: OpenAI, Google Gemini
- **Embeddings**: OpenAI text-embedding-ada-002

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL database
- OpenAI API key

### Installation

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/workflow_db
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key_optional
```

4. Create the database:

```bash
createdb workflow_db
```

5. Run the server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── database.py             # Database models and connection
├── requirements.txt        # Python dependencies
├── routers/
│   ├── workflows.py        # Workflow CRUD endpoints
│   ├── documents.py        # Document upload/processing
│   ├── chat.py             # Chat interface endpoints
│   └── llm.py              # LLM integration endpoints
└── services/
    ├── document_processor.py    # PDF text extraction
    ├── vector_store.py          # ChromaDB operations
    ├── llm_service.py           # LLM provider integrations
    └── workflow_executor.py     # Workflow execution logic
```

## API Endpoints

### Workflows

- `POST /api/workflows` - Create workflow
- `GET /api/workflows/{id}` - Get workflow
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow

### Documents

- `POST /api/documents/upload` - Upload document
- `POST /api/documents/{id}/process` - Process document
- `GET /api/documents/{id}` - Get document info

### Chat

- `POST /api/chat/message` - Send message to workflow
- `GET /api/chat/history/{workflow_id}` - Get chat history

### LLM

- `POST /api/llm/generate` - Generate LLM response
- `GET /api/llm/models` - List available models

## Database Schema

The database uses the same schema as defined in the frontend's Supabase migrations:

- `workflows` - Workflow definitions
- `workflow_nodes` - Individual components
- `workflow_edges` - Component connections
- `documents` - Uploaded files
- `chat_history` - Conversation logs

## Development

Run with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docker Deployment (Optional)

Build and run with Docker:

```bash
docker build -t workflow-backend .
docker run -p 8000:8000 --env-file .env workflow-backend
```

## Contributing

This backend is designed to work alongside the React frontend. Ensure CORS settings allow the frontend origin.
