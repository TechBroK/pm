#!/usr/bin/env python
"""Debug script to see the exact move card error."""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Login
login_resp = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "user", "password": "password"}
)
session_id = login_resp.json().get("session_id")
print(f"Session: {session_id}\n")

# Get board
board_resp = requests.get(f"{BASE_URL}/api/board?session_id={session_id}")
board = board_resp.json()
print(f"Board loaded: {len(board['columns'])} columns, {sum(len(c['cards']) for c in board['columns'])} cards\n")

# Add a card
add_resp = requests.post(
    f"{BASE_URL}/api/board/cards?column_id=1&session_id={session_id}",
    json={"title": "Test", "details": "Test move"}
)
card = add_resp.json()
card_id = card.get("id")
print(f"Added card {card_id} to column 1\n")

# Try to move it
print("Attempting to move card...")
move_resp = requests.put(
    f"{BASE_URL}/api/board/cards/{card_id}?session_id={session_id}",
    json={"column_id": 2, "position": 0}
)

print(f"Status: {move_resp.status_code}")
print(f"Response: {json.dumps(move_resp.json(), indent=2)}")
