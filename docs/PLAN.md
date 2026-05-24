# Project Management MVP - Detailed Implementation Plan

## Overview

Building a Project Management App MVP with NextJS frontend, Python FastAPI backend, and SQLite database. The app enables users to sign in, manage Kanban boards, move cards via drag-and-drop, and interact with an AI assistant for board management.

---

## Part 1: Planning & Documentation

**Objective:** Complete detailed planning for all 10 parts, document existing frontend code, and get user approval.

### Substeps

- [ ] Document existing frontend architecture in `frontend/AGENTS.md`
  - [ ] List all components with brief descriptions
  - [ ] Document data structures and state management
  - [ ] List test patterns currently in use
  - [ ] Identify any gaps or TODOs
  
- [ ] Create detailed implementation plan for Parts 2-10 (this document)
  - [ ] Break down each part into actionable substeps
  - [ ] Define success criteria for each part
  - [ ] Estimate dependencies between parts
  
- [ ] Get user approval on plan and frontend documentation
  - [ ] Review with user
  - [ ] Incorporate feedback
  - [ ] Proceed only with explicit approval

### Success Criteria

- [ ] `frontend/AGENTS.md` exists with complete component documentation
- [ ] All 10 parts have substeps, checklists, and success criteria defined
- [ ] User has reviewed and approved the plan
- [ ] No blockers or ambiguities remain

---

## Part 2: Backend Scaffolding & Hello World

**Objective:** Set up FastAPI backend infrastructure and verify it can serve static HTML and make a test API call.

### Prerequisites

- Part 1 approved

### Substeps

- [ ] Create Python FastAPI project structure in `backend/`
  - [ ] Create `main.py` with FastAPI app
  - [ ] Create `requirements.txt` with FastAPI, uvicorn, and essential dependencies
  - [ ] Set up project with Python 3.11+ and `uv` as package manager
  
- [ ] Create a static HTML hello world page
  - [ ] Create `backend/static/index.html` with simple hello world content
  - [ ] Configure FastAPI to serve static files from `/static`
  - [ ] Verify serving at `/` (root)
  
- [ ] Create a simple test API endpoint
  - [ ] Create `GET /api/test` endpoint returning `{"message": "Hello from API"}`
  - [ ] Test endpoint returns correct JSON
  
- [ ] Create backend start/stop scripts in `scripts/`
  - [ ] Create `scripts/start-backend.sh` (Linux/Mac)
  - [ ] Create `scripts/start-backend.bat` (Windows)
  - [ ] Create `scripts/stop-backend.sh` (Linux/Mac)
  - [ ] Create `scripts/stop-backend.bat` (Windows)
  - [ ] Scripts should manage uvicorn server lifecycle
  
- [ ] Test locally
  - [ ] Start backend server
  - [ ] Access static HTML at `http://localhost:8000/`
  - [ ] Call API at `http://localhost:8000/api/test` and verify response
  - [ ] Stop backend server

### Success Criteria

- [ ] Backend server starts and stops cleanly via scripts
- [ ] Static HTML serves at root path
- [ ] API endpoint responds with correct JSON
- [ ] No errors in server logs
- [ ] Server handles graceful shutdown

### Testing Strategy

- Manual testing of endpoints via curl/browser
- Log output verification
- No automated tests required at this stage

---

## Part 3: Integrate Frontend Build & Serving

**Objective:** Build the NextJS frontend and serve it statically from the backend. The app displays the Kanban board at `/`.

### Prerequisites

- Part 2 complete
- Frontend dependencies installed

### Substeps

- [ ] Build NextJS frontend
  - [ ] Run `npm run build` in `frontend/` directory
  - [ ] Verify build output in `frontend/.next/`
  - [ ] Verify standalone output is created
  
- [ ] Configure backend to serve built frontend
  - [ ] Create endpoint to serve static frontend files
  - [ ] Configure trailing slash handling
  - [ ] Set up route fallback to `index.html` for SPA routing
  
