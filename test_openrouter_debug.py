#!/usr/bin/env python3
"""
Comprehensive OpenRouter API debugging and testing.
Tests different models and request formats to identify the 405 error.
"""

import os
import httpx
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.io/api/v1/chat/completions"

print("=" * 80)
print("OPENROUTER API DEBUGGING")
print("=" * 80)
print(f"API Key configured: {'Yes' if OPENROUTER_API_KEY else 'No'}")
print(f"API Key (first 20 chars): {OPENROUTER_API_KEY[:20] if OPENROUTER_API_KEY else 'N/A'}...")
print()

# Test 1: Simple request with gpt-3.5-turbo
print("TEST 1: Basic request with gpt-3.5-turbo")
print("-" * 80)
try:
    response = httpx.post(
        OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://127.0.0.1:8000",
            "X-Title": "Kanban Studio",
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "What is 2 + 2?"}],
            "temperature": 0.7,
            "max_tokens": 100,
        },
        timeout=30.0,
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    if response.status_code == 200:
        data = response.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"✅ SUCCESS: {answer}")
    else:
        print(f"❌ ERROR: {response.status_code}")
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")

print()

# Test 2: Alternative model (meta-llama/llama-2-7b-chat)
print("TEST 2: Trying alternative model (meta-llama/llama-2-7b-chat)")
print("-" * 80)
try:
    response = httpx.post(
        OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://127.0.0.1:8000",
            "X-Title": "Kanban Studio",
        },
        json={
            "model": "meta-llama/llama-2-7b-chat",
            "messages": [{"role": "user", "content": "What is 2 + 2?"}],
            "temperature": 0.7,
            "max_tokens": 100,
        },
        timeout=30.0,
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    if response.status_code == 200:
        data = response.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"✅ SUCCESS: {answer}")
    else:
        print(f"❌ ERROR: {response.status_code}")
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")

print()

# Test 3: Using openai/gpt-4 (if available)
print("TEST 3: Trying GPT-4 (openai/gpt-4)")
print("-" * 80)
try:
    response = httpx.post(
        OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://127.0.0.1:8000",
            "X-Title": "Kanban Studio",
        },
        json={
            "model": "openai/gpt-4",
            "messages": [{"role": "user", "content": "What is 2 + 2?"}],
            "temperature": 0.7,
            "max_tokens": 100,
        },
        timeout=30.0,
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    if response.status_code == 200:
        data = response.json()
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"✅ SUCCESS: {answer}")
    else:
        print(f"❌ ERROR: {response.status_code}")
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")

print()

# Test 4: Check available models endpoint
print("TEST 4: Fetch available models from OpenRouter")
print("-" * 80)
try:
    response = httpx.get(
        "https://openrouter.io/api/v1/models",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        timeout=10.0,
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        models = data.get("data", [])
        print(f"Available models: {len(models)}")
        # Show first 5 models
        for i, model in enumerate(models[:5]):
            print(f"  - {model.get('id')}")
        if len(models) > 5:
            print(f"  ... and {len(models) - 5} more")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")

print()

# Test 5: Direct simple POST to verify API key works
print("TEST 5: Verify API key is valid (using echo endpoint)")
print("-" * 80)
try:
    response = httpx.post(
        OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Say 'hello'"}],
        },
        timeout=30.0,
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")

print()
print("=" * 80)
print("DEBUGGING COMPLETE")
print("=" * 80)
