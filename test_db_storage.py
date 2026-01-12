#!/usr/bin/env python3
"""Test database storage functionality"""

import requests
import time

def test_database_storage():
    """Test if patient data is being stored in Supabase"""
    session_id = f'db_test_{int(time.time())}'
    base_url = 'http://localhost:8000/api/chat'

    print('Testing Database Storage')
    print('=' * 40)

    # Complete conversation
    messages = [
        'Hi',  # Start
        'Alice Johnson',  # Name
        '28',  # Age
        'I have severe headache and nausea'  # Symptoms
    ]

    for i, msg in enumerate(messages, 1):
        response = requests.post(base_url, json={'message': msg, 'session_id': session_id})

        if response.status_code == 200:
            ai_response = response.json()['response']
            print(f'{i}. User: "{msg}"')
            print(f'   AI: "{ai_response[:60]}..."')
        else:
            print(f'{i}. Error with "{msg}": {response.status_code}')
        print()

    print('✅ Complete conversation finished!')
    print('📊 Check your Supabase dashboard for the stored patient record')
    print(f'   Session ID: {session_id}')
    print('   Expected data: Alice Johnson, age 28, headache symptoms')

if __name__ == "__main__":
    test_database_storage()