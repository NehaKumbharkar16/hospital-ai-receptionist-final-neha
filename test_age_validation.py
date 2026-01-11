#!/usr/bin/env python3
"""Test age validation - only numeric input should be accepted"""

import requests

def test_age_validation():
    """Test that only numeric age input is accepted"""
    session_id = 'test_age_validation'
    base_url = 'http://localhost:8000/api/chat'

    print('Testing Age Validation - Only Numbers Accepted')
    print('=' * 50)

    messages = [
        'Hello',  # Start conversation
        'John Smith',  # Valid name
        'twenty five',  # Invalid age (words)
        '25',  # Valid age (numbers)
        'I have a headache'  # Valid symptoms
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
    test_age_validation()