#!/usr/bin/env python3
import sys
import os
import asyncio

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from database import init_db, get_supabase_admin

async def test_database_connection():
    """Test if database tables are connected"""
    try:
        # Initialize database
        await init_db()
        
        supabase = get_supabase_admin()
        
        if not supabase:
            print("❌ ERROR: Supabase connection failed")
            return False
        
        print("\n✅ Supabase Connected\n")
        print("=" * 50)
        print("Testing Database Tables")
        print("=" * 50)
        
        # Test tables
        tables_to_test = ['patients', 'doctors', 'appointments', 'hospital_info']
        
        for table in tables_to_test:
            try:
                response = supabase.table(table).select("*").limit(1).execute()
                print(f"✅ {table:20} - Connected (Found {len(response.data)} records)")
            except Exception as e:
                print(f"❌ {table:20} - Error: {str(e)[:50]}")
        
        print("\n" + "=" * 50)
        print("Database connection check complete!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_database_connection())
    sys.exit(0 if success else 1)
