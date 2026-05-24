# Database Schema Design

## Overview

This document defines the SQLite database schema for the Project Management MVP. The schema is designed to support the current MVP features while allowing flexibility for future enhancements.

### Design Principles

- **Simplicity**: Minimal tables and relationships, no over-engineering
- **Normalization**: 3NF to avoid redundancy
- **Future-proof**: Support for multiple users and boards (even though MVP uses only one)
- **Audit trail**: Track creation and update timestamps for debugging

---

## Table Definitions

### 1. Users Table

Stores user account information. MVP hardcodes 'user' login, but database supports multiple users.

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

- `id`: Primary key, auto-increment
- `username`: Unique username (currently hardcoded as 'user')
- `password_hash`: Hashed password (currently hardcoded check, future: use proper hashing)
- `created_at`: Account creation timestamp

**Indexes:**

- `username` (UNIQUE) for fast login lookups

---

### 2. Boards Table

Represents a Kanban board. MVP creates one board per user; future could support multiple boards.

```sql
CREATE TABLE boards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL DEFAULT 'My Board',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Columns:**

- `id`: Primary key, auto-increment
- `user_id`: Foreign key to users table
- `title`: Board name (default: 'My Board')
- `created_at`: Board creation timestamp
- `updated_at`: Last modification timestamp

**Indexes:**

- `user_id` for fast board lookups by user

**Constraints:**

- Foreign key with CASCADE delete (deleting user deletes their boards)

---

### 3. Columns Table

Represents Kanban columns. Each board has fixed 5 columns (Backlog, Discovery, In Progress, Review, Done) that can be renamed.

```sql
CREATE TABLE columns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  board_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  position INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
  UNIQUE(board_id, position)
);
```

**Columns:**

- `id`: Primary key, auto-increment
- `board_id`: Foreign key to boards table
- `title`: Column name (e.g., 'Backlog', 'In Progress')
- `position`: Column order (0-4 for 5 columns)
- `created_at`: Column creation timestamp
- `updated_at`: Last modification timestamp

**Indexes:**

- `board_id` for fast column lookups by board
- Unique constraint on `(board_id, position)` to prevent duplicate positions

**Constraints:**

- Foreign key with CASCADE delete (deleting board deletes columns)

---

### 4. Cards Table

Represents tasks/cards on the Kanban board. Cards belong to columns and can be moved between them.

```sql
CREATE TABLE cards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  column_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  details TEXT,
  position INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (column_id) REFERENCES columns(id) ON DELETE CASCADE,
  UNIQUE(column_id, position)
);
```

**Columns:**

- `id`: Primary key, auto-increment
- `column_id`: Foreign key to columns table
- `title`: Card title (required)
- `details`: Card description/notes (optional)
- `position`: Card order within column
- `created_at`: Card creation timestamp
- `updated_at`: Last modification timestamp

**Indexes:**

- `column_id` for fast card lookups by column
- Unique constraint on `(column_id, position)` for ordering

**Constraints:**

- Foreign key with CASCADE delete (deleting column deletes cards)

---

## Data Flow Example

**User logs in:**

```
1. Query users table with username 'user'
2. Return user record with id=1
3. Query boards table with user_id=1
4. Return board record with id=1
5. Query columns table with board_id=1
6. Return 5 column records (positions 0-4)
7. Query cards table with column_id IN (col_ids)
8. Return all cards grouped by column
```

**User adds card to 'In Progress' column:**

```
1. Find column with board_id=1 and title='In Progress'
2. Get max position in that column
3. Insert new card with column_id=col_id, position=max+1
4. Return card to frontend
```

**User moves card from 'Discovery' to 'In Progress':**

```
1. Update card: column_id=new_col_id, position=new_position
2. Reorder other cards in both columns if needed
3. Return updated card
```

---

## Relationships Diagram

```
users (1)
  |
  +--< (M) boards
       |
       +--< (M) columns
            |
            +--< (M) cards
```

---

## Initial Data

When a new user logs in for the first time, the system should:

1. Create a new `users` record (or use hardcoded 'user' for MVP)
2. Create a new `boards` record with title 'My Board'
3. Create 5 `columns` records with:
   - Position 0: "Backlog"
   - Position 1: "Discovery"
   - Position 2: "In Progress"
   - Position 3: "Review"
   - Position 4: "Done"
4. Sample cards can be pre-populated or user starts with empty board

---

## Indexes Summary

| Table   | Column(s)             | Type   | Purpose                     |
| ------- | --------------------- | ------ | --------------------------- |
| users   | username              | UNIQUE | Fast login lookup           |
| boards  | user_id               | INDEX  | Fast board lookup by user   |
| columns | board_id              | INDEX  | Fast column lookup by board |
| columns | (board_id, position)  | UNIQUE | Prevent duplicate positions |
| cards   | column_id             | INDEX  | Fast card lookup by column  |
| cards   | (column_id, position) | UNIQUE | Prevent duplicate positions |

---

## Considerations for Future Phases

### Phase 6: Database Implementation

- Create SQLite database file: `backend/kanban.db`
- Initialize schema on first startup if DB doesn't exist
- Add seed data (5 columns per user)

### Phase 7: API Integration

- CRUD endpoints for cards, columns
- Bulk operations (e.g., move multiple cards)
- Transaction handling for consistency

### Phase 8-10: AI Integration

- Possible future fields: card priority, tags, due dates
- AI could suggest card placement based on content

### Future Enhancements

- Add `archived` boolean to cards (soft delete)
- Add `color` field to cards
- Add `due_date` field to cards
- Add `assigned_to` field to cards
- Add `priority` field to cards
- Add `labels` table for tagging

---

## Notes

- All timestamps use UTC (CURRENT_TIMESTAMP in SQLite)
- No soft deletes in MVP (cascade deletes are safe)
- IDs are auto-incremented integers (sufficient for MVP scale)
- No encryption or special security beyond hardcoded auth
- Database file will be single `kanban.db` in backend directory
