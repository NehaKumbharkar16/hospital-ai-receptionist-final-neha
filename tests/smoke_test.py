import os
import requests
import sys

BACKEND = os.getenv('BACKEND_URL', 'https://hospital-ai-receptionist-final.onrender.com')
FRONTEND = os.getenv('FRONTEND_URL', 'https://hospital-ai-receptionist-final-neha-9qgygfs0d.vercel.app')

print('Backend:', BACKEND)
print('Frontend:', FRONTEND)

# Check frontend
try:
    r = requests.get(FRONTEND + '/', timeout=10)
    print('Frontend status:', r.status_code)
    if r.status_code != 200:
        print('Frontend did not return 200 OK')
        sys.exit(1)
except Exception as e:
    print('Frontend check failed:', e)
    sys.exit(1)

# Check backend chat endpoint
payload = {'message': 'Smoke test: I have a fever and cough', 'session_id': 'smoke_test'}
try:
    r = requests.post(BACKEND + '/api/chat', json=payload, timeout=20)
    print('Backend /api/chat status:', r.status_code)
    if r.status_code != 200:
        print('Backend chat endpoint returned non-200')
        print(r.text)
        sys.exit(1)
    data = r.json()
    if 'response' not in data or not data['response']:
        print('Backend response missing expected "response" property')
        print(data)
        sys.exit(1)
    print('Backend response OK (preview):', data['response'][:200])
except Exception as e:
    print('Backend check failed:', e)
    sys.exit(1)

print('\nSmoke test passed ✅')