- [ ] Update start scripts to build and serve frontend
  - [ ] Modify backend start scripts to build frontend first
  - [ ] Start backend with frontend already built
  
- [ ] Test end-to-end
  - [ ] Start backend via script
  - [ ] Access Kanban board at `http://localhost:8000/`
  - [ ] Verify all assets load (CSS, JS)
  - [ ] Verify no CORS or asset loading errors
  - [ ] Test Kanban functionality (drag/drop, add cards, etc.)

### Success Criteria

- [ ] Frontend builds without errors
- [ ] Backend serves built frontend at root
- [ ] All assets (CSS, JS, images) load correctly
- [ ] Kanban board is fully interactive
- [ ] No 404 errors for assets
- [ ] Network requests show `http://localhost:8000/` as root

### Testing Strategy

- Manual e2e testing: UI interaction, asset loading
- Browser dev tools: verify network requests, no errors
- Existing frontend unit tests should still pass

---

## Part 4: Implement User Sign-in

**Objective:** Add hardcoded user authentication. Users must sign in with `user`/`password` to access the Kanban board.

### Prerequisites

- Part 3 complete
- Existing frontend tests passing

### Substeps

- [ ] Design authentication flow
  - [ ] Create login page component
  - [ ] Plan state management for auth (session storage/context)
  - [ ] Design logged-in vs logged-out UI states
  
- [ ] Create login UI component
  - [ ] Build `LoginPage.tsx` with username/password form
  - [ ] Add form validation (both fields required)
  - [ ] Style according to color scheme
  - [ ] Add error message display for failed login
  
- [ ] Implement authentication logic
  - [ ] Create auth context with hardcoded credentials
  - [ ] Implement login handler (check `user`/`password`)
  - [ ] Implement logout handler
  - [ ] Implement session persistence (localStorage or sessionStorage)
  - [ ] Protect Kanban route - redirect to login if not authenticated
  
- [ ] Add logout functionality
  - [ ] Create logout button in Kanban header
  - [ ] Clear session on logout
  - [ ] Redirect to login page after logout
  
- [ ] Test authentication flow
  - [ ] Verify login page shows on initial load
  - [ ] Test with correct credentials - should redirect to Kanban
  - [ ] Test with incorrect credentials - should show error and stay on login
  - [ ] Test logout - should clear session and redirect to login
  - [ ] Test session persistence - refresh page should keep session if valid
  
- [ ] Update tests
  - [ ] Add login flow tests
  - [ ] Add protected route tests
  - [ ] Ensure existing Kanban tests still pass
  - [ ] Add e2e tests for auth flow (Playwright)

### Success Criteria

- [ ] Unauthenticated users see login page
- [ ] Login with `user`/`password` grants access
- [ ] Login with wrong credentials shows error
- [ ] Logout clears session and shows login page
- [ ] Session persists across page refreshes
- [ ] All auth-related unit tests pass (80%+ coverage)
- [ ] E2E tests verify entire auth flow
- [ ] No console errors

### Testing Strategy

- Unit tests for auth context logic
- Component tests for login/logout UI
- E2E tests (Playwright) for complete auth flow
- Target 80%+ code coverage for auth modules

---

## Part 5: Design & Approve Database Schema

**Objective:** Design SQLite database schema to support users, boards, columns, and cards. Document the schema and get user approval.

### Substeps

- [ ] Design database schema
  - [ ] Users table: `id (PK), username (unique), password_hash, created_at`
  - [ ] Boards table: `id (PK), user_id (FK), title, created_at, updated_at`
  - [ ] Columns table: `id (PK), board_id (FK), title, position, created_at, updated_at`
  - [ ] Cards table: `id (PK), column_id (FK), title, details, position, created_at, updated_at`
  - [ ] Define relationships and constraints
  - [ ] Consider indexes for performance (user_id, board_id, column_id)
  
