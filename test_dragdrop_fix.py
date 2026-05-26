#!/usr/bin/env python3
"""
Test drag-and-drop functionality - specifically same-column moves
This verifies the fix for cards refusing to move within sections
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("DRAG-AND-DROP FIX TEST")
print("=" * 80)
print()

# Login
print("Step 1: Authenticating...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "user", "password": "password"}
)
session_id = response.json().get("session_id")
print(f"✅ Logged in, session: {session_id[:20]}...")
print()

# Get board
print("Step 2: Loading board...")
response = requests.get(
    f"{BASE_URL}/api/board",
    params={"session_id": session_id}
)
board = response.json()
columns = {col["id"]: col for col in board["columns"]}
print(f"✅ Board loaded: {len(columns)} columns")
for col in board["columns"]:
    print(f"   - Column {col['id']}: {col['title']} ({len(col['cards'])} cards)")
print()

# TEST 1: Move card to end of same column (no occupied position)
print("TEST 1: Move card within column (to end)")
print("-" * 80)
try:
    col_id = board["columns"][0]["id"]
    cards = board["columns"][0]["cards"]
    if len(cards) > 1:
        card_to_move = cards[0]
        new_position = len(cards) - 1
        
        print(f"Moving card '{card_to_move['title']}' (ID {card_to_move['id']})")
        print(f"From position 0 to position {new_position} in column {col_id}")
        
        response = requests.put(
            f"{BASE_URL}/api/board/cards/{card_to_move['id']}",
            params={"session_id": session_id},
            json={"column_id": col_id, "position": new_position}
        )
        
        if response.status_code == 200:
            print(f"✅ SUCCESS - Card moved to position {response.json()['position']}")
        else:
            print(f"❌ FAILED - Status {response.status_code}")
            print(f"   Response: {response.text}")
    else:
        print(f"⊘ Skipped - Column has < 2 cards")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
print()

# TEST 2: Move card to middle of same column (occupied position)
print("TEST 2: Move card within column (to middle - occupied position)")
print("-" * 80)
try:
    col_id = board["columns"][0]["id"]
    cards = board["columns"][0]["cards"]
    if len(cards) > 2:
        card_to_move = cards[-1]  # Take last card
        target_position = 1  # Move to position 1 (which is occupied)
        
        print(f"Moving card '{card_to_move['title']}' (ID {card_to_move['id']})")
        print(f"From end to position {target_position} in column {col_id}")
        print(f"Note: Position {target_position} is currently occupied")
        
        response = requests.put(
            f"{BASE_URL}/api/board/cards/{card_to_move['id']}",
            params={"session_id": session_id},
            json={"column_id": col_id, "position": target_position}
        )
        
        if response.status_code == 200:
            moved_card = response.json()
            print(f"✅ SUCCESS - Card moved to position {moved_card['position']}")
            print(f"   Column ID: {moved_card['column_id']}")
            print(f"   Card title: {moved_card['title']}")
        else:
            print(f"❌ FAILED - Status {response.status_code}")
            print(f"   Response: {response.text}")
    else:
        print(f"⊘ Skipped - Column has < 3 cards")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
print()

# TEST 3: Rapid moves in same column
print("TEST 3: Rapid moves (stress test)")
print("-" * 80)
try:
    col_id = board["columns"][0]["id"]
    cards = board["columns"][0]["cards"]
    if len(cards) > 2:
        card_to_move = cards[0]
        
        positions = [len(cards)-1, 1, 0, len(cards)-2, 2]
        print(f"Moving card '{card_to_move['title']}' rapidly:")
        
        success_count = 0
        for pos in positions:
            response = requests.put(
                f"{BASE_URL}/api/board/cards/{card_to_move['id']}",
                params={"session_id": session_id},
                json={"column_id": col_id, "position": pos}
            )
            if response.status_code == 200:
                success_count += 1
                print(f"  ✅ Position {pos}")
            else:
                print(f"  ❌ Position {pos} - Status {response.status_code}")
        
        print(f"✅ {success_count}/{len(positions)} rapid moves successful")
    else:
        print(f"⊘ Skipped - Column has < 3 cards")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
print()

# TEST 4: Move between columns (should still work)
print("TEST 4: Move between columns")
print("-" * 80)
try:
    if len(board["columns"]) > 1:
        source_col = board["columns"][0]
        target_col = board["columns"][1]
        card_to_move = source_col["cards"][0]
        
        print(f"Moving card '{card_to_move['title']}' from")
        print(f"  Column {source_col['id']}: {source_col['title']}")
        print(f"  To Column {target_col['id']}: {target_col['title']}")
        
        response = requests.put(
            f"{BASE_URL}/api/board/cards/{card_to_move['id']}",
            params={"session_id": session_id},
            json={"column_id": target_col["id"], "position": 0}
        )
        
        if response.status_code == 200:
            moved = response.json()
            print(f"✅ SUCCESS - Card moved to column {moved['column_id']}, position {moved['position']}")
        else:
            print(f"❌ FAILED - Status {response.status_code}")
    else:
        print(f"⊘ Skipped - Need at least 2 columns")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
print()

print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)
print()
print("SUMMARY:")
print("If all tests passed, drag-and-drop is working correctly.")
print("Cards can now be moved within sections and between sections.")
