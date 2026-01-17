#!/usr/bin/env python3
"""
Database verification using anon key (tests public access)
"""
import os
from dotenv import load_dotenv
from supabase import create_client
import time

# Load environment variables from backend/.env
backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(backend_env)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("\n" + "=" * 70)
print("HOSPITAL AI AGENT - DATABASE VERIFICATION (ANON KEY)")
print("=" * 70)

print("\n📋 Connecting to Supabase with ANON key (public access)...")
print(f"URL: {SUPABASE_URL}")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    print("❌ ERROR: Missing Supabase credentials in .env file")
    exit(1)

try:
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    print("✅ Connected to Supabase with anon key")
    time.sleep(1)  # Small delay for connection to settle
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
            print(f"⚠️  {description:25} - {table:25} {str(e)[:50]}")
            failed_tables.append(table)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if success_count == len(tables):
    print(f"\n✅ SUCCESS! All {len(tables)} tables are accessible!")
    print("\n🎉 Your Hospital AI Agent database is fully configured!")
    print("\n📱 Access the application:")
    print("   Frontend: http://localhost:5173")
    print("   Backend:  http://localhost:8000")
    print("\n✨ Database connection verified and working!\n")
    exit(0)
else:
    print(f"\n⚠️  {success_count}/{len(tables)} tables connected")
    
    if failed_tables:
        print(f"\n❌ Inaccessible tables: {', '.join(failed_tables)}")
        print("\n💡 The RLS commands in Supabase may not have taken effect yet.")
        print("   Try refreshing the page or waiting a few seconds.")
        print("\n   If issue persists, scroll down in Supabase Policies page")
        print("   and disable RLS for these remaining tables:")
        for table in failed_tables:
            print(f"      - {table}")
    
    exit(1)
