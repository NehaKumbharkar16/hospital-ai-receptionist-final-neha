#!/usr/bin/env python3
"""Test the improved conversation flow"""

import requests

def test_improved_flow():
    """Test the enhanced conversation with ward info and symptom details"""
    session_id = 'test_improved_flow'
    base_url = 'http://localhost:8000/api/chat'

    print('Testing improved conversation flow:')
    print('=' * 50)

    messages = [
        'I have a headache',  # Initial symptom
        'I have a severe headache and feel dizzy',  # Detailed symptoms
        'John Smith',  # Name
        '35'  # Age
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
    test_improved_flow()