#!/usr/bin/env python3
"""Test script for deployed Hospital AI Agent"""

import requests
import sys

def test_deployment():
    """Test both local and deployed versions"""

    # Test URLs - update these with your deployed URLs
    BACKEND_URL = "http://localhost:8000"  # Change to your Render URL when deployed
    FRONTEND_URL = "http://localhost:5173"  # Change to your Vercel/Netlify URL when deployed

    print("🧪 Testing Hospital AI Agent Deployment")
    print("=" * 50)

    # Test Backend API
    print("🔧 Testing Backend API...")
    try:
        # Test health check
        health_response = requests.get(f"{BACKEND_URL}/", timeout=10)
        print(f"✅ Health Check: {health_response.status_code}")

        # Test chat API
        chat_data = {"message": "Hello", "session_id": "deploy_test"}
        chat_response = requests.post(f"{BACKEND_URL}/api/chat",
                                    json=chat_data, timeout=10)

        if chat_response.status_code == 200:
            result = chat_response.json()
            print("✅ Chat API: Working")
            print(f"   Response: {result['response'][:50]}...")
        else:
            print(f"❌ Chat API: HTTP {chat_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Backend Connection Failed: {e}")

    # Test Frontend (if running)
    print("\n🎨 Testing Frontend...")
    try:
        frontend_response = requests.get(FRONTEND_URL, timeout=10)
        print(f"✅ Frontend: {frontend_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Frontend Not Running: {e}")
        print("   (This is normal if testing backend only)")

    print("\n" + "=" * 50)

    # Instructions
    print("📋 Next Steps:")
    print("1. Update BACKEND_URL and FRONTEND_URL in this script")
    print("2. Deploy backend to Render (see DEPLOYMENT.md)")
    print("3. Deploy frontend to Vercel/Netlify")
    print("4. Update CORS settings in backend/main.py")
    print("5. Test the full deployed application!")

if __name__ == "__main__":
    test_deployment()