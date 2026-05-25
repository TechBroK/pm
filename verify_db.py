import sqlite3
import sys

db_path = 'backend/kanban.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f"✅ Database Tables: {tables}")

# Get row counts for each table
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"   - {table}: {count} rows")

# Get users
cursor.execute("SELECT id, username FROM users")
users = cursor.fetchall()
print(f"\n✅ Users in database:")
for user_id, username in users:
    print(f"   - ID {user_id}: {username}")

# Get boards
cursor.execute("SELECT id, user_id, title FROM boards")
boards = cursor.fetchall()
print(f"\n✅ Boards in database:")
for board_id, user_id, title in boards:
    print(f"   - ID {board_id}: '{title}' (user_id: {user_id})")

# Get columns
cursor.execute("SELECT id, board_id, position, title FROM columns ORDER BY position")
columns = cursor.fetchall()
print(f"\n✅ Columns in database:")
for col_id, board_id, pos, title in columns:
    print(f"   - ID {col_id}: Position {pos} - '{title}'")

# Get cards with their columns
cursor.execute("""
    SELECT c.id, c.column_id, c.title, col.title as column_name, c.position
    FROM cards c
    JOIN columns col ON c.column_id = col.id
    ORDER BY c.column_id, c.position
""")
cards = cursor.fetchall()
print(f"\n✅ Cards in database ({len(cards)} total):")
for card_id, col_id, title, col_name, pos in cards:
    print(f"   - Card {card_id} (Pos {pos}): '{title}' → {col_name}")

conn.close()
print("\n✅ Database connection and queries successful!")
