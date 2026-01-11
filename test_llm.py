#!/usr/bin/env python3
import requests

# Test the LLM classification
data = {'message': 'I have chest pain', 'session_id': 'test_llm'}
response = requests.post('http://localhost:8000/api/chat', json=data, timeout=10)

print(f'Status: {response.status_code}')
if response.status_code == 200:
    result = response.json()
    print(f'AI Response: {result["response"]}')
else:
    print(f'Error: {response.text}')