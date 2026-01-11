#!/usr/bin/env python3
"""Test the new conversation flow: name -> age -> symptoms -> ward classification"""

import requests

def test_new_conversation_flow():
    """Test the new flow where AI asks for name first, then age, then symptoms, then classifies ward"""
    session_id = 'test_new_flow'
    base_url = 'http://localhost:8000/api/chat'

    print('Testing NEW conversation flow: Name -> Age -> Symptoms -> Ward Classification')
    print('=' * 70)

    messages = [
        'Hello',  # User starts conversation
        'John Smith',  # Name response
        '35',  # Age response
        'I have chest pain and difficulty breathing'  # Symptoms response
    ]

    for i, msg in enumerate(messages, 1):
        print(f'{i}. User: "{msg}"')

        response = requests.post(base_url, json={'message': msg, 'session_id': session_id})

        if response.status_code == 200:
            ai_response = response.json()['response']
            print(f'   AI: "{ai_response}"')
        else:
            print(f'   Error: {response.status_code}')
        print()

if __name__ == "__main__":
    test_new_conversation_flow()