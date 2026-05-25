#!/usr/bin/env python3
"""Debug move card with verbose output."""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Login
login_response = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "user", "password": "password"})
session_id = login_response.json()["session_id"]
print(f"Session: {session_id}\n")

# Get board
board_response = requests.get(f"{BASE_URL}/api/board", params={"session_id": session_id})
board = board_response.json()
print(f"Board loaded: {len(board['columns'])} columns, {sum(len(col['cards']) for col in board['columns'])} cards\n")

# Add a test card to column 1
add_response = requests.post(
    f"{BASE_URL}/api/board/cards",
    params={"column_id": 1, "session_id": session_id},
    json={"title": "Test", "details": ""}
)
card_id = add_response.json()["id"]
print(f"Added card {card_id} to column 1\n")

# Now try to move it to column 2, position 0
print(f"Attempting to move card {card_id} from column 1 to column 2, position 0...")
move_response = requests.put(
    f"{BASE_URL}/api/board/cards/{card_id}",
    params={"session_id": session_id},
    json={"column_id": 2, "position": 0}
)

print(f"Status: {move_response.status_code}")
print(f"Response: {json.dumps(move_response.json(), indent=2)}")
