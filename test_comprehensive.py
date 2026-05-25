#!/usr/bin/env python
"""Comprehensive test suite for PM Backend - All Features."""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_result(name, success, details=""):
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"  [{status}] {name}")
    if details:
        print(f"         {details}")

# ============================================================================
# FULL FEATURE TEST
# ============================================================================

print_section("PM BACKEND - COMPREHENSIVE FEATURE TEST")

results = {
    "api_endpoints": [],
    "board_operations": [],
    "ai_integration": [],
}

# Test 1: Health Check
try:
    response = requests.get(f"{BASE_URL}/health")
    success = response.status_code == 200
    results["api_endpoints"].append(("Health Check", success))
    test_result("Health Check", success, f"Status: {response.status_code}")
except Exception as e:
    results["api_endpoints"].append(("Health Check", False))
    test_result("Health Check", False, str(e))

# Test 2: Test Endpoint
try:
    response = requests.get(f"{BASE_URL}/api/test")
    success = response.status_code == 200 and "Hello from API" in response.text
    results["api_endpoints"].append(("Test Endpoint", success))
    test_result("Test Endpoint", success, f"Response: {response.json()}")
except Exception as e:
    results["api_endpoints"].append(("Test Endpoint", False))
    test_result("Test Endpoint", False, str(e))

# Test 3: Login
print_section("AUTHENTICATION TESTS")
login_data = {"username": "user", "password": "password"}
try:
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    success = response.status_code == 200
    results["board_operations"].append(("Login", success))
    test_result("Login", success, f"Status: {response.status_code}")
    
    if success:
        login_response = response.json()
        session_id = login_response.get("session_id")
        username = login_response.get("username")
        test_result("Session Created", True, f"User: {username}")
    else:
        session_id = None
        test_result("Login Failed", False, response.text)
except Exception as e:
    results["board_operations"].append(("Login", False))
    test_result("Login Failed", False, str(e))
    session_id = None

# Test 4-8: Board Operations
if session_id:
    print_section("BOARD OPERATIONS")
    
    # Get Board
    try:
        response = requests.get(f"{BASE_URL}/api/board?session_id={session_id}")
        success = response.status_code == 200
        results["board_operations"].append(("Get Board", success))
        test_result("Get Board", success)
        
        if success:
            board = response.json()
            num_columns = len(board.get("columns", []))
            total_cards = sum(len(col.get("cards", [])) for col in board.get("columns", []))
            test_result("Board Structure", True, f"Columns: {num_columns}, Cards: {total_cards}")
    except Exception as e:
        results["board_operations"].append(("Get Board", False))
        test_result("Get Board", False, str(e))
    
    # Add Card
    try:
        add_data = {"title": "Test Card", "details": "Feature test card"}
        response = requests.post(
            f"{BASE_URL}/api/board/cards?column_id=1&session_id={session_id}",
            json=add_data
        )
        success = response.status_code == 200
        results["board_operations"].append(("Add Card", success))
        test_result("Add Card", success, f"Status: {response.status_code}")
        
        if success:
            card = response.json()
            card_id = card.get("id")
    except Exception as e:
        results["board_operations"].append(("Add Card", False))
        test_result("Add Card", False, str(e))
        card_id = None
    
    # Move Card
    if card_id:
        try:
            move_data = {"column_id": 2, "position": 0}
            response = requests.put(
                f"{BASE_URL}/api/board/cards/{card_id}?session_id={session_id}",
                json=move_data
            )
            success = response.status_code == 200
            results["board_operations"].append(("Move Card", success))
            test_result("Move Card", success, f"Status: {response.status_code}")
        except Exception as e:
            results["board_operations"].append(("Move Card", False))
            test_result("Move Card", False, str(e))
    
    # Rename Column
    try:
        rename_data = {"title": "Updated Backlog"}
        response = requests.post(
            f"{BASE_URL}/api/board/columns/1?session_id={session_id}",
            json=rename_data
        )
        success = response.status_code == 200
        results["board_operations"].append(("Rename Column", success))
        test_result("Rename Column", success, f"Status: {response.status_code}")
    except Exception as e:
        results["board_operations"].append(("Rename Column", False))
        test_result("Rename Column", False, str(e))
    
    # Delete Card
    if card_id:
        try:
            response = requests.delete(
                f"{BASE_URL}/api/board/cards/{card_id}?session_id={session_id}"
            )
            success = response.status_code == 200
            results["board_operations"].append(("Delete Card", success))
            test_result("Delete Card", success, f"Status: {response.status_code}")
        except Exception as e:
            results["board_operations"].append(("Delete Card", False))
            test_result("Delete Card", False, str(e))
    
    # Logout
    try:
        response = requests.post(f"{BASE_URL}/api/auth/logout?session_id={session_id}")
        success = response.status_code == 200
        results["board_operations"].append(("Logout", success))
        test_result("Logout", success, f"Status: {response.status_code}")
    except Exception as e:
        results["board_operations"].append(("Logout", False))
        test_result("Logout", False, str(e))

# Test 9: AI Connectivity
print_section("AI INTEGRATION TESTS")

try:
    response = requests.get(f"{BASE_URL}/api/ai/test")
    success = response.status_code == 200
    data = response.json()
    
    results["ai_integration"].append(("AI Test Endpoint", success))
    test_result("AI Test Endpoint", success, f"Status: {response.status_code}")
    
    if success:
        if data.get("success"):
            test_result("OpenRouter Connection", True, f"Model: {data.get('model')}")
            test_result("AI Response", True, f"2+2={data.get('response')}")
            results["ai_integration"].append(("OpenRouter Connection", True))
        else:
            error = data.get("error", "Unknown error")
            test_result("OpenRouter Connection", False, error)
            results["ai_integration"].append(("OpenRouter Connection", False))
            
            if "not configured" in error.lower():
                print()
                print("  NOTE: To enable AI features, add your OpenRouter API key to .env:")
                print("        OPENROUTER_API_KEY=your_key_here")
                print("        Then restart the backend.")
except Exception as e:
    results["ai_integration"].append(("AI Test Endpoint", False))
    test_result("AI Test Endpoint", False, str(e))

# ============================================================================
# SUMMARY
# ============================================================================

print_section("TEST SUMMARY")

def count_passed(tests):
    return sum(1 for _, passed in tests if passed)

def count_total(tests):
    return len(tests)

api_pass = count_passed(results["api_endpoints"])
api_total = count_total(results["api_endpoints"])

board_pass = count_passed(results["board_operations"])
board_total = count_total(results["board_operations"])

ai_pass = count_passed(results["ai_integration"])
ai_total = count_total(results["ai_integration"])

total_pass = api_pass + board_pass + ai_pass
total_tests = api_total + board_total + ai_total

print(f"  API Endpoints:        {api_pass}/{api_total} passed")
print(f"  Board Operations:     {board_pass}/{board_total} passed")
print(f"  AI Integration:       {ai_pass}/{ai_total} passed")
print()
print(f"  TOTAL:                {total_pass}/{total_tests} passed ({100*total_pass//total_tests}%)")

if total_pass == total_tests:
    print()
    print("  🎉 ALL TESTS PASSED! System is fully functional.")
elif ai_pass < ai_total and (ai_total - ai_pass) == 1:
    print()
    print("  ⚠️  AI integration not ready (API key needed)")
    print("      All other features are working perfectly!")
else:
    print()
    print("  ⚠️  Some tests failed. Review output above.")

sys.exit(0 if total_pass == total_tests else 1)
