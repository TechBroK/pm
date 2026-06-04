# Kanban Studio

Kanban Studio is a local-first project management MVP with a Next.js frontend, a FastAPI backend, and a SQLite database. It lets users sign up, sign in, manage a single Kanban board, move cards across fixed columns, edit board content, and use an AI sidebar for project-management assistance.

The application is designed to run locally as one web app served from the FastAPI backend at `http://127.0.0.1:8000`.

## Features

- User signup and sign in
- Session-based authentication
- One Kanban board per user
- Fixed board columns that can be renamed
- Cards that can be created, edited, moved, and deleted
- Drag-and-drop card movement
- SQLite persistence
- AI sidebar backed by OpenRouter, with mock fallback when no API key is available
- Backend serves both API routes and the built static frontend
- Docker configuration for single-container deployment
- Start and stop scripts for Windows, macOS, and Linux

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- dnd-kit for drag and drop
- Vitest for unit tests
- Playwright for end-to-end tests

### Backend

- Python
- FastAPI
- Uvicorn
- SQLite
- httpx
- python-dotenv

### AI

- OpenRouter API
- Current implementation model: `openai/gpt-3.5-turbo`
- Project requirement target model: `openai/gpt-oss-120b`

## Project Structure

```text
.
+-- backend/
|   +-- ai_service.py        # OpenRouter integration and mock fallback
|   +-- db.py                # SQLite schema, seed data, and database operations
|   +-- kanban.db            # Local SQLite database
|   +-- main.py              # FastAPI app, API routes, static frontend serving
|   +-- requirements.txt     # Python dependencies
+-- docs/
|   +-- PLAN.md              # Main implementation plan and status
|   +-- DATABASE_SCHEMA.md   # Database design notes
|   +-- schema.json          # Schema reference
+-- frontend/
|   +-- src/app/             # Next.js app shell
|   +-- src/components/      # UI components
|   +-- src/lib/             # API, auth, and Kanban utilities
|   +-- tests/               # Playwright tests
|   +-- package.json         # Frontend scripts and dependencies
+-- scripts/
|   +-- start-backend.bat    # Windows start script
|   +-- start-backend.sh     # macOS/Linux start script
|   +-- stop-backend.bat     # Windows stop script
|   +-- stop-backend.sh      # macOS/Linux stop script
+-- Dockerfile
+-- docker-compose.yml
+-- README.md
```

## Requirements

- Python 3.11 or newer
- Node.js and npm
- Docker, optional
- OpenRouter API key, optional for AI live mode

The app can run without an OpenRouter key. In that case, AI endpoints return mock development responses.

## Environment Variables

Create a `.env` file in the project root when using AI live mode:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
ENVIRONMENT=development
```

`ENVIRONMENT` is optional. In development mode, the backend allows all CORS origins.

## Running Locally

Run these commands from the project root.

### Windows

```bat
scripts\start-backend.bat
```

### macOS or Linux

```bash
chmod +x scripts/start-backend.sh
./scripts/start-backend.sh
```

The start script:

1. Installs frontend dependencies.
2. Builds the Next.js static frontend.
3. Installs backend dependencies.
4. Starts FastAPI on `http://127.0.0.1:8000`.

Open the app at:

```text
http://127.0.0.1:8000
```

## Stopping The Server

### Windows

```bat
scripts\stop-backend.bat
```

### macOS or Linux

```bash
chmod +x scripts/stop-backend.sh
./scripts/stop-backend.sh
```

## Running The Frontend Only

This is useful for UI development, but API-backed features require the FastAPI backend.

```bash
cd frontend
npm install
npm run dev
```

By default, Next.js runs on:

```text
http://localhost:3000
```

## Running The Backend Manually

