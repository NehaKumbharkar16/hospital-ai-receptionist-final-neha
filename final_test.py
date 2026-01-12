#!/usr/bin/env python3
"""Final test of the age validation system"""

import requests

def test_final_system():
    """Test the complete age validation and conversation flow"""
    session_id = 'final_test'
    base_url = 'http://localhost:8000/api/chat'

    print('Final System Test - Age Validation')
    print('=' * 50)

    # Test conversation with age validation
    messages = [
        'Hi',  # Start
        'Sarah Johnson',  # Valid name
        'thirty',  # Invalid age (words)
        '25',  # Valid age (numbers)
        'I have severe chest pain'  # Emergency symptoms
    ]

    for i, msg in enumerate(messages, 1):
        response = requests.post(base_url, json={'message': msg, 'session_id': session_id})

        if response.status_code == 200:
            ai_response = response.json()['response']
            print(f'{i}. User: "{msg}"')
            print(f'   AI: "{ai_response}"')
        else:
            print(f'{i}. Error with "{msg}": {response.status_code}')
        print()

if __name__ == "__main__":
    test_final_system()