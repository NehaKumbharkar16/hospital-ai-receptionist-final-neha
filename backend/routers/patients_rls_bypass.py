"""
Alternative patients router with RLS bypass using PostgREST client directly
"""
from fastapi import APIRouter, HTTPException
from typing import List
from database import get_supabase_admin
from models.hospital import (
    PatientCreate, PatientUpdate, Patient, PatientLookup,
    SuccessResponse, ErrorResponse
)
import uuid
from supabase import create_client
import os

router = APIRouter(prefix="/patients", tags=["Patients"])

# Direct Supabase API client for RLS bypass
def get_admin_client():
    """Get admin client with service role key"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

@router.post("/register", response_model=Patient)
async def register_patient(patient: PatientCreate):
    """Register a new patient - with RLS bypass"""
    try:
        supabase = get_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Check if patient already exists
        try:
            existing = supabase.table("patients").select("*").eq("email", patient.email).execute()
            if existing.data and len(existing.data) > 0:
                raise HTTPException(status_code=400, detail="Patient with this email already exists")
        except Exception as check_error:
            print(f"[DEBUG] Check existing error: {check_error}")
            # Continue anyway - might be RLS error on read
        
        data = {
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email,
            "phone": patient.phone,
            "age": patient.age,
            "gender": patient.gender.value if patient.gender else None,
            "blood_group": patient.blood_group,
            "address": patient.address,
            "emergency_contact_name": patient.emergency_contact_name,
            "emergency_contact_phone": patient.emergency_contact_phone,
            "medical_history": patient.medical_history,
            "allergies": patient.allergies,
            "has_emergency_flag": patient.has_emergency_flag or False,
            "emergency_description": patient.emergency_description,
            "preferred_department_id": patient.preferred_department_id,
            "registration_date": "now()"
        }
        
        # Try with explicit PostgREST headers
        headers = {
            "Authorization": f"Bearer {os.getenv('SUPABASE_SERVICE_ROLE_KEY')}"
        }
        
        try:
            # Attempt direct insert
            result = supabase.table("patients").insert(data).execute()
            if result.data and len(result.data) > 0:
                print(f"[SUCCESS] Patient registered: {result.data[0].get('patient_id', 'unknown')}")
                return result.data[0]
        except Exception as first_attempt:
            print(f"[INFO] First insert attempt failed: {first_attempt}")
            error_msg = str(first_attempt).lower()
            
            # If RLS error, try alternative approaches
            if "permission denied" in error_msg or "42501" in str(first_attempt):
                print(f"[INFO] RLS permission error detected - trying with explicit count parameter")
                try:
                    # Try with count parameter
                    result = supabase.table("patients").insert(data, count='exact').execute()
                    if result.data and len(result.data) > 0:
                        print(f"[SUCCESS] Patient registered with count param: {result.data[0].get('patient_id', 'unknown')}")
                        return result.data[0]
                except Exception as second_attempt:
                    print(f"[INFO] Second attempt also failed: {second_attempt}")
                    print(f"[ERROR] All insert attempts failed with RLS error")
                    raise HTTPException(status_code=500, detail=f"Database write failed: permission denied. RLS might still be enabled.")
            
            raise
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in register_patient: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lookup", response_model=List[Patient])
async def lookup_patient(lookup: PatientLookup):
    """Look up existing patient by email, phone, or patient ID"""
    try:
        supabase = get_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        query = supabase.table("patients").select("*")
        
        if lookup.email:
            query = query.eq("email", lookup.email)
        elif lookup.phone:
            query = query.eq("phone", lookup.phone)
        elif lookup.patient_id:
            query = query.eq("patient_id", lookup.patient_id)
        else:
            raise HTTPException(status_code=400, detail="Provide email, phone, or patient_id for lookup")
        
        result = query.execute()
        return result.data if result.data else []
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in lookup_patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Get patient by ID"""
    try:
        supabase = get_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("patients").select("*").eq("patient_id", patient_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Patient not found")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in get_patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, patient: PatientUpdate):
    """Update patient information"""
    try:
        supabase = get_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Build update data (only include non-None fields)
        data = {}
        if patient.first_name:
            data["first_name"] = patient.first_name
        if patient.last_name:
            data["last_name"] = patient.last_name
        if patient.phone:
            data["phone"] = patient.phone
        if patient.age:
            data["age"] = patient.age
        if patient.gender:
            data["gender"] = patient.gender.value
        if patient.blood_group:
            data["blood_group"] = patient.blood_group
        if patient.address:
            data["address"] = patient.address
        if patient.medical_history:
            data["medical_history"] = patient.medical_history
        if patient.allergies:
            data["allergies"] = patient.allergies
        if patient.has_emergency_flag is not None:
            data["has_emergency_flag"] = patient.has_emergency_flag
        if patient.emergency_description:
            data["emergency_description"] = patient.emergency_description
        
        result = supabase.table("patients").update(data).eq("patient_id", patient_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Patient not found or update failed")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in update_patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))
