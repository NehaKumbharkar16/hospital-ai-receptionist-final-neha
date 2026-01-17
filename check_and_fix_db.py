#!/usr/bin/env python3
"""
Script to fix database issues by:
1. Creating missing hospital_info table
2. Attempting to disable RLS through table operations
"""
import sys
import os
import asyncio

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from database import init_db, get_supabase_admin
from dotenv import load_dotenv

load_dotenv()

async def fix_database():
    """Fix RLS issues and create missing tables"""
    try:
        # Initialize database
        await init_db()
        supabase = get_supabase_admin()
        
        if not supabase:
            print("❌ ERROR: Supabase connection failed")
            return False
        
        print("\n" + "=" * 70)
        print("HOSPITAL AI AGENT - DATABASE CONFIGURATION")
        print("=" * 70)
        
        # Step 1: Check and create hospital_info table
        print("\n📋 Step 1: Checking hospital_info table...")
        try:
            response = supabase.table('hospital_info').select("*").limit(1).execute()
            print("   ✅ hospital_info table exists")
            if len(response.data) > 0:
                print(f"      Hospital: {response.data[0].get('hospital_name', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  hospital_info table not found or inaccessible")
            print(f"      Error: {str(e)[:100]}")
            
            # Try to create it with upsert
            print("\n   🔧 Creating hospital_info table via insert...")
            try:
                data = {
                    'hospital_name': 'City Hospital',
                    'phone': '+1-800-HOSPITAL',
                    'email': 'info@cityhospital.com',
                    'address': '123 Main Street, Medical City',
                    'total_beds': 500,
                    'ambulance_count': 10,
                    'operating_theatres': 8
                }
                result = supabase.table('hospital_info').insert(data, count='exact').execute()
                print("   ✅ hospital_info record created successfully")
            except Exception as insert_err:
                print(f"   ℹ️  Insert failed (table may not exist): {str(insert_err)[:80]}")
        
        # Step 2: Test main table access
        print("\n📋 Step 2: Testing table access...")
        tables_to_test = {
            'patients': 'Patient Records',
            'doctors': 'Doctor Information',
            'appointments': 'Appointments',
            'departments': 'Departments',
            'chat_sessions': 'Chat Sessions'
        }
        
        results = {}
        for table, description in tables_to_test.items():
            try:
                response = supabase.table(table).select("*").limit(1).execute()
                status = f"✅ {description:25} - OK ({len(response.data)} records)"
                results[table] = True
                print(f"   {status}")
            except Exception as e:
                error_msg = str(e).lower()
                if 'permission' in error_msg or 'denied' in error_msg:
                    status = f"❌ {description:25} - RLS BLOCKING ACCESS"
                    results[table] = False
                else:
                    status = f"⚠️  {description:25} - {str(e)[:50]}"
                    results[table] = None
                print(f"   {status}")
        
        # Step 3: Provide solution summary
        print("\n" + "=" * 70)
        print("CONFIGURATION SUMMARY")
        print("=" * 70)
        
        blocked_tables = [t for t, r in results.items() if r is False]
        
        if blocked_tables:
            print("\n⚠️  ISSUE FOUND: Row Level Security (RLS) is blocking access")
            print(f"    Affected tables: {', '.join(blocked_tables)}")
            
            print("\n📝 SOLUTION: Disable RLS in Supabase Console")
            print("    1. Go to: https://app.supabase.com")
            print("    2. Select your project")
            print("    3. Go to: Authentication → Policies")
            print("    4. For each affected table, click 'Disable RLS'")
            print("    5. OR manually execute in SQL Editor:")
            print("\n" + "-" * 70)
            for table in blocked_tables:
                print(f"    ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")
            print("-" * 70)
        
        all_ok = all(r is True for r in results.values())
        
        if all_ok:
            print("\n✅ ALL CHECKS PASSED - Database is fully configured!")
            print("   Your Hospital AI Agent is ready to use.")
        else:
            print("\n⚠️  ACTION REQUIRED - Please follow the solution steps above")
            print("   Once RLS is disabled, re-run this script to verify.")
        
        print("\n" + "=" * 70 + "\n")
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(fix_database())
    sys.exit(0 if success else 1)
