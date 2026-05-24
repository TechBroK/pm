# Backend Architecture Documentation

## Overview

The PM backend is a FastAPI application that serves the frontend and provides API endpoints for Kanban board management and AI chat functionality. The current implementation (Part 2) provides hello world serving and basic API structure.

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── static/             # Static files (HTML, CSS, JS)
│   └── index.html      # Hello world landing page
├── AGENTS.md           # This file
└── [future modules]
```

## Current Status (Part 2)

### ✅ Implemented

- **FastAPI Application** (`main.py`)
  - Serves static files at root (`/`)
  - Provides `/api/test` endpoint
  - Provides `/health` endpoint for monitoring
  - Configured with proper logging

- **Static HTML** (`static/index.html`)
  - Styled hello world landing page
  - Verifies server is running
  - Links to test API endpoint

- **Dependencies** (`requirements.txt`)
  - FastAPI 0.104.1
  - Uvicorn 0.24.0
  - Python-multipart 0.0.6

- **Server Management**
  - Start/stop scripts for Windows (`.bat`)
  - Start/stop scripts for Linux/macOS (`.sh`)
  - Server runs on `http://127.0.0.1:8000`

## API Endpoints (Current)

### GET /

- **Purpose**: Serve static HTML
- **Response**: HTML page
- **Status**: ✅ Working

### GET /api/test

- **Purpose**: Test API connectivity
- **Response**: `{"message": "Hello from API"}`
- **Status Code**: 200
- **Status**: ✅ Working

### GET /health

- **Purpose**: Health check for monitoring
- **Response**: `{"status": "ok"}`
- **Status Code**: 200
- **Status**: ✅ Working

## Key Dependencies

| Package          | Version | Purpose           |
| ---------------- | ------- | ----------------- |
| FastAPI          | 0.104.1 | Web framework     |
| Uvicorn          | 0.24.0  | ASGI server       |
| python-multipart | 0.0.6   | Form data parsing |

## Running the Backend

### Option 1: Using Scripts

**Windows:**

```bash
.\scripts\start-backend.bat
```

**Linux/macOS:**

```bash
./scripts/start-backend.sh
```

### Option 2: Direct Command

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Access Points

- **Frontend**: http://127.0.0.1:8000/
- **API Test**: http://127.0.0.1:8000/api/test
- **Health Check**: http://127.0.0.1:8000/health

## Architecture Overview

### Current Stack

```
Request → Uvicorn (ASGI Server)
            ↓
        FastAPI App
            ↓
        Route Handler
            ↓
        Response (JSON or HTML)
```

### Future Stack (Parts 3-10)

```
Request → Uvicorn
            ↓
        FastAPI App
            ↓
        Auth Middleware
            ↓
        Route Handler
            ├─ Database Layer (SQLite)
            ├─ API Logic Layer
            └─ AI Service Layer
            ↓
        Response (JSON)
```

## Code Organization Plan (Future Parts)

### Part 3: Frontend Integration

- Configure static file serving for built Next.js app
- Set up route fallback for SPA

### Part 4: Authentication

- Add `auth.py` module for auth logic
- Add auth middleware

### Part 5-6: Database & API

- Add `db.py` module for database operations
- Add `models.py` for SQLAlchemy/dataclass models
- Add `api/` directory for route grouping
  - `api/board.py` - Board endpoints
  - `api/auth.py` - Auth endpoints
  - `api/chat.py` - Chat endpoints

### Part 8-10: AI Integration

- Add `ai_service.py` for OpenRouter integration
- Add structured response handling
- Add chat history management

## Testing Strategy (Future)

**Backend Unit Tests** (pytest):

- Database operations
- API endpoint logic
- Auth validation
- AI response parsing

**Integration Tests**:

- Auth flow + board operations
- API + database interaction
- Frontend + backend data flow

**Target Coverage**: 80%+

## Environment Setup

### System Requirements

- Python 3.11+
- pip or uv package manager

### Installation

```bash
cd backend
pip install -r requirements.txt
```

## Logging

Current logging level: `INFO`

**Log Output**:

- Server startup/shutdown events
- HTTP request details
- Request status codes

## Error Handling (Future)

Planned error handling:

- Database connection failures
- Authentication errors (401, 403)
- Validation errors (422)
- Not found errors (404)
- Server errors (500)

All errors returned as JSON with proper HTTP status codes.

## Performance Considerations

**Current**:

- Static file serving (optimized by FastAPI)
- Direct route handling

**Future**:

- Database query optimization (indexes)
- Connection pooling (SQLite)
- Caching for AI responses
- Rate limiting for API
- Pagination for large datasets

## Security Considerations (Future)

- Session management
- CORS configuration
- Input validation and sanitization
- SQL injection prevention
- API key management (OpenRouter)

## Next Steps

1. **Part 3**: Serve built Next.js frontend from backend
2. **Part 4**: Add authentication middleware and endpoints
3. **Part 5**: Database schema design and approval
4. **Part 6**: Implement database layer and API endpoints
5. **Part 7**: Frontend-backend integration
6. **Parts 8-10**: AI integration and chat features

## Development Notes

- Server uses `--reload` flag for auto-restart on code changes
- Static files mounted at root to serve React app
- API routes prefixed with `/api/` for separation
- All responses use JSON format except for static HTML
