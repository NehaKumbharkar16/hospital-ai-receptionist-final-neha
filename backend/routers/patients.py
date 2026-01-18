from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_supabase_admin
from models.hospital import (
    PatientCreate, PatientUpdate, Patient, PatientLookup,
    SuccessResponse, ErrorResponse
)
import uuid
import os
from supabase import create_client

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_fresh_admin_client():
    """Create a fresh admin client to avoid cached permissions"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        print("[ERROR] Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
        return None
    return create_client(url, key)

@router.post("/register", response_model=Patient)
async def register_patient(patient: PatientCreate):
    """Register a new patient"""
    try:
        # Use fresh client to avoid any caching issues
        supabase = get_fresh_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Check if patient already exists
        try:
            existing = supabase.table("patients").select("*").eq("email", patient.email).execute()
            if existing.data and len(existing.data) > 0:
                raise HTTPException(status_code=400, detail="Patient with this email already exists")
        except Exception as check_error:
            print(f"[DEBUG] Existing patient check error (continuing): {check_error}")
        
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
        
        try:
            print(f"[DEBUG] Attempting patient registration with data: {data.get('email')}")
            result = supabase.table("patients").insert(data).execute()
            if result.data and len(result.data) > 0:
                print(f"[SUCCESS] Patient registered: {result.data[0].get('patient_id', 'unknown')}")
                return result.data[0]
            else:
                raise HTTPException(status_code=500, detail="Failed to register patient")
        except Exception as db_error:
            error_str = str(db_error).lower()
            print(f"[DEBUG] Insert attempt 1 failed: {db_error}")
            if "permission denied" in error_str or "42501" in str(db_error):
                print(f"[WARNING] RLS permission error detected - trying alternative approach")
                try:
                    # Retry with count parameter
                    result = supabase.table("patients").insert(data, count='exact').execute()
                    if result.data and len(result.data) > 0:
                        print(f"[SUCCESS] Patient registered after count retry: {result.data[0].get('patient_id', 'unknown')}")
                        return result.data[0]
                except Exception as retry_error:
                    print(f"[DEBUG] Count retry also failed: {retry_error}")
            raise
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in register_patient: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lookup", response_model=List[Patient])
async def lookup_patient(email: Optional[str] = Query(None), phone: Optional[str] = Query(None), patient_id: Optional[str] = Query(None)):
    """Look up existing patient by email, phone, or patient ID"""
    try:
        supabase = get_fresh_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        query = supabase.table("patients").select("*")
        
        if email:
            query = query.eq("email", email)
        elif phone:
            query = query.eq("phone", phone)
        elif patient_id:
            query = query.eq("patient_id", patient_id)
        else:
            raise HTTPException(status_code=400, detail="Provide email, phone, or patient_id for lookup")
        
        result = query.execute()
        print(f"DEBUG lookup_patient: email={email}, phone={phone}, patient_id={patient_id}, result={result.data}")
        return result.data if result.data else []
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in lookup_patient: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/all-patients")
async def debug_all_patients():
    """Debug endpoint to see all patients in database"""
    try:
        supabase = get_fresh_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("patients").select("*").execute()
        print(f"DEBUG all_patients: total={len(result.data)}, patients={result.data}")
        return {
            "total": len(result.data),
            "patients": result.data
        }
    except Exception as e:
        print(f"ERROR in debug_all_patients: {e}")
        import traceback
        traceback.print_exc()
        return {
            "total": 0,
            "patients": [],
            "error": str(e)
        }

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Get patient details by ID"""
    try:
        supabase = get_fresh_admin_client()
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
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, patient: PatientUpdate):
    """Update patient details"""
    try:
        supabase = get_fresh_admin_client()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Check if patient exists
        existing = supabase.table("patients").select("*").eq("patient_id", patient_id).execute()
        if not existing.data or len(existing.data) == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Prepare update data (only non-None values)
        data = {}
        for field, value in patient.model_dump().items():
            if value is not None:
                if hasattr(value, 'value'):
                    data[field] = value.value
                else:
                    data[field] = value
        
        data["updated_at"] = "now()"
        
        result = supabase.table("patients").update(data).eq("patient_id", patient_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to update patient")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Patient])
async def list_patients(skip: int = Query(0), limit: int = Query(10)):
    """List all patients with pagination"""
    try:
        supabase = get_fresh_admin_client()
        return result.data if result.data else []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
