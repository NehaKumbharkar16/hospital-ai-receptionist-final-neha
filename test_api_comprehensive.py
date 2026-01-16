#!/usr/bin/env python3
"""
Comprehensive API Testing for Hospital Management System
Tests all endpoints to ensure they work correctly
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"
PATIENT_ID = None
APPOINTMENT_ID = None
DOCTOR_ID = None

class TestColors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test(name, passed):
    status = f"{TestColors.GREEN}✓ PASS{TestColors.END}" if passed else f"{TestColors.RED}✗ FAIL{TestColors.END}"
    print(f"{status} - {name}")

def print_header(header):
    print(f"\n{TestColors.BLUE}{TestColors.BOLD}{header}{TestColors.END}")
    print("=" * 50)

def test_patient_registration():
    print_header("Testing Patient Registration")
    
    global PATIENT_ID
    
    # Test 1: Register new patient
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"john_{datetime.now().timestamp()}@example.com",
        "phone": "9876543210",
        "age": 35,
        "gender": "male",
        "blood_group": "O+",
        "address": "123 Main Street"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/patients/register", json=patient_data)
        if response.status_code == 200:
            result = response.json()
            PATIENT_ID = result.get("id") or result.get("patient_id")
            print_test("Register patient", True)
            print(f"  → Patient ID: {PATIENT_ID}")
            return True
        else:
            print_test("Register patient", False)
            print(f"  → Error: {response.text}")
            return False
    except Exception as e:
        print_test("Register patient", False)
        print(f"  → Error: {str(e)}")
        return False

def test_patient_lookup():
    print_header("Testing Patient Lookup")
    
    if not PATIENT_ID:
        print_test("Lookup patient by ID", False)
        print("  → No patient ID available")
        return False
    
    try:
        response = requests.post(
            f"{BASE_URL}/patients/lookup",
            json={"patient_id": PATIENT_ID}
        )
        if response.status_code == 200:
            print_test("Lookup patient by ID", True)
            patient = response.json()
            print(f"  → Found: {patient.get('first_name')} {patient.get('last_name')}")
            return True
        else:
            print_test("Lookup patient by ID", False)
            return False
    except Exception as e:
        print_test("Lookup patient by ID", False)
        print(f"  → Error: {str(e)}")
        return False

def test_doctors():
    print_header("Testing Doctor Management")
    
    global DOCTOR_ID
    
    # Test 1: Get all doctors
    try:
        response = requests.get(f"{BASE_URL}/doctors")
        if response.status_code == 200:
            doctors = response.json()
            print_test("Get all doctors", True)
            print(f"  → Found {len(doctors)} doctors")
            if doctors:
                DOCTOR_ID = doctors[0].get("id")
                print(f"  → Using doctor ID: {DOCTOR_ID}")
            return True
        else:
            print_test("Get all doctors", False)
            return False
    except Exception as e:
        print_test("Get all doctors", False)
        print(f"  → Error: {str(e)}")
        return False

def test_appointments():
    print_header("Testing Appointment Management")
    
    global APPOINTMENT_ID
    
    if not PATIENT_ID or not DOCTOR_ID:
        print_test("Create appointment", False)
        print("  → Missing patient or doctor ID")
        return False
    
    # Test 1: Create appointment
    appointment_data = {
        "patient_id": PATIENT_ID,
        "doctor_id": DOCTOR_ID,
        "appointment_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "reason_for_visit": "Regular checkup",
        "priority": "normal"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/appointments", json=appointment_data)
        if response.status_code == 200:
            result = response.json()
            APPOINTMENT_ID = result.get("id") or result.get("appointment_id")
            print_test("Create appointment", True)
            print(f"  → Appointment ID: {APPOINTMENT_ID}")
        else:
            print_test("Create appointment", False)
            print(f"  → Error: {response.text}")
    except Exception as e:
        print_test("Create appointment", False)
        print(f"  → Error: {str(e)}")
    
    # Test 2: Get patient appointments
    try:
        response = requests.get(f"{BASE_URL}/appointments/patient/{PATIENT_ID}")
        if response.status_code == 200:
            appointments = response.json()
            print_test("Get patient appointments", True)
            print(f"  → Found {len(appointments)} appointments")
            return True
        else:
            print_test("Get patient appointments", False)
            return False
    except Exception as e:
        print_test("Get patient appointments", False)
        print(f"  → Error: {str(e)}")
        return False

def test_admin_dashboard():
    print_header("Testing Admin Dashboard")
    
    # Test 1: Get statistics
    try:
        response = requests.get(f"{BASE_URL}/admin/statistics")
        if response.status_code == 200:
            print_test("Get statistics", True)
            stats = response.json()
            print(f"  → Total patients today: {stats.get('total_patients_today', 0)}")
            print(f"  → Total appointments: {stats.get('total_appointments_today', 0)}")
            print(f"  → Emergency cases: {stats.get('emergency_cases', 0)}")
        else:
            print_test("Get statistics", False)
    except Exception as e:
        print_test("Get statistics", False)
        print(f"  → Error: {str(e)}")
    
    # Test 2: Get dashboard overview
    try:
        response = requests.get(f"{BASE_URL}/admin/dashboard/overview")
        if response.status_code == 200:
            print_test("Get dashboard overview", True)
            overview = response.json()
            print(f"  → Pending appointments: {overview.get('pending_appointments', 0)}")
            print(f"  → Available doctors: {overview.get('available_doctors', 0)}")
            return True
        else:
            print_test("Get dashboard overview", False)
            return False
    except Exception as e:
        print_test("Get dashboard overview", False)
        print(f"  → Error: {str(e)}")
        return False

def test_emergency_cases():
    print_header("Testing Emergency Cases")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/emergency-cases?days=7")
        if response.status_code == 200:
            data = response.json()
            cases = data.get("cases", [])
            print_test("Get emergency cases", True)
            print(f"  → Found {len(cases)} emergency cases in last 7 days")
            return True
        else:
            print_test("Get emergency cases", False)
            return False
    except Exception as e:
        print_test("Get emergency cases", False)
        print(f"  → Error: {str(e)}")
        return False

def test_chat():
    print_header("Testing AI Receptionist Chat")
    
    try:
        chat_data = {
            "user_input": "I have a headache and fever",
            "patient_data": {
                "first_name": "Test",
                "last_name": "User",
                "age": 30
            }
        }
        
        response = requests.post(f"{BASE_URL}/chat", json=chat_data)
        if response.status_code == 200:
            result = response.json()
            print_test("Chat endpoint", True)
            print(f"  → AI Response: {result.get('response', 'No response')[:100]}...")
            ward = result.get('ward')
            if ward:
                print(f"  → Recommended Ward: {ward}")
            return True
        else:
            print_test("Chat endpoint", False)
            print(f"  → Error: {response.text}")
            return False
    except Exception as e:
        print_test("Chat endpoint", False)
        print(f"  → Error: {str(e)}")
        return False

def test_feedback():
    print_header("Testing Feedback System")
    
    if not APPOINTMENT_ID:
        print_test("Submit feedback", False)
        print("  → No appointment ID available")
        return False
    
    feedback_data = {
        "appointment_id": APPOINTMENT_ID,
        "rating": 5,
        "feedback_text": "Great service and professional staff"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/feedback", json=feedback_data)
        if response.status_code == 200:
            print_test("Submit feedback", True)
            return True
        else:
            print_test("Submit feedback", False)
            return False
    except Exception as e:
        print_test("Submit feedback", False)
        print(f"  → Error: {str(e)}")
        return False

def test_departments():
    print_header("Testing Departments")
    
    try:
        response = requests.get(f"{BASE_URL}/departments")
        if response.status_code == 200:
            departments = response.json()
            print_test("Get departments", True)
            print(f"  → Found {len(departments)} departments")
            for dept in departments[:3]:
                print(f"    - {dept.get('name', 'Unknown')}")
            return True
        else:
            print_test("Get departments", False)
            return False
    except Exception as e:
        print_test("Get departments", False)
        print(f"  → Error: {str(e)}")
        return False

def run_all_tests():
    print(f"\n{TestColors.BOLD}{TestColors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     HOSPITAL MANAGEMENT SYSTEM - API TEST SUITE           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(TestColors.END)
    
    print(f"\n{TestColors.YELLOW}Testing endpoint: {BASE_URL}{TestColors.END}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run all tests
    test_patient_registration()
    test_patient_lookup()
    test_doctors()
    test_appointments()
    test_departments()
    test_admin_dashboard()
    test_emergency_cases()
    test_chat()
    test_feedback()
    
    # Summary
    print_header("Test Summary")
    print(f"{TestColors.GREEN}All tests completed!{TestColors.END}")
    print(f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{TestColors.BOLD}Next Steps:{TestColors.END}")
    print("1. Check all PASS indicators above")
    print("2. If any tests FAIL, check backend logs")
    print("3. Verify Supabase database has schema applied")
    print("4. Confirm all environment variables are set")
    print("5. Test the frontend at http://localhost:5173")

if __name__ == "__main__":
    try:
        # Test backend is running
        response = requests.get(f"{BASE_URL}/patients")
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print(f"{TestColors.RED}❌ ERROR: Cannot connect to backend at {BASE_URL}{TestColors.END}")
        print(f"\nMake sure the backend is running:")
        print("  cd backend")
        print("  uvicorn main:app --reload --port 8000")
    except Exception as e:
        print(f"{TestColors.RED}❌ ERROR: {str(e)}{TestColors.END}")
