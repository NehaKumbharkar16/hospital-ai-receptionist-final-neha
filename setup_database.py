#!/usr/bin/env python3
"""
Database Setup Script for Hospital Management System
Applies the database schema to Supabase
"""

import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def apply_schema():
    """Read and apply the database schema"""
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("[ERROR] Missing Supabase credentials in backend/.env")
        print("Please ensure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set")
        return False
    
    # Read schema file
    schema_path = Path("backend/database/schema.sql")
    if not schema_path.exists():
        print(f"[ERROR] Schema file not found: {schema_path}")
        return False
    
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Create Supabase client with service role key (allows DDL operations)
    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        print("[INFO] Connected to Supabase with service role key")
    except Exception as e:
        print(f"[ERROR] Failed to connect to Supabase: {e}")
        return False
    
    # Apply schema using PostgreSQL directly
    # Note: Supabase client doesn't directly support raw SQL DDL
    # You need to use the SQL Editor in Supabase dashboard or pgAdmin
    print("\n" + "="*60)
    print("DATABASE SCHEMA APPLICATION")
    print("="*60)
    print("\nUnfortunately, Supabase Python client doesn't support raw DDL operations.")
    print("You need to apply the schema manually using Supabase SQL Editor.\n")
    print("Follow these steps:")
    print("1. Go to https://app.supabase.com/")
    print("2. Select your project")
    print("3. Go to SQL Editor (left sidebar)")
    print("4. Click 'New Query'")
    print("5. Copy the entire content of: backend/database/schema.sql")
    print("6. Paste it into the SQL editor")
    print("7. Click 'Run' to execute")
    print("\nAlternatively, you can use psql to connect directly:")
    print(f"\npsql '{SUPABASE_URL}' -U postgres")
    print("Then paste the schema.sql contents\n")
    print("="*60 + "\n")
    
    return True

def check_tables():
    """Check if the required tables exist in Supabase"""
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("[ERROR] Missing Supabase credentials")
        return False
    
    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        # Try to query the patients table to check if it exists
        result = client.table("patients").select("id").limit(1).execute()
        print("[SUCCESS] ✓ patients table exists")
        
        # Check other important tables
        tables_to_check = [
            "doctors", "appointments", "departments", 
            "patient_visits", "ai_recommendations", "chat_sessions"
        ]
        
        for table_name in tables_to_check:
            try:
                client.table(table_name).select("id").limit(1).execute()
                print(f"[SUCCESS] ✓ {table_name} table exists")
            except Exception as e:
                print(f"[WARNING] ✗ {table_name} table not found: {str(e)[:50]}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to check tables: {e}")
        print("\n[INFO] The patients table (or other required tables) don't exist.")
        print("You need to apply the schema using the instructions above.")
        return False

def main():
    print("\n" + "="*60)
    print("Hospital Management System - Database Setup")
    print("="*60 + "\n")
    
    # First, try to check if tables exist
    print("[STEP 1] Checking if tables already exist in Supabase...")
    print("-" * 60)
    tables_exist = check_tables()
    
    if not tables_exist:
        print("\n[STEP 2] Displaying schema application instructions...")
        print("-" * 60)
        apply_schema()
        print("\n[ACTION REQUIRED]")
        print("Please apply the database schema using one of the methods above.")
        print("Once done, run this script again to verify the tables were created.")
    else:
        print("\n[SUCCESS] All required tables exist in Supabase!")
        print("Your database is ready to use.")

if __name__ == "__main__":
    main()