- [ ] Create schema documentation
  - [ ] Document in `docs/DATABASE_SCHEMA.md`
  - [ ] Include ER diagram (Mermaid or similar)
  - [ ] List all tables, columns, types, and relationships
  - [ ] Document any business rules (e.g., cascade deletes)
  - [ ] Save schema as JSON in `docs/schema.json`
  
- [ ] Plan database initialization
  - [ ] Design migration/initialization function
  - [ ] Plan how DB creates on startup if missing
  - [ ] Plan schema versioning strategy
  
- [ ] Get user approval
  - [ ] Share documentation with user
  - [ ] Incorporate feedback
  - [ ] Confirm schema design is correct before implementation

### Success Criteria

- [ ] `docs/DATABASE_SCHEMA.md` exists with detailed documentation
- [ ] `docs/schema.json` contains schema in JSON format
- [ ] ER diagram is clear and accurate
- [ ] User has reviewed and approved the schema
- [ ] Schema supports MVP requirements (1 user, 1 board per user)
- [ ] Schema is normalized and avoids redundancy

---

## Part 6: Implement Backend Database & API

**Objective:** Implement SQLite database initialization, data models, and API endpoints for reading/writing Kanban data.

### Prerequisites

- Part 5 approved

### Substeps

- [ ] Set up database layer
  - [ ] Create `backend/db.py` with SQLite connection management
  - [ ] Implement database initialization function (create tables if missing)
  - [ ] Create data models/classes (User, Board, Column, Card)
  - [ ] Implement database context manager for transactions
  
- [ ] Create database utilities
  - [ ] Implement CRUD operations for all models
  - [ ] Create query functions for board state retrieval
  - [ ] Implement data validation
  
- [ ] Add seed data for testing
  - [ ] Create function to populate test user and sample board
  - [ ] Make seeding optional (for development)
  
- [ ] Implement API endpoints
  - [ ] `POST /api/auth/login` - Authenticate user (for now, hardcoded)
  - [ ] `POST /api/auth/logout` - Clear session
  - [ ] `GET /api/board` - Get current user's board with all columns and cards
  - [ ] `PUT /api/board` - Update entire board state (columns and card positions)
  - [ ] `POST /api/board/columns/{columnId}` - Rename column
  - [ ] `POST /api/board/cards` - Add new card to column
  - [ ] `PUT /api/board/cards/{cardId}` - Update card
  - [ ] `DELETE /api/board/cards/{cardId}` - Delete card
  - [ ] All endpoints require authentication (session check)
  
- [ ] Add error handling
  - [ ] Handle database errors gracefully
  - [ ] Return appropriate HTTP status codes
  - [ ] Return error messages as JSON
  
- [ ] Add database tests
  - [ ] Test database initialization
  - [ ] Test CRUD operations for all models
  - [ ] Test transaction handling
  - [ ] Test data validation
  
- [ ] Test API endpoints
  - [ ] Unit tests for all endpoints
  - [ ] Test authentication requirement
  - [ ] Test board state persistence
  - [ ] Test data validation
  - [ ] Test error cases

### Success Criteria

- [ ] Database initializes on first run
- [ ] All CRUD endpoints work correctly
- [ ] Authentication is enforced on protected endpoints
- [ ] Board state persists across restarts
- [ ] API returns correct HTTP status codes
- [ ] Error responses are clear and JSON-formatted
- [ ] Database tests have 80%+ coverage
- [ ] API endpoint tests have 80%+ coverage
- [ ] No data loss on server restart

### Testing Strategy

- Unit tests for database layer (CRUD operations)
- Unit tests for all API endpoints
- Integration tests for auth + endpoint flow
- Test with actual SQLite database
- Target 80%+ coverage for backend

---

## Part 7: Connect Frontend to Backend API

**Objective:** Replace frontend's local state with actual backend API calls. Frontend now persists all changes to the server.

### Prerequisites

- Part 6 complete
- Frontend authentication UI from Part 4 in place

