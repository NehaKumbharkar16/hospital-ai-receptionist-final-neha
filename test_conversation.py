#!/usr/bin/env python3
"""Test the conversation flow to verify state management"""

import requests
import json

def test_conversation():
    session_id = 'test_conv_123'
    base_url = 'http://localhost:8000/api/chat'

    # Test conversation flow
    messages = [
        'I have a headache',  # Initial query
        'John Doe',           # Name response
        '35'                  # Age response
    ]

    print("Testing conversation flow...\n")

    for i, msg in enumerate(messages):
        print(f'Step {i+1}: User says "{msg}"')

        data = {'message': msg, 'session_id': session_id}
        response = requests.post(base_url, json=data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print(f'AI: "{result["response"]}"')
        else:
            print(f'Error: {response.status_code} - {response.text}')
        print()

if __name__ == "__main__":
    test_conversation()