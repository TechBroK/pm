#!/usr/bin/env python
"""Test script to verify OpenRouter AI connectivity."""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_ai_connectivity():
    """Test the AI connectivity endpoint."""
    print("Testing OpenRouter AI connectivity...")
    
    url = f"{BASE_URL}/api/ai/test"
    print(f"GET {url}")
    
    try:
        response = requests.get(url)
        data = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get("success"):
            print("\n✓ AI connectivity SUCCESS!")
            print(f"Model response: {data.get('response')}")
        else:
            print(f"\n✗ AI connectivity FAILED")
            print(f"Error: {data.get('error')}")
            print(f"Detail: {data.get('detail')}")
            
        return data.get("success", False)
        
    except Exception as e:
        print(f"✗ Request failed: {e}")
        return False

def test_board_api():
    """Test that we can get board data."""
    print("\n\nTesting board API...")
    
    # First login
    login_url = f"{BASE_URL}/api/auth/login"
    login_data = {"username": "user", "password": "password"}
    
    print(f"POST {login_url}")
    print(f"Body: {json.dumps(login_data)}")
    
    try:
        response = requests.post(login_url, json=login_data)
        login_result = response.json()
        print(f"Response: {json.dumps(login_result, indent=2)}")
        
        if response.status_code != 200:
            print("✗ Login failed")
            return False
            
        session_id = login_result.get("session_id")
        print(f"✓ Logged in with session: {session_id}")
        
        # Get board
        board_url = f"{BASE_URL}/api/board?session_id={session_id}"
        print(f"\nGET {board_url}")
        
        response = requests.get(board_url)
        board_data = response.json()
        
        print(f"Board loaded successfully!")
        print(f"Title: {board_data.get('title')}")
        print(f"Columns: {len(board_data.get('columns', []))}")
        
        total_cards = sum(len(col.get('cards', [])) for col in board_data.get('columns', []))
        print(f"Total cards: {total_cards}")
        
        return True
        
    except Exception as e:
        print(f"✗ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PM Backend - AI Integration Test")
    print("=" * 60)
    
    ai_ok = test_ai_connectivity()
    board_ok = test_board_api()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  AI Connectivity: {'✓ PASS' if ai_ok else '✗ FAIL'}")
    print(f"  Board API: {'✓ PASS' if board_ok else '✗ FAIL'}")
    print("=" * 60)
    
    sys.exit(0 if (ai_ok and board_ok) else 1)
