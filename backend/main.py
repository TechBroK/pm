#!/usr/bin/env python
"""
Project Management MVP Backend
FastAPI application serving frontend and API endpoints
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv
from backend.db import Database, DatabaseOps
from backend.ai_service import AIService

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="PM Backend", version="0.1.0")

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Initializing database...")
    Database.init()
    Database.seed_data()
    logger.info("Database initialized successfully")


# Session management (simple in-memory for MVP)
sessions: Dict[str, int] = {}  # session_id -> user_id


def get_current_user_id(session_id: Optional[str] = None) -> int:
    """Get current user ID from session"""
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return sessions[session_id]


# Models
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_id: str
    username: str


class CardRequest(BaseModel):
    title: str
    details: Optional[str] = None


class CardPositionRequest(BaseModel):
    column_id: int
    position: int


class ColumnRenameRequest(BaseModel):
    title: str


# API Endpoints

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """Authenticate user with hardcoded credentials"""
    # MVP: hardcoded user/password
    if request.username == "user" and request.password == "password":
        user = DatabaseOps.get_user_by_username(request.username)
        if user:
            # Create session
            import uuid
            session_id = str(uuid.uuid4())
            sessions[session_id] = user.id
            
            return LoginResponse(session_id=session_id, username=user.username)
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/api/auth/logout")
async def logout(session_id: Optional[str] = None):
    """Logout user and clear session"""
    if session_id and session_id in sessions:
        del sessions[session_id]
    
    return JSONResponse({"message": "Logged out"})


@app.get("/api/board")
async def get_board(session_id: Optional[str] = None):
    """Get current user's board with all columns and cards"""
    user_id = get_current_user_id(session_id)
    
    board = DatabaseOps.get_board(user_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    return board


@app.post("/api/board/cards")
async def add_card(request: CardRequest, session_id: Optional[str] = None, column_id: int = None):
    """Add new card to column"""
    user_id = get_current_user_id(session_id)
    
    if not column_id:
        raise HTTPException(status_code=400, detail="column_id required")
    
    try:
        card = DatabaseOps.add_card(column_id, request.title, request.details)
        return {
            "id": card.id,
            "column_id": card.column_id,
            "title": card.title,
            "details": card.details,
            "position": card.position,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/board/cards/{card_id}")
async def move_card(card_id: int, request: CardPositionRequest, session_id: Optional[str] = None):
    """Move card to new column/position"""
    user_id = get_current_user_id(session_id)
    
    try:
        card = DatabaseOps.update_card(card_id, request.column_id, request.position)
        return {
            "id": card.id,
            "column_id": card.column_id,
            "title": card.title,
            "details": card.details,
            "position": card.position,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/board/cards/{card_id}")
async def delete_card(card_id: int, session_id: Optional[str] = None):
    """Delete card"""
    user_id = get_current_user_id(session_id)
    
    if DatabaseOps.delete_card(card_id):
        return JSONResponse({"message": "Card deleted"})
    
    raise HTTPException(status_code=404, detail="Card not found")


@app.post("/api/board/columns/{column_id}")
async def rename_column(column_id: int, request: ColumnRenameRequest, session_id: Optional[str] = None):
    """Rename column"""
    user_id = get_current_user_id(session_id)
    
    try:
        column = DatabaseOps.rename_column(column_id, request.title)
        return {
            "id": column.id,
            "board_id": column.board_id,
            "title": column.title,
            "position": column.position,
            "created_at": column.created_at,
            "updated_at": column.updated_at,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working"""
    return JSONResponse({"message": "Hello from API"})


@app.get("/api/ai/test")
async def test_ai_connection():
    """Test OpenRouter connection with a simple prompt"""
    result = AIService.test_connection()
    return JSONResponse(result)


@app.post("/api/ai/ask")
async def ask_ai(question: str, session_id: Optional[str] = None):
    """Ask AI a question about the Kanban board"""
    user_id = get_current_user_id(session_id)
    
    board = DatabaseOps.get_board(user_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    result = AIService.ask_about_board("", board, question)
    return JSONResponse(result)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({"status": "ok"})


# Determine frontend build path
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
frontend_dist = project_root / "frontend" / "dist"

logger.info(f"Frontend dist path: {frontend_dist}")

# Mount Next.js static assets
if frontend_dist.exists():
    logger.info("Mounting Next.js static files from frontend/dist")
    app.mount("/_next", StaticFiles(directory=frontend_dist / "_next"), name="next-static")
    
    # Mount all static files from dist
    try:
        app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
        logger.info("Successfully mounted frontend from frontend/dist")
    except Exception as e:
        logger.error(f"Failed to mount frontend: {e}")
else:
    logger.warning(f"Frontend dist not found at {frontend_dist}")
    logger.warning("Run 'npm run build' in frontend/ directory to build the frontend")


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting PM Backend server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
