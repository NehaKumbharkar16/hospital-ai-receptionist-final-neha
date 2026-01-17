#!/usr/bin/env python3
"""
Diagnostic script to show what credentials are being used
Add this to your backend to debug Render issues
"""
import os
from dotenv import load_dotenv

print("\n" + "=" * 70)
print("ENVIRONMENT DIAGNOSTIC")
print("=" * 70 + "\n")

# Try to load from multiple locations
print("📋 Checking environment variables...\n")

# Load from backend/.env
backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(backend_env)

# Check what we have
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("SUPABASE_URL:")
if SUPABASE_URL:
    print(f"  ✅ {SUPABASE_URL}")
else:
    print("  ❌ NOT SET")

print("\nSUPABASE_ANON_KEY:")
if SUPABASE_ANON_KEY:
    print(f"  ✅ Set ({len(SUPABASE_ANON_KEY)} chars)")
else:
    print("  ❌ NOT SET")

print("\nSUPABASE_SERVICE_ROLE_KEY:")
if SUPABASE_SERVICE_ROLE_KEY:
    print(f"  ✅ Set ({len(SUPABASE_SERVICE_ROLE_KEY)} chars)")
else:
    print("  ❌ NOT SET - THIS IS THE PROBLEM!")
    print("     Without this, Render can only use ANON key which respects RLS!")

print("\nGOOGLE_API_KEY:")
if GOOGLE_API_KEY:
    print(f"  ✅ Set ({len(GOOGLE_API_KEY)} chars)")
else:
    print("  ⚠️  Not set (optional for Render)")

print("\n" + "=" * 70)
print("DIAGNOSIS")
print("=" * 70 + "\n")

if not SUPABASE_SERVICE_ROLE_KEY:
    print("🔴 CRITICAL: SERVICE_ROLE_KEY IS MISSING!")
    print("\nThis is why you're getting permission denied:")
    print("  1. Code tries to use service role key")
    print("  2. Service role key is empty")
    print("  3. Falls back to anon key")
    print("  4. Anon key respects RLS → permission denied")
    
    print("\n✅ FIX:")
    print("  1. Go to Render dashboard")
    print("  2. Click Hospital AI Agent service")
    print("  3. Click 'Environment' or 'Settings'")
    print("  4. Add this variable:")
    print("     Name: SUPABASE_SERVICE_ROLE_KEY")
    print("     Value: (copy from backend/.env)")
    print("  5. Click Save")
    print("  6. Manual Deploy")
else:
    print("✅ Service role key is set")
    print("\nIf still getting permission denied:")
    print("  1. RLS might not be fully disabled")
    print("  2. Key might be incorrect/expired")
    print("  3. Database connection might be stale")

print("\n" + "=" * 70 + "\n")