### Substeps

- [ ] Update login flow
  - [ ] Modify login to call `POST /api/auth/login`
  - [ ] Store session/auth token if returned
  - [ ] Handle login errors from API
  - [ ] Add loading state during login
  
- [ ] Create API client
  - [ ] Create `frontend/src/lib/api.ts` with fetch wrapper
  - [ ] Handle authentication headers/cookies
  - [ ] Implement error handling
  - [ ] Add loading/error states
  
- [ ] Update KanbanBoard component
  - [ ] Replace initial state with API call to `GET /api/board`
  - [ ] Add loading state while fetching
  - [ ] Add error state display
  
- [ ] Update card operations
  - [ ] Update drag-and-drop to call `PUT /api/board` with new state
  - [ ] Update column rename to call `POST /api/board/columns/{columnId}`
  - [ ] Update add card to call `POST /api/board/cards`
  - [ ] Update delete card to call `DELETE /api/board/cards/{cardId}`
  - [ ] Add loading/error feedback for each operation
  
- [ ] Implement optimistic updates
  - [ ] Update UI immediately on user action
  - [ ] Revert on API error
  - [ ] Show undo option on error
  
- [ ] Add logging/debugging
  - [ ] Log API requests/responses (dev only)
  - [ ] Add error tracking
  
- [ ] Test API integration
  - [ ] Test login flow connects to API
  - [ ] Test board loads from API
  - [ ] Test card operations persist to API
  - [ ] Test error handling (network errors, API errors)
  - [ ] Test with server down - graceful error
  - [ ] Manual e2e testing

### Success Criteria

- [ ] Frontend loads board from API
- [ ] All card operations persist to API
- [ ] Login/logout works with backend
- [ ] Error states are handled gracefully
- [ ] Optimistic updates work correctly
- [ ] No data loss on API errors
- [ ] All existing frontend tests still pass
- [ ] Add new integration tests for API calls
- [ ] Network requests show correct API calls

### Testing Strategy

- Mock API calls in existing component tests
- Add integration tests for API-connected components
- E2E tests verify data persistence (Playwright)
- Test error scenarios (network failure, invalid response)
- Target 80%+ coverage

---

## Part 8: AI Connectivity - Test OpenRouter

**Objective:** Verify backend can successfully call OpenRouter API. Test with simple "2+2" prompt to confirm AI connectivity.

### Prerequisites

- Part 6 complete (backend API working)
- `OPENROUTER_API_KEY` in `.env` file

### Substeps

- [ ] Set up environment variables
  - [ ] Create `.env` file in project root
  - [ ] Verify `OPENROUTER_API_KEY` is set
  - [ ] Load environment in backend startup
  
- [ ] Create AI service module
  - [ ] Create `backend/ai_service.py`
  - [ ] Import `openai` library (using OpenRouter endpoint)
  - [ ] Implement function to call OpenRouter API
  - [ ] Configure model as `openai/gpt-oss-120b`
  - [ ] Set up proper error handling
  
- [ ] Create test endpoint
  - [ ] Create `POST /api/ai/test` endpoint
  - [ ] Accept simple text prompt
  - [ ] Call OpenRouter with prompt
  - [ ] Return response text
  
- [ ] Test connectivity
  - [ ] Call test endpoint with "2+2"
  - [ ] Verify response contains "4" or similar math result
  - [ ] Test with various prompts
  - [ ] Test error handling (invalid API key, rate limits, etc.)
  
- [ ] Add logging
  - [ ] Log API requests (model, tokens, etc.)
  - [ ] Log timing of requests
  - [ ] Log errors with details

### Success Criteria

- [ ] OpenRouter API calls succeed
- [ ] Test endpoint returns valid responses
- [ ] "2+2" test returns correct answer
- [ ] Error handling works (invalid key, timeouts, etc.)
- [ ] Response times are reasonable (< 30s typical)
- [ ] No sensitive data logged
- [ ] API key is not exposed in logs

