#!/usr/bin/env python3
"""
Integration test demonstrating the complete Hospital AI Receptionist system.
This simulates a full conversation from user query to webhook trigger.
"""

import requests
import time
import json
from typing import List, Dict

def simulate_conversation():
    """Simulate a complete conversation with the AI receptionist"""
    print("=== Hospital AI Receptionist Integration Test ===\n")

    # Test conversation flow
    conversation = [
        "I have chest pain and difficulty breathing",
        "John Smith",
        "45"
    ]

    session_id = f"test_session_{int(time.time())}"
    base_url = "http://localhost:8000"

    print(f"Starting conversation with session ID: {session_id}")
    print("-" * 60)

    for i, user_message in enumerate(conversation, 1):
        print(f"Step {i}: User says: '{user_message}'")

        # Send message to API
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={
                    "message": user_message,
                    "session_id": session_id
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "No response")
                print(f"AI responds: '{ai_response}'")
            else:
                print(f"Error: HTTP {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        print()

    print("Conversation completed!")
    print("\nNote: In a real scenario, the webhook would be triggered when all patient")
    print("information is collected. Check your webhook endpoint for the payload.")

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✓ Backend API is running")
            return True
        else:
            print(f"✗ Backend API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("✗ Backend API is not accessible")
        return False

def main():
    print("Checking system status...\n")

    api_running = check_api_health()

    if not api_running:
        print("\nTo run this test:")
        print("1. Start the backend: cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("2. Set up environment variables (SUPABASE_URL, SUPABASE_ANON_KEY, WEBHOOK_URL)")
        print("3. Run this test again")
        return

    print("\nStarting integration test...\n")
    simulate_conversation()

if __name__ == "__main__":
    main()