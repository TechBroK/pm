#!/usr/bin/env python3
"""Debug OpenRouter API connection."""
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

# Test AI connection
print("Testing OpenRouter API connection...\n")

# Get test response
response = requests.get(f"{BASE_URL}/api/ai/test")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Check if API key is loaded
api_key = os.getenv("OPENROUTER_API_KEY")
print(f"\nAPI Key loaded: {bool(api_key)}")
if api_key:
    print(f"Key (first 20 chars): {api_key[:20]}...")

# Try direct OpenRouter call
print("\n" + "="*60)
print("Testing direct OpenRouter API call...")
print("="*60)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

payload = {
    "model": "openai/gpt-oss-120b",
    "messages": [{"role": "user", "content": "What is 2 + 2?"}],
    "temperature": 0.7,
    "max_tokens": 100,
}

try:
    direct_response = requests.post(
        "https://openrouter.io/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    print(f"Status: {direct_response.status_code}")
    print(f"Response:\n{json.dumps(direct_response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
