#!/usr/bin/env python3
"""
Debug the move card within same column issue
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Login
print("Logging in...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "user", "password": "password"}
)
session_id = response.json().get("session_id")
print(f"Session: {session_id}")

# Add a card
print("\nAdding card to column 1...")
response = requests.post(
    f"{BASE_URL}/api/board/cards",
    params={"session_id": session_id, "column_id": 1},
    json={"title": "Test Card", "details": "Test"}
)
print(f"Status: {response.status_code}")
card = response.json()
card_id = card.get("id")
current_position = card.get("position")
print(f"Card ID: {card_id}, Current Position: {current_position}")

# Try to move within same column
print(f"\nMoving card {card_id} within column 1 from position {current_position} to position {current_position + 1}...")
response = requests.put(
    f"{BASE_URL}/api/board/cards/{card_id}",
    params={"session_id": session_id},
    json={"column_id": 1, "position": current_position + 1}
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Check board state
print("\nFinal board state...")
response = requests.get(
    f"{BASE_URL}/api/board",
    params={"session_id": session_id}
)
board = response.json()
for col in board.get("columns", []):
    if col["id"] == 1:
        print(f"Column {col['title']}: {len(col['cards'])} cards")
        for i, c in enumerate(col['cards']):
            print(f"  - Position {i}: Card {c['id']} '{c['title']}'")
