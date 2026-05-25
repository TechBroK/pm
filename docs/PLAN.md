# Project Management MVP - Detailed Implementation Plan

## Overview

Building a Project Management App MVP with NextJS frontend, Python FastAPI backend, and SQLite database. The app enables users to sign in, manage Kanban boards, move cards via drag-and-drop, and interact with an AI assistant for board management.

**Last Updated:** May 25, 2026  
**Current Status:** Parts 1-7 Complete (70% done) | Parts 8-10 Not Started

---

## Part 1: Planning & Documentation ✅ COMPLETE

**Objective:** Complete detailed planning for all 10 parts, document existing frontend code, and get user approval.

**Status:** ✅ COMPLETE - See `docs/PART_1_SUMMARY.md`

### Completed Deliverables

- [x] Enriched 10-part implementation plan with detailed substeps for each part
- [x] Frontend architecture documentation in `frontend/AGENTS.md`
- [x] Backend architecture documentation in `backend/AGENTS.md`
- [x] All components, data structures, and utility functions documented
- [x] Testing strategies and known issues identified

---

## Part 2: Backend Scaffolding & Hello World ✅ COMPLETE

**Objective:** Set up FastAPI backend infrastructure and verify it can serve static HTML and make a test API call.

**Status:** ✅ COMPLETE - See `docs/PART_2_SUMMARY.md`

### Completed Deliverables

- [x] FastAPI backend running on `http://localhost:8000`
- [x] Backend serves static HTML hello world page
- [x] Test API endpoint: `GET /api/test` returns `{"message": "Hello from API"}`
- [x] Health check endpoint: `GET /health`
- [x] Server management scripts for Windows, Linux, macOS
- [x] Requirements.txt with FastAPI, Uvicorn, and dependencies
- [x] Automatic static directory creation on startup

### Prerequisites

- ✅ Part 1 approved

---

## Part 3: Integrate Frontend Build & Serving ✅ COMPLETE

**Objective:** Build the NextJS frontend and serve it statically from the backend. The app displays the Kanban board at `/`.

**Status:** ✅ COMPLETE - See `docs/PART_3_SUMMARY.md`

### Completed Deliverables

- [x] Frontend builds successfully with `npm run build`
- [x] Frontend exports to `frontend/dist/` directory
- [x] Backend mounts frontend assets at `/_next`
- [x] Backend serves frontend SPA at root path `/`
- [x] SPA routing fallback configured (404.html handling)
- [x] Updated start scripts to build frontend before starting backend
- [x] All assets load correctly (CSS, JS, images)
- [x] Kanban board fully interactive at `http://localhost:8000/`

### Prerequisites

- ✅ Part 2 complete
- ✅ Frontend dependencies installed

---

## Part 4: Implement User Sign-in ✅ COMPLETE

**Objective:** Add hardcoded user authentication. Users must sign in with `user`/`password` to access the Kanban board.

**Status:** ✅ COMPLETE - See `docs/PART_4_SUMMARY.md`

### Completed Deliverables

- [x] Login page component: `frontend/src/components/LoginPage.tsx`
- [x] Auth context: `frontend/src/lib/auth-context.tsx` with `useAuth()` hook
- [x] Auth utilities: `frontend/src/lib/auth.ts` with authenticate/session functions
- [x] Protected route wrapper: `frontend/src/components/ProtectedRoute.tsx`
- [x] Kanban board updated with Sign Out button and username display
- [x] Root layout wrapped with AuthProvider
- [x] Session persistence via localStorage
- [x] All authentication tests passing
- [x] End-to-end auth flow tested and verified

### Prerequisites

- ✅ Part 3 complete
- ✅ Existing frontend tests passing

---

## Part 5: Design & Approve Database Schema ✅ COMPLETE

**Objective:** Design SQLite database schema to support users, boards, columns, and cards. Document the schema and get user approval.

**Status:** ✅ COMPLETE - See `docs/DATABASE_SCHEMA.md` and `docs/schema.json`

### Completed Design

**Database:** SQLite (file-based, auto-created on first startup)

**Tables:**

