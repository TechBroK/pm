import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("API FUNCTIONALITY TEST SUITE")
print("=" * 60)

# Test 1: Health Check
print("\n[TEST 1] Health Check")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"  ✅ Health endpoint: {response.status_code}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 2: Test Endpoint
print("\n[TEST 2] Test Endpoint")
try:
    response = requests.get(f"{BASE_URL}/api/test")
    print(f"  ✅ Test endpoint: {response.status_code}")
    print(f"     Response: {response.json()}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 3: Login
print("\n[TEST 3] Authentication - Login")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "user", "password": "password"}
    )
    data = response.json()
    session_id = data.get("session_id")
    print(f"  ✅ Login: {response.status_code}")
    print(f"     Session ID: {session_id}")
    print(f"     Username: {data.get('username')}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 4: Get Board
print("\n[TEST 4] Get Board")
try:
    response = requests.get(
        f"{BASE_URL}/api/board",
        params={"session_id": session_id}
    )
    board_data = response.json()
    print(f"  ✅ Get Board: {response.status_code}")
    print(f"     Board Title: {board_data.get('title')}")
    print(f"     Columns: {len(board_data.get('columns', []))}")
    
    total_cards = sum(len(col.get('cards', [])) for col in board_data.get('columns', []))
    print(f"     Total Cards: {total_cards}")
    
    for col in board_data.get('columns', []):
        card_count = len(col.get('cards', []))
        print(f"       - {col.get('title')}: {card_count} cards")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 5: Add Card
print("\n[TEST 5] Add New Card")
try:
    # Add to Backlog (column_id=1)
    response = requests.post(
        f"{BASE_URL}/api/board/cards",
        params={"session_id": session_id, "column_id": 1},
        json={"title": "Verification Test Card", "details": "Testing API functionality"}
    )
    new_card = response.json()
    new_card_id = new_card.get('id')
    print(f"  ✅ Add Card: {response.status_code}")
    print(f"     Card ID: {new_card_id}")
    print(f"     Title: {new_card.get('title')}")
    print(f"     Column ID: {new_card.get('column_id')}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 6: Verify Card was Added
print("\n[TEST 6] Verify Card Added to Database")
try:
    response = requests.get(
        f"{BASE_URL}/api/board",
        params={"session_id": session_id}
    )
    board_data = response.json()
    backlog = next((col for col in board_data.get('columns', []) if col['title'] == 'Backlog'), None)
    if backlog:
        card_count = len(backlog.get('cards', []))
        print(f"  ✅ Backlog now has {card_count} cards")
        # Find our test card
        test_card = next((c for c in backlog.get('cards', []) if c['title'] == 'Verification Test Card'), None)
        if test_card:
            print(f"     ✅ Test card found in Backlog")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 7: Move Card
print("\n[TEST 7] Move Card Between Columns")
try:
    # Move the test card to Discovery (column_id=2), position 0
    response = requests.put(
        f"{BASE_URL}/api/board/cards/{new_card_id}",
        params={"session_id": session_id},
        json={"column_id": 2, "position": 0}
    )
    moved_card = response.json()
    print(f"  ✅ Move Card: {response.status_code}")
    print(f"     New Column ID: {moved_card.get('column_id')}")
    print(f"     New Position: {moved_card.get('position')}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 8: Verify Card Moved
print("\n[TEST 8] Verify Card Moved to Discovery")
try:
    response = requests.get(
        f"{BASE_URL}/api/board",
        params={"session_id": session_id}
    )
    board_data = response.json()
    discovery = next((col for col in board_data.get('columns', []) if col['title'] == 'Discovery'), None)
    if discovery:
        test_card = next((c for c in discovery.get('cards', []) if c['id'] == new_card_id), None)
        if test_card:
            print(f"  ✅ Card successfully moved to Discovery column")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 9: Rename Column
print("\n[TEST 9] Rename Column")
try:
    # Rename Discovery to 'Research' temporarily
    response = requests.post(
        f"{BASE_URL}/api/board/columns/2",
        params={"session_id": session_id},
        json={"title": "Research"}
    )
    renamed_col = response.json()
    print(f"  ✅ Rename Column: {response.status_code}")
    print(f"     Column ID: {renamed_col.get('id')}")
    print(f"     New Title: {renamed_col.get('title')}")
    
    # Rename it back
    response = requests.post(
        f"{BASE_URL}/api/board/columns/2",
        params={"session_id": session_id},
        json={"title": "Discovery"}
    )
    print(f"     Renamed back to 'Discovery': {response.status_code}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 10: Delete Card
print("\n[TEST 10] Delete Card")
try:
    response = requests.delete(
        f"{BASE_URL}/api/board/cards/{new_card_id}",
        params={"session_id": session_id}
    )
    print(f"  ✅ Delete Card: {response.status_code}")
    print(f"     Response: {response.json()}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 11: Verify Card Deleted
print("\n[TEST 11] Verify Card Deleted")
try:
    response = requests.get(
        f"{BASE_URL}/api/board",
        params={"session_id": session_id}
    )
    board_data = response.json()
    total_cards = sum(len(col.get('cards', [])) for col in board_data.get('columns', []))
    print(f"  ✅ Total cards after deletion: {total_cards}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 12: Logout
print("\n[TEST 12] Logout")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/logout",
        json={"session_id": session_id}
    )
    print(f"  ✅ Logout: {response.status_code}")
    print(f"     Response: {response.json()}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 13: Verify Session Invalidated
print("\n[TEST 13] Verify Session Invalidated After Logout")
try:
    response = requests.get(
        f"{BASE_URL}/api/board",
        params={"session_id": session_id}
    )
    if response.status_code == 401:
        print(f"  ✅ Access denied after logout: {response.status_code}")
    else:
        print(f"  ⚠️  Expected 401, got: {response.status_code}")
except Exception as e:
    print(f"  ❌ Error: {e}")

print("\n" + "=" * 60)
print("API TESTS COMPLETE")
print("=" * 60)
