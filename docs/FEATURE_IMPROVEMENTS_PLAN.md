# Feature Improvements Implementation Plan

## Overview
Five major features to enhance the Kanban MVP. Implementation order prioritizes high-impact, manageable changes.

---

## Feature 1: Enhanced Card Details ✓ Planning
**Impact:** High | **Effort:** Medium | **Time:** 2-3 hours

### Schema Changes
```sql
-- Add columns to cards table
ALTER TABLE cards ADD COLUMN priority TEXT DEFAULT 'medium'; -- low, medium, high
ALTER TABLE cards ADD COLUMN due_date DATE;
ALTER TABLE cards ADD COLUMN assignee TEXT;
```

### Backend Changes
- Update `Card` dataclass with new fields
- Update `add_card()` to accept new fields
- Update `update_card()` to handle new fields
- Update `get_board()` to return new fields
- Add `update_card_details()` endpoint

### Frontend Changes
- Update `Card` type in `lib/kanban.ts`
- Add `KanbanCardEditor.tsx` component for editing
- Update `KanbanCard.tsx` to display priority, due date, assignee
- Add priority badge with color (low=blue, medium=yellow, high=red)
- Add due date display with warning if overdue

### API Endpoints
```
POST /api/board/cards/{id} - Update card details
  payload: {title, details, priority, due_date, assignee}
```

---

## Feature 2: Activity Tracking & Undo/Redo
**Impact:** Medium | **Effort:** High | **Time:** 3-4 hours

### Schema Changes
```sql
-- Create activity_log table
CREATE TABLE activity_log (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  board_id INTEGER NOT NULL,
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id INTEGER NOT NULL,
  details TEXT,
  created_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (board_id) REFERENCES boards(id)
);

-- Create undo_log table
CREATE TABLE undo_log (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  board_id INTEGER NOT NULL,
  action_type TEXT,
  entity_data TEXT,
  created_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (board_id) REFERENCES boards(id)
);
```

### Backend Changes
- Add `log_activity()` function to capture all changes
- Add `get_activity_log()` endpoint to retrieve history
- Implement undo/redo stack management
- Add `/api/board/history` endpoint

### Frontend Changes
- Add activity sidebar showing recent changes
- Add Undo (Ctrl+Z) / Redo (Ctrl+Y) buttons
- Display change timestamp and what changed
- Visual timeline of board activity

---

## Feature 3: Smarter AI Features
**Impact:** High | **Effort:** Medium | **Time:** 2-3 hours

### New AI Capabilities
1. **Board Summary** - "Summarize board status"
2. **Smart Suggestions** - "What should I prioritize?"
3. **Bulk Operations** - "Move all pending items to In Progress"
4. **Task Generation** - "Create subtasks for..." 
5. **Status Report** - "Generate status report"

### Backend Changes
- Add `AIService` methods:
  - `summarize_board(board)`
  - `suggest_priorities(board, user_id)`
  - `get_board_insights(board)`
  - `generate_status_report(board)`

### Frontend Changes
- Add AI prompt templates in sidebar
- Add response formatting (better markdown display)
- Show action buttons on AI suggestions

---

## Feature 4: Visual Polish & Animations
**Impact:** Medium | **Effort:** Low | **Time:** 1-2 hours

### Styling Improvements
- Use brand colors consistently:
  - Accent Yellow: `#ecad0a`
  - Blue Primary: `#209dd7`
  - Purple Secondary: `#753991`
  - Dark Navy: `#032147`
  - Gray Text: `#888888`

### Animations
- Smooth card drag animations (already using dnd-kit)
- Column fade-in on page load
- Card entry animations (slide up)
- Priority badge color transitions
- Due date warning animations

### Responsive Design
- Mobile-friendly card layout
- Touch-friendly drag & drop
- Mobile sidebar collapse
- Responsive typography

### UX Enhancements
- Loading skeletons for cards
- Confirmation dialogs for delete
- Tooltip on hover (priority, assignee, due date)
- Empty state messages
- Success/error toast notifications

---

## Feature 5: Export & Backups
**Impact:** Low-Medium | **Effort:** Low | **Time:** 1-2 hours

### Export Formats
1. **CSV Export**
   - Column: title, details, priority, due_date, assignee
   - Separate CSV per column or single CSV with column name

2. **JSON Export**
   - Full board structure with all metadata
   - Includes columns, cards, metadata

3. **PDF Report**
   - Printable board summary
   - Color-coded by priority

### Backup Features
- **Auto-backup**: Daily SQLite backup
- **Manual backup**: Download `.db` file
- **Restore from backup**: Upload SQLite file

### API Endpoints
```
GET /api/board/export?format=csv|json|pdf
GET /api/board/backup - Download database
POST /api/board/restore - Upload and restore backup
```

---

## Implementation Order

1. **Phase 1** (2-3 hours): Enhanced Card Details
   - Database migration
   - Backend endpoints
   - Frontend card editor

2. **Phase 2** (2 hours): Visual Polish
   - Brand colors
   - Animations
   - Responsive layout

3. **Phase 3** (2-3 hours): Smarter AI
   - New AI service methods
   - Frontend prompts
   - Response formatting

4. **Phase 4** (3-4 hours): Activity Tracking
   - Database schema
   - Activity logging
   - Undo/Redo UI

5. **Phase 5** (1-2 hours): Export & Backups
   - CSV/JSON export
   - Backup endpoints
   - Restore functionality

---

## Testing Strategy

- [ ] Unit tests for each new service method
- [ ] Integration tests for API endpoints
- [ ] Component tests for new UI elements
- [ ] E2E tests for complete workflows
- [ ] Manual testing on production URL

---

## Rollback Plan

Each phase is independent:
- If Phase 1 breaks, can rollback to previous commit
- Database migrations are additive (won't break existing data)
- Feature flags for risky changes (AI, undo/redo)

---

## Success Criteria

✅ All new fields saved and retrieved correctly
✅ AI features provide useful suggestions
✅ Undo/Redo works smoothly
✅ App looks polished with brand colors
✅ Export/backup works for data safety
✅ No regression in existing features
✅ Performance not degraded
