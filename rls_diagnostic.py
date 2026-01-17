#!/usr/bin/env python3
"""
Complete RLS Diagnostic Tool - Check and report on RLS state in Supabase
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
    print("❌ Missing credentials")
    exit(1)

client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

print("\n" + "="*70)
print("🔍 SUPABASE RLS DIAGNOSTIC REPORT")
print("="*70)

try:
    # Check which tables exist and their RLS status
    result = client.postgrest.rpc(
        "sql",
        {
            "query": """
            SELECT 
                schemaname,
                tablename,
                rowsecurity
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
            """
        }
    ).execute()
    
    print("\n📋 TABLE RLS STATUS:")
    print("-" * 70)
    
    if result.data:
        for table in result.data:
            rls_status = "🔓 DISABLED" if not table.get('rowsecurity') else "🔒 ENABLED"
            print(f"  {table['tablename']:30} {rls_status}")
    else:
        print("  ⚠️  Could not fetch table status")
except Exception as e:
    print(f"  ❌ Error checking RLS status: {e}")

# Try to check RLS policies
try:
    result = client.postgrest.rpc(
        "sql",
        {
            "query": """
            SELECT 
                schemaname,
                tablename,
                policyname,
                permissive,
                cmd,
                qual
            FROM pg_policies
            WHERE schemaname = 'public'
            ORDER BY tablename, policyname;
            """
        }
    ).execute()
    
    print("\n📌 RLS POLICIES:")
    print("-" * 70)
    
    if result.data and len(result.data) > 0:
        for policy in result.data:
            pol_type = "✅ PERMISSIVE" if policy.get('permissive') else "🚫 RESTRICTIVE"
            print(f"  Table: {policy['tablename']}")
            print(f"    Policy: {policy['policyname']} ({pol_type})")
            print(f"    Command: {policy['cmd']}")
            if policy.get('qual'):
                print(f"    Condition: {policy['qual'][:60]}...")
            print()
    else:
        print("  ✅ NO POLICIES FOUND - RLS EFFECTIVELY DISABLED")
        
except Exception as e:
    print(f"  ❌ Error checking policies: {e}")

# Test actual INSERT operation
print("\n🧪 TESTING DATABASE ACCESS:")
print("-" * 70)

test_data = {
    "first_name": "Test",
    "last_name": "User",
    "email": f"test_{os.urandom(4).hex()}@example.com",
    "phone": "5551234567",
    "age": 30,
    "gender": "M",
    "blood_group": "O+",
    "address": "Test Address",
    "emergency_contact_name": "Emergency Contact",
    "emergency_contact_phone": "5559876543",
    "medical_history": None,
    "allergies": None,
    "has_emergency_flag": False,
    "emergency_description": None,
    "preferred_department_id": None,
    "registration_date": "now()"
}

try:
    result = client.table("patients").insert(test_data).execute()
    if result.data and len(result.data) > 0:
        print(f"  ✅ INSERT SUCCESSFUL")
        print(f"     Patient ID: {result.data[0].get('patient_id', 'N/A')}")
        print(f"     Email: {result.data[0].get('email', 'N/A')}")
    else:
        print(f"  ⚠️  INSERT returned no data")
except Exception as e:
    error_msg = str(e).lower()
    if "permission denied" in error_msg:
        print(f"  ❌ RLS PERMISSION ERROR - RLS still active!")
        print(f"     Error: {e}")
    else:
        print(f"  ❌ INSERT FAILED")
        print(f"     Error: {e}")

print("\n" + "="*70)
print("✅ DIAGNOSTIC COMPLETE")
print("="*70 + "\n")
