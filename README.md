# AI-planet-Assignment

No-Code AI Workflow Builder with React frontend and FastAPI backend.

## 🏗️ Architecture

- **Frontend**: React 18 + TypeScript + Vite (Port 8080)
- **Backend**: FastAPI + Python 3.9+ (Port 8000)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Vector Store**: ChromaDB
- **LLM**: OpenAI GPT-4 / GPT-3.5

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- (Optional) PostgreSQL database
- (Optional) OpenAI API key for LLM features

### 1. Clone and Install

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 2. Configure Environment

**Frontend** - Create `.env` in project root:
```bash
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_URL=http://localhost:8000
```

**Backend** - Create `backend/.env`:
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```env
# Database (leave empty for SQLite)
DATABASE_URL=

# OpenAI API Key (optional for testing)
OPENAI_API_KEY=your_openai_api_key_here

# CORS Origins
CORS_ORIGINS=http://localhost:8080,http://localhost:5173
```

**Note**: The backend will automatically use SQLite (`workflow_db.sqlite`) if `DATABASE_URL` is empty.

### 3. Run Development Servers

**Option A: Run Both Servers Together** (Recommended)
```bash
npm run dev:all
```

**Option B: Run Separately**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

Terminal 2 - Frontend:
```bash
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Testing

### Backend Tests
```bash
# Run all backend tests
npm run test:backend

# Or run directly with pytest
cd backend
pytest tests/ -v
```

### Manual API Testing

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Create Workflow:**
```bash
curl -X POST http://localhost:8000/api/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Workflow",
    "user_id": "00000000-0000-0000-0000-000000000001",
    "nodes": [],
    "edges": []
  }'
```

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy models and DB config
│   ├── requirements.txt     # Python dependencies
│   ├── routers/             # API endpoints
│   │   ├── workflows.py     # Workflow CRUD
│   │   ├── chat.py          # Chat interface
│   │   ├── documents.py     # Document processing
│   │   └── llm.py           # LLM integration
│   ├── services/            # Business logic
│   │   ├── workflow_executor.py
│   │   ├── llm_service.py
│   │   ├── vector_store.py
│   │   └── document_processor.py
│   └── tests/               # Backend tests
│       └── test_api.py
├── src/
│   ├── components/          # React components
│   │   ├── WorkflowBuilder.tsx
│   │   ├── ChatInterface.tsx
│   │   ├── BackendStatus.tsx
│   │   └── ui/              # Shadcn UI components
│   ├── lib/
│   │   └── api.ts           # Backend API client
│   └── pages/
│       └── Index.tsx
├── package.json             # Frontend dependencies & scripts
└── README.md
```

## 🔧 Development

### Backend Development

- **Auto-reload**: The backend uses `uvicorn` with `--reload` flag
- **Add new endpoint**: Create in `backend/routers/`
- **Database changes**: Models are in `backend/database.py`
- **Run tests**: `cd backend && pytest tests/`

### Frontend Development

- **Hot reload**: Vite provides instant HMR
- **API calls**: Use `src/lib/api.ts` client
- **Lint**: `npm run lint`

## 🐛 Troubleshooting

### Backend won't start

**Issue**: `ModuleNotFoundError` or import errors

**Solution**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: Database connection error

**Solution**: Make sure `DATABASE_URL` is empty in `backend/.env` to use SQLite.

### Frontend shows "Backend Not Connected"

**Issue**: Backend not running or wrong port

**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify `.env` has `VITE_API_URL=http://localhost:8000`
3. Restart frontend: `npm run dev`

### CORS errors

**Issue**: Browser blocks requests from frontend to backend

**Solution**: Ensure `backend/.env` has:
```env
CORS_ORIGINS=http://localhost:8080,http://localhost:5173
```

### OpenAI API errors

**Issue**: "OpenAI API key not configured"

**Solution**: Add your OpenAI API key to `backend/.env`:
```env
OPENAI_API_KEY=sk-...
```

Note: You can use the app without OpenAI - only LLM features will be disabled.

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /health` - Health check
- `POST /api/workflows` - Create workflow
- `GET /api/workflows/{id}` - Get workflow
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow
- `POST /api/chat/message` - Send chat message
- `GET /api/chat/history/{workflow_id}` - Get chat history
- `POST /api/documents/upload` - Upload document
- `GET /api/llm/models` - List available LLM models

## 🚢 Production Deployment

### Backend

1. Set `DATABASE_URL` to PostgreSQL connection string
2. Set production `OPENAI_API_KEY`
3. Deploy with Docker or directly:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
npm run build
# Serve dist/ folder with any static host
```

## 📝 License

MIT

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and test
3. Commit: `git commit -m "feat: add my feature"`
4. Push and create PR

---

**Built with** ❤️ **using React, FastAPI, and OpenAI**
