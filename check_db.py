#!/usr/bin/env python
"""Debug database state."""

import sqlite3
from pathlib import Path

db_path = Path("backend/kanban.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Show all cards in columns 1-3
for col_id in [1, 2, 3]:
    print(f"\nColumn {col_id}:")
    cursor.execute("SELECT id, position, title FROM cards WHERE column_id = ? ORDER BY position", (col_id,))
    for row in cursor.fetchall():
        print(f"  Card {row['id']}: position {row['position']} - {row['title']}")

conn.close()