### Testing Strategy

- Manual testing via curl or Postman
- Test with valid and invalid API keys
- Test with various prompt lengths
- Test timeout behavior
- Monitor API usage/costs

---

## Part 9: AI Integration - Structured Output & Kanban Updates

**Objective:** Extend AI service to receive board context and user questions. AI returns structured response with text reply and optional Kanban updates.

### Prerequisites

- Part 8 complete (AI connectivity working)

### Substeps

- [ ] Design AI response schema
  - [ ] Create schema for structured output
  - [ ] Include: response_text (string), kanban_updates (object, optional)
  - [ ] Kanban_updates structure: { columns: [...], cards: [...] }
  - [ ] Document in `docs/AI_RESPONSE_SCHEMA.md`
  
- [ ] Create chat history management
  - [ ] Design conversation history storage (in-memory for MVP)
  - [ ] Create function to maintain conversation context
  - [ ] Plan data structure for conversation (messages array)
  
- [ ] Implement AI chat endpoint
  - [ ] Create `POST /api/chat` endpoint
  - [ ] Accept: user_message, board_state (JSON), conversation_history
  - [ ] Send to AI with system prompt explaining Kanban structure
  - [ ] Include full board context in prompt
  - [ ] Request structured JSON output
  
- [ ] Parse AI response
  - [ ] Extract response_text from AI output
  - [ ] Extract kanban_updates if provided
  - [ ] Validate Kanban updates
  - [ ] Apply updates to board if valid
  
- [ ] Add prompt engineering
  - [ ] Create system prompt explaining board structure
  - [ ] Include examples of valid Kanban updates
  - [ ] Provide guidelines for when to suggest updates
  - [ ] Document prompt in code comments
  
- [ ] Test AI integration
  - [ ] Test with simple questions (chat only)
  - [ ] Test with Kanban modification requests
  - [ ] Test with conversation history
  - [ ] Test error handling (malformed response, etc.)
  - [ ] Test with various board states

### Success Criteria

- [ ] AI endpoint accepts board context and questions
- [ ] AI returns structured JSON response
- [ ] Response includes both text and optional updates
- [ ] Kanban updates are valid and applied correctly
- [ ] Conversation history is maintained
- [ ] AI can suggest and execute Kanban changes
- [ ] Error handling for malformed AI responses
- [ ] Response times reasonable (< 60s typical)
- [ ] All tests pass with 80%+ coverage

### Testing Strategy

- Unit tests for response parsing
- Unit tests for schema validation
- Integration tests for full chat flow
- Mock AI responses for consistent testing
- Test with various board states and questions
- Manual testing with real AI

---

## Part 10: Add AI Chat Sidebar UI

**Objective:** Add beautiful chat sidebar to frontend. Users can chat with AI, which can update the Kanban board in real-time.

### Prerequisites

- Part 9 complete (AI backend fully functional)
- Parts 4 & 7 complete (authentication and API integration)

### Substeps

- [ ] Design chat UI
  - [ ] Plan sidebar layout and responsiveness
  - [ ] Design message bubble styles (user vs AI)
  - [ ] Design input area with send button
  - [ ] Plan for loading states and errors
  - [ ] Ensure mobile-friendly layout
  
- [ ] Create Chat component
  - [ ] Create `frontend/src/components/ChatSidebar.tsx`
  - [ ] Create `frontend/src/components/ChatMessage.tsx`
  - [ ] Create `frontend/src/components/ChatInput.tsx`
  - [ ] Implement message display with scrolling
  - [ ] Add timestamp display for messages
  
- [ ] Implement chat state management
  - [ ] Create hook for chat state (messages, loading, error)
  - [ ] Manage conversation history in local state
  - [ ] Implement message sending logic
  - [ ] Handle API call to `/api/chat` endpoint
  
