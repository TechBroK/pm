"""Diagnose OpenRouter API connectivity issues."""

import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
print(f"API Key loaded: {bool(API_KEY)}")
if API_KEY:
    print(f"Key format: {API_KEY[:30]}...")

print("\n" + "="*70)
print("TESTING OPENROUTER API")
print("="*70)

# Test 1: Basic models endpoint (no auth needed usually)
print("\n[Test 1] GET /models (no auth)")
try:
    resp = httpx.get("https://openrouter.io/api/v1/models", timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        models = data.get("data", [])
        print(f"Found {len(models)} models")
        if models:
            print(f"First model: {models[0].get('id')}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Chat completion with exact format
print("\n[Test 2] POST /chat/completions (with auth)")
try:
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "What is 2+2?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "PM App"
    }
    
    print(f"Headers: {json.dumps({k: v[:30] + '...' if len(str(v)) > 30 else v for k, v in headers.items()}, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    resp = httpx.post(
        "https://openrouter.io/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    print(f"Status: {resp.status_code}")
    print(f"Headers: {dict(resp.headers)}")
    if resp.content:
        try:
            print(f"Response: {resp.json()}")
        except:
            print(f"Response (raw): {resp.text[:200]}")
    else:
        print("Response: (empty)")
        
except Exception as e:
    print(f"Error: {e}")

# Test 3: Try alternative model
print("\n[Test 3] POST /chat/completions (alternative model)")
try:
    payload = {
        "model": "meta-llama/llama-2-7b-chat",
        "messages": [
            {"role": "user", "content": "Hello"}
        ]
    }
    
    resp = httpx.post(
        "https://openrouter.io/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=10
    )
    
    print(f"Status: {resp.status_code}")
    if resp.content:
        print(f"Response snippet: {resp.text[:300]}")
        
except Exception as e:
    print(f"Error: {e}")

# Test 4: Check if API key is valid format
print("\n[Test 4] API Key validation")
if API_KEY and API_KEY.startswith("sk-or-v1-"):
    print("✓ API key format looks correct (sk-or-v1-*)")
else:
    print("✗ API key format looks WRONG or missing")

# Test 5: Check IP/network
print("\n[Test 5] Network connectivity")
try:
    resp = httpx.get("https://openrouter.io", timeout=5)
    print(f"✓ Can reach openrouter.io (status: {resp.status_code})")
except Exception as e:
    print(f"✗ Cannot reach openrouter.io: {e}")

print("\n" + "="*70)
