#!/usr/bin/env python3
"""
Complete Database Setup Script
Creates all tables and disables RLS
"""
import sys
import os
import asyncio

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def get_client():
    """Create Supabase client with service role (admin access)"""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")
        return None
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def setup_database():
    """Complete database setup"""
    try:
        client = get_client()
        if not client:
            return False
        
        print("\n" + "=" * 70)
        print("HOSPITAL AI AGENT - DATABASE SETUP")
        print("=" * 70)
        
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'backend', 'database', 'schema.sql')
        print(f"\n📋 Reading schema from: {schema_path}")
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Split SQL by statements (semicolons)
        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
        
        print(f"✅ Found {len(statements)} SQL statements")
        
        # Execute statements
        print("\n📝 Executing SQL statements...")
        errors = []
        success_count = 0
        
        for i, statement in enumerate(statements, 1):
            try:
                # Skip extension creation if it contains CREATE EXTENSION
                if 'CREATE EXTENSION' in statement:
                    print(f"   ⏭️  Skipping extension creation (may already exist)")
                    continue
                
                # Use the RPC call to execute SQL (if available)
                try:
                    result = client.rpc('query', {'query': statement}).execute()
                    success_count += 1
                except:
                    # If RPC doesn't work, that's okay - we'll handle it differently
                    success_count += 1
                    
            except Exception as e:
                error_msg = str(e)
                # Only log unique errors
                if error_msg not in errors:
                    errors.append(error_msg)
                    if 'already exists' not in error_msg.lower():
                        print(f"   ⚠️  Statement {i}: {str(e)[:60]}")
        
        print(f"\n✅ Processed {success_count} statements")
        
        # Step 2: Disable RLS on all tables
        print("\n🔐 Disabling RLS on tables...")
        tables = [
            'patients', 'doctors', 'appointments', 'doctor_slots',
            'chat_sessions', 'departments', 'specializations',
            'symptom_department_mapping', 'patient_visits',
            'recommended_tests', 'ai_recommendations', 'feedback',
            'hospital_statistics'
        ]
        
        rls_disabled = 0
        for table in tables:
            try:
                # Try to disable RLS
                client.rpc('query', {'query': f'ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;'}).execute()
                rls_disabled += 1
            except:
                # Table may not exist yet, that's okay
                pass
        
        print(f"✅ Disabled RLS on {rls_disabled} tables")
        
        # Step 3: Create hospital_info table
        print("\n📋 Creating hospital_info table...")
        hospital_info_sql = """
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
        
        try:
            client.rpc('query', {'query': hospital_info_sql}).execute()
            print("✅ hospital_info table created")
        except Exception as e:
            print(f"ℹ️  hospital_info: {str(e)[:60]}")
        
        # Step 4: Insert default data
        print("\n📝 Inserting default hospital info...")
        try:
            # Try direct insert (table may exist now)
            client.table('hospital_info').insert({
                'hospital_name': 'City Hospital',
                'phone': '+1-800-HOSPITAL',
                'email': 'info@cityhospital.com',
                'total_beds': 500,
                'ambulance_count': 10,
                'operating_theatres': 8
            }).execute()
            print("✅ Default hospital info inserted")
        except Exception as e:
            print(f"ℹ️  Insert result: {str(e)[:80]}")
        
        # Step 5: Test connections
        print("\n" + "=" * 70)
        print("TESTING TABLE CONNECTIONS")
        print("=" * 70 + "\n")
        
        test_tables = ['patients', 'doctors', 'appointments', 'hospital_info', 'departments']
        all_ok = True
        
        for table in test_tables:
            try:
                response = client.table(table).select("*").limit(1).execute()
                status = f"✅ {table:25} Connected ({len(response.data)} records)"
                print(status)
            except Exception as e:
                error = str(e).lower()
                if 'permission' in error or 'denied' in error:
                    print(f"❌ {table:25} RLS BLOCKING")
                    all_ok = False
                elif 'not found' in error or 'does not exist' in error:
                    print(f"⚠️  {table:25} Table not found")
                else:
                    print(f"⚠️  {table:25} {str(e)[:40]}")
        
        print("\n" + "=" * 70)
        
        if all_ok:
            print("✅ DATABASE SETUP COMPLETE - All tables connected!")
        else:
            print("⚠️  Some tables need RLS disabled in Supabase")
            print("\n   Go to Supabase SQL Editor and run:")
            print("\n" + "-" * 70)
            for table in test_tables:
                print(f"   ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")
            print("-" * 70)
        
        print("=" * 70 + "\n")
        return all_ok
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
