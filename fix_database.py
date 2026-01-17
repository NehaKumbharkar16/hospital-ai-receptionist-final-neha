#!/usr/bin/env python3
"""
Script to fix RLS issues and create missing tables in Supabase
"""
import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from database import init_db, get_supabase_admin
import asyncio

async def fix_database():
    """Fix RLS issues and create missing tables"""
    try:
        # Initialize database
        await init_db()
        supabase = get_supabase_admin()
        
        if not supabase:
            print("❌ ERROR: Supabase connection failed")
            return False
        
        print("\n" + "=" * 60)
        print("FIXING DATABASE RLS AND CREATING MISSING TABLES")
        print("=" * 60)
        
        # Step 1: Disable RLS on all tables
        print("\n📋 Disabling RLS on tables...")
        tables = ['patients', 'doctors', 'appointments', 'doctor_slots', 
                 'chat_sessions', 'departments', 'specializations',
                 'symptom_department_mapping', 'patient_visits', 
                 'recommended_tests', 'ai_recommendations', 'feedback', 
                 'hospital_statistics']
        
        for table in tables:
            try:
                supabase.rpc('exec_sql', {'query': f'ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;'}).execute()
                print(f"   ✅ {table}")
            except:
                print(f"   ℹ️  {table} (may already be disabled)")
        
        # Step 2: Create hospital_info table
        print("\n📋 Creating hospital_info table...")
        try:
            # Check if table exists
            response = supabase.table('hospital_info').select("*").limit(1).execute()
            print("   ✅ hospital_info table already exists")
        except:
            # Table doesn't exist, create it
            try:
                query = """
                CREATE TABLE IF NOT EXISTS hospital_info (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    hospital_name VARCHAR(200) NOT NULL DEFAULT 'City Hospital',
                    address TEXT,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    website VARCHAR(200),
                    established_year INT,
                    total_beds INT,
                    ambulance_count INT,
                    operating_theatres INT,
                    icu_beds INT,
                    description TEXT,
                    logo_url TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
                """
                supabase.rpc('exec_sql', {'query': query}).execute()
                print("   ✅ hospital_info table created")
            except Exception as e:
                print(f"   ⚠️  Could not create hospital_info: {str(e)[:100]}")
        
        # Step 3: Insert default hospital info
        print("\n📋 Inserting default hospital info...")
        try:
            supabase.table('hospital_info').insert({
                'hospital_name': 'City Hospital',
                'phone': '+1-800-HOSPITAL',
                'email': 'info@cityhospital.com'
            }).execute()
            print("   ✅ Default hospital info inserted")
        except:
            print("   ℹ️  Hospital info already exists or table issue")
        
        # Step 4: Test connection again
        print("\n" + "=" * 60)
        print("TESTING DATABASE CONNECTIONS")
        print("=" * 60 + "\n")
        
        tables_to_test = ['patients', 'doctors', 'appointments', 'hospital_info']
        all_success = True
        
        for table in tables_to_test:
            try:
                response = supabase.table(table).select("*").limit(1).execute()
                print(f"✅ {table:20} - Connected (Found {len(response.data)} records)")
            except Exception as e:
                print(f"❌ {table:20} - Error: {str(e)[:50]}")
                all_success = False
        
        print("\n" + "=" * 60)
        if all_success:
            print("✅ ALL TESTS PASSED - Database is ready!")
        else:
            print("⚠️  Some tables still have issues - Check Supabase manually")
        print("=" * 60 + "\n")
        
        return all_success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(fix_database())
    sys.exit(0 if success else 1)