```bash
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Before serving the full frontend from the backend, build the frontend:

```bash
cd frontend
npm install
npm run build
cd ..
```

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

The app will be available at:

```text
http://localhost:8000
```

The compose file mounts `./backend` into the container so the SQLite database persists between restarts.

## Authentication

The app supports:

- Signup for new local test users
- Login for existing users
- Logout
- Session persistence in browser localStorage

The seeded default user is:

```text
Username: user
Password: password
```

Newly signed-up users automatically receive one board with five default columns:

- Backlog
- Discovery
- In Progress
- Review
- Done

Passwords are stored in the current MVP database field named `password_hash`, but they are not yet hashed. This is acceptable only for local MVP testing.

## Database

The SQLite database lives at:

```text
backend/kanban.db
```

The database is created automatically when the backend starts if it does not already exist.

Main tables:

- `users`: login accounts
- `boards`: one board per user for the MVP
- `columns`: fixed board columns
- `cards`: Kanban task cards
- `activity_log`: activity records for future workflow history

The schema is documented in:

```text
docs/DATABASE_SCHEMA.md
docs/schema.json
```

## API Overview

All API routes are served under `/api`.

### Auth

```http
POST /api/auth/signup
POST /api/auth/login
POST /api/auth/logout?session_id={session_id}
```

Signup and login request body:

```json
{
  "username": "user",
  "password": "password"
}
```

Successful response:

```json
{
  "session_id": "uuid-session-id",
  "username": "user"
}
```

### Board

```http
GET /api/board?session_id={session_id}
```

Returns the signed-in user's board, columns, and cards.

### Cards

```http
POST /api/board/cards?session_id={session_id}&column_id={column_id}
PUT /api/board/cards/{card_id}?session_id={session_id}
DELETE /api/board/cards/{card_id}?session_id={session_id}
```

Create card body:

```json
{
  "title": "Write launch notes",
  "details": "Draft concise release notes for the MVP.",
  "priority": "medium",
  "due_date": null,
  "assignee": null
}
```

Move card body:

```json
{
  "column_id": 3,
  "position": 0
}
```

Update card body:

```json
{
  "title": "Updated title",
  "details": "Updated details",
  "priority": "high",
  "due_date": "2026-06-30",
  "assignee": "Alex"
}
```

### Columns

```http
POST /api/board/columns/{column_id}?session_id={session_id}
```

Rename column body:

```json
{
  "title": "In Review"
}
```

### AI

```http
GET /api/ai/test
POST /api/ai/ask?session_id={session_id}&question={question}
```

The AI service uses OpenRouter when `OPENROUTER_API_KEY` is configured. Without a key, it returns mock responses for local development.

### Health

```http
GET /health
GET /api/test
```

## Testing

Run frontend unit tests:

```bash
cd frontend
npm run test:unit
```

Run end-to-end tests:

```bash
cd frontend
npm run test:e2e
```

Run all frontend tests:

```bash
cd frontend
npm run test:all
```

Run a Python syntax check for backend files:

```bash
python -m py_compile backend/main.py backend/db.py backend/ai_service.py
```

## Build Notes

The frontend uses `next/font/google` for Manrope and Space Grotesk. A production build requires network access to fetch those fonts unless the fonts are changed to local assets.

If `npm run build` fails with a Google Fonts fetch error, the root cause is network access rather than application code.

## Current Limitations

- Passwords are not hashed yet.
- Sessions are stored in memory, so they reset when the backend restarts.
- The SQLite database is local to the machine or container volume.
- The MVP supports one board per user.
- AI board-editing behavior is still limited and partially mocked depending on OpenRouter access.
- The project requirement names `openai/gpt-oss-120b`, but the current code uses `openai/gpt-3.5-turbo`.
- Full lint currently scans generated output unless the command is scoped to source files.

## Development Notes

- Read `docs/PLAN.md` before starting new feature work.
- Keep changes small and aligned with the existing frontend and backend patterns.
- Prefer the existing API client in `frontend/src/lib/api.ts` for frontend/backend calls.
- Prefer `DatabaseOps` in `backend/db.py` for database changes.
- Keep documentation in `docs/` for planning and implementation notes.
