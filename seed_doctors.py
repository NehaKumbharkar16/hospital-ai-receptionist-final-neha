#!/usr/bin/env python3
"""Script to add sample doctors to the database"""

import os
import sys

# Load from backend .env directly
backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
if os.path.exists(backend_env):
    with open(backend_env, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"\'')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from supabase import create_client
import uuid

# Initialize Supabase client
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not url or not key:
    print("❌ Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
    print(f"URL: {url}")
    print(f"KEY: {'SET' if key else 'NOT SET'}")
    sys.exit(1)

supabase = create_client(url, key)

# First, let's get or create departments
departments = [
    {'name': 'General Medicine', 'description': 'General medical care'},
    {'name': 'Cardiology', 'description': 'Heart and cardiovascular diseases'},
    {'name': 'Pediatrics', 'description': 'Child health and development'},
]

print("📌 Creating/Getting departments...")
dept_ids = {}
for dept in departments:
    try:
        result = supabase.table('departments').select('id').eq('name', dept['name']).execute()
        if result.data and len(result.data) > 0:
            dept_ids[dept['name']] = result.data[0]['id']
            print(f"  ✓ Found department: {dept['name']}")
        else:
            # Create department
            new_dept = supabase.table('departments').insert({
                'name': dept['name'],
                'description': dept['description']
            }).execute()
            if new_dept.data:
                dept_ids[dept['name']] = new_dept.data[0]['id']
                print(f"  ✓ Created department: {dept['name']}")
    except Exception as e:
        print(f"  ✗ Error with {dept['name']}: {e}")

# Sample doctors to add
sample_doctors = [
    {
        'name': 'Dr. Rajesh Kumar',
        'email': 'rajesh.kumar@hospital.com',
        'phone': '9876543210',
        'department': 'General Medicine',
        'qualification': 'MBBS, MD',
        'experience_years': 15,
        'consultation_fee': 500,
    },
    {
        'name': 'Dr. Priya Sharma',
        'email': 'priya.sharma@hospital.com',
        'phone': '9876543211',
        'department': 'Cardiology',
        'qualification': 'MBBS, DM (Cardiology)',
        'experience_years': 12,
        'consultation_fee': 800,
    },
    {
        'name': 'Dr. Amit Patel',
        'email': 'amit.patel@hospital.com',
        'phone': '9876543212',
        'department': 'Pediatrics',
        'qualification': 'MBBS, MD (Pediatrics)',
        'experience_years': 10,
        'consultation_fee': 600,
    },
    {
        'name': 'Dr. Neha Verma',
        'email': 'neha.verma@hospital.com',
        'phone': '9876543213',
        'department': 'General Medicine',
        'qualification': 'MBBS, MD',
        'experience_years': 8,
        'consultation_fee': 450,
    },
    {
        'name': 'Dr. Sandeep Singh',
        'email': 'sandeep.singh@hospital.com',
        'phone': '9876543214',
        'department': 'Cardiology',
        'qualification': 'MBBS, DM (Cardiology)',
        'experience_years': 18,
        'consultation_fee': 1000,
    },
]

print("\n🏥 Adding doctors...")
added_count = 0
for doctor in sample_doctors:
    try:
        # Check if doctor already exists
        existing = supabase.table('doctors').select('id').eq('email', doctor['email']).execute()
        if existing.data and len(existing.data) > 0:
            print(f"  ℹ Doctor already exists: {doctor['name']}")
            continue
        
        dept_id = dept_ids.get(doctor['department'])
        if not dept_id:
            print(f"  ✗ Department not found: {doctor['department']}")
            continue
        
        # Insert doctor with minimal required fields
        data = {
            'name': doctor['name'],
            'email': doctor['email'],
            'phone': doctor['phone'],
            'department_id': dept_id,
        }
        
        # Add optional fields if they exist
        if doctor.get('qualification'):
            data['qualification'] = doctor['qualification']
        if doctor.get('experience_years'):
            data['experience_years'] = doctor['experience_years']
        
        result = supabase.table('doctors').insert(data).execute()
        
        if result.data:
            print(f"  ✓ Added: {doctor['name']}")
            added_count += 1
        else:
            print(f"  ✗ Failed to add: {doctor['name']}")
    except Exception as e:
        print(f"  ✗ Error adding {doctor['name']}: {e}")

print(f"\n✅ Process complete! Added {added_count} doctors.")

# Verify
try:
    verify = supabase.table('doctors').select('name, email, department_id').execute()
    print(f"\n📊 Total doctors in database: {len(verify.data)}")
    for doc in verify.data:
        print(f"  - {doc['name']} ({doc['email']})")
except Exception as e:
    print(f"Error verifying: {e}")