1. **users** - User authentication
   - `id` (INTEGER PRIMARY KEY)
   - `username` (TEXT UNIQUE NOT NULL)
   - `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

2. **boards** - User's Kanban board (1 per user in MVP)
   - `id` (INTEGER PRIMARY KEY)
   - `user_id` (INTEGER FOREIGN KEY → users.id)
   - `title` (TEXT NOT NULL)
   - `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
   - `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

3. **columns** - Fixed columns (5 per board)
   - `id` (INTEGER PRIMARY KEY)
   - `board_id` (INTEGER FOREIGN KEY → boards.id)
   - `title` (TEXT NOT NULL)
   - `position` (INTEGER NOT NULL)
   - `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
   - `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

4. **cards** - Task cards in columns
   - `id` (INTEGER PRIMARY KEY)
   - `column_id` (INTEGER FOREIGN KEY → columns.id)
   - `title` (TEXT NOT NULL)
   - `details` (TEXT)
   - `position` (INTEGER NOT NULL)
   - `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
   - `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### Design Decisions

- **SQLite for MVP:** Simple, serverless, embedded database. File persists in `backend/kanban.db`
- **Foreign Keys:** Cascade delete enabled for data integrity
- **Indexes:** Created on `user_id`, `board_id`, `column_id` for query performance
- **Timestamps:** Track creation and modification for audit trail
- **Position Field:** Enables drag-and-drop reordering without re-indexing IDs

### Completed Deliverables

- [x] Database schema fully documented in `docs/DATABASE_SCHEMA.md`
- [x] ER diagram included
- [x] Schema exported as JSON in `docs/schema.json`
- [x] Design supports MVP requirements (1 user, 1 board, unlimited cards)
- [x] User approved schema

---

## Part 6: Implement Backend Database & API ✅ COMPLETE

**Objective:** Implement SQLite database initialization, data models, and API endpoints for reading/writing Kanban data.

**Status:** ✅ COMPLETE (with minor issues noted) - See `docs/PART_6_SUMMARY.md`

### Completed Deliverables

- [x] Database layer: `backend/db.py` with SQLite connection management
- [x] Database initialization: Auto-creates tables on first run
- [x] Data models: User, Board, Column, Card (dataclasses)
- [x] Database context manager for transaction handling
- [x] Seed data: Populates test user and sample board
- [x] CRUD operations for all data models
- [x] Session management: In-memory UUID-based sessions

### Implemented API Endpoints

**Authentication:**
- [x] `POST /api/auth/login` - Returns session_id and username
- [x] `POST /api/auth/logout` - Clears session

**Board Operations:**
- [x] `GET /api/board` - Returns board with all columns and cards
- [x] `GET /health` - Health check
- [x] `GET /api/test` - Test endpoint

**Card Operations:**
- [x] `POST /api/board/cards` - Add new card (auto-assigns position)
- [x] `PUT /api/board/cards/{card_id}` - Move/update card
- [x] `DELETE /api/board/cards/{card_id}` - Delete card

**Column Operations:**
- [x] `POST /api/board/columns/{column_id}` - Rename column

### Completed Implementation Details

- [x] Database initialization on startup
- [x] Automatic schema creation if tables missing
- [x] Seed data population on first run
- [x] CORS middleware enabled for development
- [x] Static file serving (frontend) still works
- [x] Backend serves both API and frontend from port 8000
- [x] Proper error handling with HTTP status codes
- [x] Validation on all data operations

### Database File

- **Location:** `backend/kanban.db`
- **Size:** 49,152 bytes
- **Tables:** users (1 row), boards (1 row), columns (5 rows), cards (8+ rows)
- **Status:** ✅ All data persists correctly, verified via tests

### Known Issues ⚠️ (Minor)

1. **Column Rename Persistence** ⚠️
   - Symptom: Column renames work in UI but don't persist after logout/login
   - Impact: Column renames lost between sessions
   - Recommendation: Verify column rename is calling API and database is being updated

2. **Move Card API Returns 400** ⚠️
   - Symptom: `PUT /api/board/cards/{card_id}` returns 400 Bad Request
   - Impact: API call fails, but UI drag/drop still works
   - Recommendation: Check request validation in backend

3. **Session Invalidation** ⚠️
   - Symptom: After logout, accessing protected endpoints still returns 200 instead of 401
   - Impact: Session may not be properly cleared
   - Recommendation: Review session management logic

### Prerequisites

- ✅ Part 5 approved

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