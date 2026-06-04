"""Database layer for Kanban app using SQLite."""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

# Database file location
DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "kanban.db"


@dataclass
class User:
    """User model."""
    id: int
    username: str
    password_hash: str
    created_at: str


@dataclass
class Board:
    """Board model."""
    id: int
    user_id: int
    title: str
    created_at: str
    updated_at: str


@dataclass
class Column:
    """Column model."""
    id: int
    board_id: int
    title: str
    position: int
    created_at: str
    updated_at: str


@dataclass
class Card:
    """Card model."""
    id: int
    column_id: int
    title: str
    details: Optional[str]
    position: int
    priority: str = "medium"  # low, medium, high
    due_date: Optional[str] = None
    assignee: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Activity:
    """Activity log entry."""
    id: int
    user_id: int
    board_id: int
    action: str  # created, updated, moved, deleted
    entity_type: str  # card, column, board
    entity_id: int
    details: Optional[str]
    created_at: str


class Database:
    """SQLite database manager for Kanban app."""

    @staticmethod
    def init() -> None:
        """Initialize database schema if it doesn't exist."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Boards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS boards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL DEFAULT 'My Board',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Columns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS columns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                board_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                position INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
                UNIQUE(board_id, position)
            )
        """)

        # Cards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                column_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                details TEXT,
                position INTEGER NOT NULL,
                priority TEXT DEFAULT 'medium',
                due_date DATE,
                assignee TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (column_id) REFERENCES columns(id) ON DELETE CASCADE,
                UNIQUE(column_id, position)
            )
        """)

        # Activity log table for tracking changes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                board_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id INTEGER NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_boards_user_id ON boards(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_columns_board_id ON columns(board_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cards_column_id ON cards(column_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_board ON activity_log(board_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_user ON activity_log(user_id)")

        conn.commit()
        conn.close()

    @staticmethod
    @contextmanager
    def get_connection():
        """Get database connection context manager."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Return rows as dicts
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def seed_data() -> None:
        """Create default demo data (for testing only)."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = ?", ("user",))
            user = cursor.fetchone()

            if not user:
                # Create user
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    ("user", "password")  # In MVP, password is not hashed
                )
                user_id = cursor.lastrowid
            else:
                user_id = user[0]

            # Check if board already exists
            cursor.execute("SELECT id FROM boards WHERE user_id = ?", (user_id,))
            board = cursor.fetchone()

            if not board:
                # Create board
                cursor.execute(
                    "INSERT INTO boards (user_id, title) VALUES (?, ?)",
                    (user_id, "My Board")
                )
                board_id = cursor.lastrowid

                # Create default columns
                default_columns = [
                    ("Backlog", 0),
                    ("Discovery", 1),
                    ("In Progress", 2),
                    ("Review", 3),
                    ("Done", 4),
                ]

                for title, position in default_columns:
                    cursor.execute(
                        "INSERT INTO columns (board_id, title, position) VALUES (?, ?, ?)",
                        (board_id, title, position)
                    )

                # Create sample cards
                sample_cards = [
                    (1, "Align roadmap themes", "Draft quarterly themes with impact statements and metrics."),
                    (1, "Gather customer signals", "Review support tags, sales notes, and churn feedback."),
                    (2, "Prototype analytics view", "Sketch initial dashboard layout and key drill-downs."),
                    (3, "Refine status language", "Standardize column labels and tone across the board."),
                    (3, "Design card layout", "Add hierarchy and spacing for scanning dense lists."),
                    (4, "QA micro-interactions", "Verify hover, focus, and loading states."),
                    (5, "Ship marketing page", "Final copy approved and asset pack delivered."),
                    (5, "Close onboarding sprint", "Document release notes and share internally."),
                ]

                for col_id, title, details in sample_cards:
                    cursor.execute(
                        "SELECT COUNT(*) as count FROM cards WHERE column_id = ?",
                        (col_id,)
                    )
                    position = cursor.fetchone()["count"]
                    cursor.execute(
                        "INSERT INTO cards (column_id, title, details, position) VALUES (?, ?, ?, ?)",
                        (col_id, title, details, position)
                    )


# Database operations
class DatabaseOps:
    """Database CRUD operations."""

    @staticmethod
    def create_user(username: str, password: str) -> User:
        """Create a user with one default board and fixed columns."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password)
                )
            except sqlite3.IntegrityError:
                raise ValueError("Username already exists")

            user_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO boards (user_id, title) VALUES (?, ?)",
                (user_id, "My Board")
            )
            board_id = cursor.lastrowid

            default_columns = [
                ("Backlog", 0),
                ("Discovery", 1),
                ("In Progress", 2),
                ("Review", 3),
                ("Done", 4),
            ]

            for title, position in default_columns:
                cursor.execute(
                    "INSERT INTO columns (board_id, title, position) VALUES (?, ?, ?)",
                    (board_id, title, position)
                )

            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return User(
                id=row["id"],
                username=row["username"],
                password_hash=row["password_hash"],
                created_at=row["created_at"]
            )

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    id=row["id"],
                    username=row["username"],
                    password_hash=row["password_hash"],
                    created_at=row["created_at"]
                )
        return None

    @staticmethod
    def get_board(user_id: int) -> Optional[Dict[str, Any]]:
        """Get board with all columns and cards for a user."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()

            # Get board
            cursor.execute(
                "SELECT * FROM boards WHERE user_id = ? LIMIT 1",
                (user_id,)
            )
            board_row = cursor.fetchone()
            if not board_row:
                return None

            board = {
                "id": board_row["id"],
                "user_id": board_row["user_id"],
                "title": board_row["title"],
                "created_at": board_row["created_at"],
                "updated_at": board_row["updated_at"],
                "columns": []
            }

            # Get columns with cards
            cursor.execute(
                "SELECT * FROM columns WHERE board_id = ? ORDER BY position",
                (board_row["id"],)
            )
            columns = cursor.fetchall()

            for col_row in columns:
                cursor.execute(
                    "SELECT * FROM cards WHERE column_id = ? ORDER BY position",
                    (col_row["id"],)
                )
                cards = cursor.fetchall()

                column = {
                    "id": col_row["id"],
                    "board_id": col_row["board_id"],
                    "title": col_row["title"],
                    "position": col_row["position"],
                    "created_at": col_row["created_at"],
                    "updated_at": col_row["updated_at"],
                    "cards": [
                        {
                            "id": card_row["id"],
                            "column_id": card_row["column_id"],
                            "title": card_row["title"],
                            "details": card_row["details"],
                            "position": card_row["position"],
                            "priority": card_row["priority"] or "medium",
                            "due_date": card_row["due_date"],
                            "assignee": card_row["assignee"],
                            "created_at": card_row["created_at"],
                            "updated_at": card_row["updated_at"],
                        }
                        for card_row in cards
                    ]
                }
                board["columns"].append(column)

        return board

    @staticmethod
    def add_card(column_id: int, title: str, details: Optional[str] = None,
                priority: str = "medium", due_date: Optional[str] = None,
                assignee: Optional[str] = None) -> Card:
        """Add new card to column."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()

            # Get next position
            cursor.execute(
                "SELECT MAX(position) as max_pos FROM cards WHERE column_id = ?",
                (column_id,)
            )
            row = cursor.fetchone()
            position = (row["max_pos"] or -1) + 1

            # Insert card with new fields
            cursor.execute(
                "INSERT INTO cards (column_id, title, details, position, priority, due_date, assignee) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (column_id, title, details, position, priority, due_date, assignee)
            )

            card_id = cursor.lastrowid
            cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
            card_row = cursor.fetchone()

            return Card(
                id=card_row["id"],
                column_id=card_row["column_id"],
                title=card_row["title"],
                details=card_row["details"],
                position=card_row["position"],
                priority=card_row["priority"] or "medium",
                due_date=card_row["due_date"],
                assignee=card_row["assignee"],
                created_at=card_row["created_at"],
                updated_at=card_row["updated_at"],
            )

    @staticmethod
    def update_card(card_id: int, column_id: int, position: int) -> Card:
        """Move card to new column/position using a safe reordering algorithm."""
        import sys
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Get current card
            cursor.execute("SELECT column_id, position FROM cards WHERE id = ?", (card_id,))
            current_card = cursor.fetchone()
            if not current_card:
                raise ValueError(f"Card {card_id} not found")
            
            old_column_id = current_card["column_id"]
            old_position = current_card["position"]
            
            print(f"DEBUG: Moving card {card_id} from ({old_column_id}, {old_position}) to ({column_id}, {position})", file=sys.stderr)

            if old_column_id == column_id:
                # Same column - need to handle reordering if target position is occupied
                print(f"DEBUG: Same column, reordering needed", file=sys.stderr)
                
                # Step 1: Mark card as moving (position -1) to remove from constraint
                print(f"DEBUG: Step 1 - Mark card as moving (position -1)", file=sys.stderr)
                cursor.execute(
                    "UPDATE cards SET position = -1 WHERE id = ?",
                    (card_id,)
                )
                conn.commit()
                
                # Step 2: Reorder remaining cards to remove gaps
                print(f"DEBUG: Step 2 - Reordering column {old_column_id} to remove gaps", file=sys.stderr)
                cursor.execute(
                    "SELECT id, position FROM cards WHERE column_id = ? AND position >= 0 ORDER BY position",
                    (old_column_id,)
                )
                remaining_cards = cursor.fetchall()
                for idx, card in enumerate(remaining_cards):
                    if card["position"] != idx:
                        print(f"DEBUG:   - Moving card {card['id']} from position {card['position']} to {idx}", file=sys.stderr)
                        cursor.execute(
                            "UPDATE cards SET position = ? WHERE id = ?",
                            (idx, card["id"])
                        )
                conn.commit()
                
                # Step 3: Check if target position is occupied
                print(f"DEBUG: Step 3 - Checking if position {position} in column {column_id} is occupied", file=sys.stderr)
                cursor.execute(
                    "SELECT COUNT(*) as cnt FROM cards WHERE column_id = ? AND position >= ?",
                    (column_id, position)
                )
                cards_at_or_after = cursor.fetchone()["cnt"]
                
                # If position is occupied, shift cards to the right
                if cards_at_or_after > 0:
                    print(f"DEBUG:   - Position occupied, shifting {cards_at_or_after} cards to the right", file=sys.stderr)
                    cursor.execute(
                        "SELECT id, position FROM cards WHERE column_id = ? AND position >= ? ORDER BY position DESC",
                        (column_id, position)
                    )
                    cards_to_shift = cursor.fetchall()
                    for card in cards_to_shift:
                        new_pos = card["position"] + 1
                        print(f"DEBUG:   - Shifting card {card['id']} from position {card['position']} to {new_pos}", file=sys.stderr)
                        cursor.execute(
                            "UPDATE cards SET position = ? WHERE id = ?",
                            (new_pos, card["id"])
                        )
                conn.commit()
                
                # Step 4: Place our card at target position
                print(f"DEBUG: Step 4 - Moving card {card_id} to position {position}", file=sys.stderr)
                cursor.execute(
                    "UPDATE cards SET position = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (position, card_id)
                )
                conn.commit()
                print(f"DEBUG: Same-column move complete", file=sys.stderr)
            else:
                # Different column - more complex
                print(f"DEBUG: Different column", file=sys.stderr)
                
                # Step 1: Remove card from old column (temporarily set to negative position to mark as moving)
                print(f"DEBUG: Step 1 - Mark card as moving (position -1)", file=sys.stderr)
                cursor.execute(
                    "UPDATE cards SET position = -1 WHERE id = ?",
                    (card_id,)
                )
                conn.commit()
                
                # Step 2: Reorder remaining cards in old column to remove gaps
                print(f"DEBUG: Step 2 - Reordering old column {old_column_id}", file=sys.stderr)
                cursor.execute(
                    "SELECT id, position FROM cards WHERE column_id = ? AND position >= 0 ORDER BY position",
                    (old_column_id,)
                )
                old_column_cards = cursor.fetchall()
                for idx, card in enumerate(old_column_cards):
                    if card["position"] != idx:
                        print(f"DEBUG:   - Moving card {card['id']} from position {card['position']} to {idx}", file=sys.stderr)
                        cursor.execute(
                            "UPDATE cards SET position = ? WHERE id = ?",
                            (idx, card["id"])
                        )
                conn.commit()
                
                # Step 3: Check if target position in new column is occupied
                print(f"DEBUG: Step 3 - Checking if position {position} in column {column_id} is occupied", file=sys.stderr)
                cursor.execute(
                    "SELECT COUNT(*) as cnt FROM cards WHERE column_id = ? AND position >= ?",
                    (column_id, position)
                )
                cards_at_or_after = cursor.fetchone()["cnt"]
                
                # If position is occupied, shift existing cards to the right
                if cards_at_or_after > 0:
                    print(f"DEBUG:   - Position occupied, shifting {cards_at_or_after} cards to the right", file=sys.stderr)
                    cursor.execute(
                        "SELECT id, position FROM cards WHERE column_id = ? AND position >= ? ORDER BY position DESC",
                        (column_id, position)
                    )
                    cards_to_shift = cursor.fetchall()
                    for card in cards_to_shift:
                        new_pos = card["position"] + 1
                        print(f"DEBUG:   - Shifting card {card['id']} from position {card['position']} to {new_pos}", file=sys.stderr)
                        cursor.execute(
                            "UPDATE cards SET position = ? WHERE id = ?",
                            (new_pos, card["id"])
                        )
                conn.commit()
                
                # Step 4: Move our card to target column and position
                print(f"DEBUG: Step 4 - Moving card {card_id} to column {column_id}, position {position}", file=sys.stderr)
                cursor.execute(
                    "UPDATE cards SET column_id = ?, position = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (column_id, position, card_id)
                )
                conn.commit()
                print(f"DEBUG: Move complete", file=sys.stderr)

            # Fetch updated card
            cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
            card_row = cursor.fetchone()

            return Card(
                id=card_row["id"],
                column_id=card_row["column_id"],
                title=card_row["title"],
                details=card_row["details"],
                position=card_row["position"],
                priority=card_row["priority"] or "medium",
                due_date=card_row["due_date"],
                assignee=card_row["assignee"],
                created_at=card_row["created_at"],
                updated_at=card_row["updated_at"],
            )
        except Exception as e:
            print(f"DEBUG: Exception: {e}", file=sys.stderr)
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def delete_card(card_id: int) -> bool:
        """Delete card."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
            return cursor.rowcount > 0

    @staticmethod
    def rename_column(column_id: int, title: str) -> Column:
        """Rename column."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE columns SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (title, column_id)
            )

            cursor.execute("SELECT * FROM columns WHERE id = ?", (column_id,))
            col_row = cursor.fetchone()

            return Column(
                id=col_row["id"],
                board_id=col_row["board_id"],
                title=col_row["title"],
                position=col_row["position"],
                created_at=col_row["created_at"],
                updated_at=col_row["updated_at"],
            )

    @staticmethod
    def update_card_details(card_id: int, title: str = None, details: str = None, 
                           priority: str = None, due_date: str = None, 
                           assignee: str = None) -> Card:
        """Update card details (title, details, priority, due_date, assignee)."""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build update query dynamically
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = ?")
                params.append(title)
            if details is not None:
                updates.append("details = ?")
                params.append(details)
            if priority is not None:
                updates.append("priority = ?")
                params.append(priority)
            if due_date is not None:
                updates.append("due_date = ?")
                params.append(due_date)
            if assignee is not None:
                updates.append("assignee = ?")
                params.append(assignee)
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                params.append(card_id)
                
                query = f"UPDATE cards SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
            
            # Fetch updated card
            cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
            card_row = cursor.fetchone()
            
            if not card_row:
                raise ValueError(f"Card {card_id} not found")
            
            return Card(
                id=card_row["id"],
                column_id=card_row["column_id"],
                title=card_row["title"],
                details=card_row["details"],
                position=card_row["position"],
                priority=card_row["priority"] or "medium",
                due_date=card_row["due_date"],
                assignee=card_row["assignee"],
                created_at=card_row["created_at"],
                updated_at=card_row["updated_at"],
            )