- [ ] Handle Kanban updates from AI
  - [ ] Listen for Kanban updates in AI response
  - [ ] Update parent board state when AI suggests changes
  - [ ] Show visual feedback when AI updates board
  - [ ] Optional: Show "AI updated your board" notification
  
- [ ] Add error handling
  - [ ] Handle API errors gracefully
  - [ ] Show error messages to user
  - [ ] Implement retry logic
  - [ ] Handle network timeouts
  
- [ ] Style with color scheme
  - [ ] Use Accent Yellow (#ecad0a) for highlights
  - [ ] Use Blue Primary (#209dd7) for links/input focus
  - [ ] Use Purple Secondary (#753991) for send button
  - [ ] Use Dark Navy (#032147) for text
  - [ ] Use Gray Text (#888888) for supporting text
  
- [ ] Add animations
  - [ ] Message slide-in animation
  - [ ] Typing indicator while awaiting response
  - [ ] Smooth transitions for UI state changes
  - [ ] Highlight board changes when AI updates
  
- [ ] Implement localStorage for chat history
  - [ ] Persist chat history between sessions
  - [ ] Allow clearing chat history
  - [ ] Handle storage limits gracefully
  
- [ ] Test chat functionality
  - [ ] Unit tests for ChatSidebar component
  - [ ] Unit tests for message handling
  - [ ] Integration tests for chat + board updates
  - [ ] E2E tests for full chat flow (Playwright)
  - [ ] Test error scenarios
  - [ ] Manual testing of UI/UX
  
- [ ] Update layout
  - [ ] Integrate sidebar into main layout
  - [ ] Make sidebar responsive (collapse on mobile)
  - [ ] Ensure Kanban board adjusts for sidebar
  - [ ] Test layout on various screen sizes

### Success Criteria

- [ ] Chat sidebar displays prominently
- [ ] Users can send messages and receive responses
- [ ] AI responses display with proper formatting
- [ ] AI can update Kanban board from chat
- [ ] Board updates reflect immediately in UI
- [ ] Chat history persists across sessions
- [ ] Loading states and errors handled gracefully
- [ ] UI is responsive and looks polished
- [ ] Color scheme is consistent and professional
- [ ] All tests pass with 80%+ coverage
- [ ] Animations are smooth and not distracting
- [ ] Mobile layout works well

### Testing Strategy

- Unit tests for all Chat components (80%+ coverage)
- Integration tests for chat + API + board updates
- E2E tests for user chat scenario (Playwright)
- Manual testing on desktop and mobile
- Accessibility testing (keyboard nav, screen readers)
- Performance testing (response times, memory usage)

---

## Cross-Part Dependencies & Notes

### Key Dependencies

- Part 1 → All other parts (approval gate)
- Part 2 → Part 3 (backend must exist before frontend integration)
- Part 3 → Parts 4-7 (frontend must build first)
- Part 4 → Part 7 (auth UI needed before API integration)
- Part 5 → Part 6 (schema approved before implementation)
- Part 6 → Parts 7, 8, 9 (API endpoints needed)
- Part 8 → Part 9 (AI connectivity test before structured output)
- Part 9 → Part 10 (AI backend complete before UI)

### Testing Philosophy

- **Minimum 80% unit test coverage** for all code
- **Robust integration testing** connecting major components
- **E2E tests** using Playwright for critical user flows
- **Manual testing** for UI/UX and edge cases
- Test as you build, not after

### Success Metrics (MVP Complete)

- [ ] All 10 parts complete
- [ ] 80%+ code coverage across backend and frontend
- [ ] Comprehensive E2E test suite
- [ ] User can sign in, manage Kanban, chat with AI
- [ ] AI can update board based on chat requests
- [ ] Zero data loss scenarios
- [ ] Graceful error handling throughout
- [ ] Performance acceptable (< 2s response times typical)

---

## Next Steps

1. Get user approval on this plan
2. Proceed with Part 1: Create `frontend/AGENTS.md`
3. Continue through parts sequentially
4. Each part requires user sign-off before moving to next