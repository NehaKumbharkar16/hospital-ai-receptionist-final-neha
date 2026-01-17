#!/usr/bin/env python3
"""
Direct database verification using service role key
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables from backend/.env
backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(backend_env)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("\n" + "=" * 70)
print("HOSPITAL AI AGENT - DATABASE VERIFICATION")
print("=" * 70)

print("\n📋 Connecting to Supabase...")
print(f"URL: {SUPABASE_URL}")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ ERROR: Missing Supabase credentials in .env file")
    exit(1)

try:
    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    print("✅ Connected to Supabase with service role key")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

# Test each table
print("\n📊 Testing Table Access:\n")

tables = {
    'patients': 'Patient Records',
    'doctors': 'Doctor Information',
    'appointments': 'Appointments',
    'departments': 'Departments',
    'chat_sessions': 'Chat Sessions',
    'hospital_info': 'Hospital Info',
    'specializations': 'Specializations'
}

success_count = 0
failed_tables = []

for table, description in tables.items():
    try:
        response = client.table(table).select("*").limit(1).execute()
        print(f"✅ {description:25} - {table:25} OK ({len(response.data)} records)")
        success_count += 1
    except Exception as e:
        error = str(e).lower()
        if 'permission' in error or 'denied' in error or '42501' in str(e):
            print(f"❌ {description:25} - {table:25} RLS BLOCKING")
            failed_tables.append(table)
        elif 'not found' in error or 'does not exist' in error:
            print(f"⚠️  {description:25} - {table:25} TABLE NOT FOUND")
            failed_tables.append(table)
        else:
            print(f"⚠️  {description:25} - {table:25} ERROR: {str(e)[:40]}")
            failed_tables.append(table)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if success_count == len(tables):
    print(f"\n✅ ALL TESTS PASSED! ({success_count}/{len(tables)} tables connected)")
    print("\n🎉 Your Hospital AI Agent database is fully configured and ready!")
    print("   Frontend: http://localhost:5173")
    print("   Backend:  http://localhost:8000")
    exit(0)
else:
    print(f"\n⚠️  PARTIAL SUCCESS: {success_count}/{len(tables)} tables connected")
    
    if failed_tables:
        print(f"\n❌ Problem tables: {', '.join(failed_tables)}")
        print("\n💡 SOLUTIONS:")
        print("\n   Option 1 - Disable RLS in Supabase UI:")
        print("   1. Go to https://app.supabase.com")
        print("   2. Go to Authentication → Policies")
        print("   3. Find each table and click 'Disable RLS'")
        print("\n   Option 2 - Execute SQL directly:")
        print("   1. Go to https://app.supabase.com → SQL Editor")
        print("   2. Run this query:")
        print("\n" + "-" * 70)
        for table in failed_tables:
            print(f"   ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")
        print("-" * 70)
    
    exit(1)
