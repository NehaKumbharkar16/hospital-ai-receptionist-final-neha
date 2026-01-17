#!/usr/bin/env python3
"""
Execute Database Schema on Supabase
Uses postgres connection to execute DDL commands
"""

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")

def extract_connection_params(supabase_url):
    """Extract database connection parameters from Supabase URL"""
    # Supabase URLs are typically: https://xxxx.supabase.co
    # The DB host is: xxxx.supabase.co
    if supabase_url:
        host = supabase_url.replace("https://", "").replace("http://", "").rstrip("/")
        return {
            "host": host,
            "port": "5432",
            "database": "postgres",
            "user": "postgres"
        }
    return None

def apply_schema_via_sql_file():
    """Apply schema by reading SQL and executing it"""
    
    if not SUPABASE_URL:
        print("[ERROR] SUPABASE_URL not found in backend/.env")
        return False
    
    schema_path = Path("backend/database/schema.sql")
    if not schema_path.exists():
        print(f"[ERROR] Schema file not found: {schema_path}")
        return False
    
    print("="*70)
    print("TO APPLY THE DATABASE SCHEMA TO SUPABASE:")
    print("="*70)
    print()
    print("OPTION 1: Using Supabase Dashboard (Recommended & Easiest)")
    print("-" * 70)
    print("1. Go to: https://app.supabase.com/")
    print("2. Login and select your project")
    print("3. Click 'SQL Editor' in the left sidebar")
    print("4. Click 'New Query' button")
    print("5. Copy ALL the content below (everything between the dashes):")
    print()
    print("-" * 70)
    print("COPY FROM HERE:")
    print("-" * 70)
    
    with open(schema_path, 'r') as f:
        schema_content = f.read()
    
    print(schema_content)
    
    print()
    print("-" * 70)
    print("COPY UNTIL HERE")
    print("-" * 70)
    print()
    print("6. Paste the SQL in the SQL Editor")
    print("7. Click 'RUN' button")
    print("8. Wait for it to complete (should take a few seconds)")
    print()
    print("OPTION 2: Using Command Line (If you have psql installed)")
    print("-" * 70)
    print(f"psql postgresql://postgres:<PASSWORD>@{SUPABASE_URL.replace('https://', '')}/postgres < backend/database/schema.sql")
    print()
    print("="*70)
    
    return True

def main():
    print("\n🏥 Hospital Management System - Database Schema Setup\n")
    
    if not SUPABASE_URL:
        print("[ERROR] SUPABASE_URL not configured in backend/.env")
        print("Please set up your Supabase credentials first.")
        return
    
    print(f"[INFO] Supabase URL: {SUPABASE_URL}")
    print()
    
    apply_schema_via_sql_file()
    
    print("\n📋 After applying the schema:")
    print("-" * 70)
    print("1. Re-run 'python setup_database.py' to verify tables were created")
    print("2. You can then start the backend server")
    print("3. Patient registration will work properly once schema is applied")
    print()

if __name__ == "__main__":
    main()
