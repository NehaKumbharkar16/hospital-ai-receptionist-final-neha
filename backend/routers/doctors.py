from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_supabase_admin
from models.hospital import (
    DoctorCreate, DoctorUpdate, Doctor, DoctorSlotCreate, DoctorSlot
)
from datetime import date, datetime

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("/", response_model=Doctor)
async def create_doctor(doctor: DoctorCreate):
    """Add a new doctor"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Check if doctor already exists
        existing = supabase.table("doctors").select("*").eq("email", doctor.email).execute()
        if existing.data and len(existing.data) > 0:
            raise HTTPException(status_code=400, detail="Doctor with this email already exists")
        
        data = {
            "name": doctor.name,
            "email": doctor.email,
            "phone": doctor.phone,
            "specialization_id": doctor.specialization_id,
            "department_id": doctor.department_id,
            "qualification": doctor.qualification,
            "experience_years": doctor.experience_years,
            "opd_start_time": doctor.opd_start_time.isoformat() if doctor.opd_start_time else None,
            "opd_end_time": doctor.opd_end_time.isoformat() if doctor.opd_end_time else None,
            "consultation_fee": doctor.consultation_fee,
            "available_days": doctor.available_days,
            "is_on_leave": False
        }
        
        result = supabase.table("doctors").insert(data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to create doctor")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: str):
    """Get doctor details"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("doctors").select("*").eq("id", doctor_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Doctor not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{doctor_id}", response_model=Doctor)
async def update_doctor(doctor_id: str, doctor: DoctorUpdate):
    """Update doctor profile"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        data = {}
        for field, value in doctor.model_dump().items():
            if value is not None:
                if hasattr(value, 'isoformat'):
                    data[field] = value.isoformat()
                else:
                    data[field] = value
        
        data["updated_at"] = "now()"
        
        result = supabase.table("doctors").update(data).eq("id", doctor_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to update doctor")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Doctor])
async def list_doctors(department_id: Optional[str] = None, skip: int = Query(0), limit: int = Query(10)):
    """List all doctors, optionally filtered by department"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        query = supabase.table("doctors").select("*")
        
        if department_id:
            query = query.eq("department_id", department_id)
        
        result = query.range(skip, skip + limit - 1).execute()
        print(f"DEBUG list_doctors: total_doctors={len(result.data) if result.data else 0}, doctors={result.data}")
        return result.data if result.data else []
        
    except Exception as e:
        print(f"ERROR in list_doctors: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{doctor_id}/slots", response_model=DoctorSlot)
async def create_doctor_slot(doctor_id: str, slot: DoctorSlotCreate):
    """Create available time slots for a doctor"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        data = {
            "doctor_id": doctor_id,
            "slot_date": slot.slot_date.isoformat(),
            "start_time": slot.start_time.isoformat(),
            "end_time": slot.end_time.isoformat(),
            "capacity": slot.capacity,
            "booked": 0,
            "is_available": True
        }
        
        result = supabase.table("doctor_slots").insert(data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to create slot")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{doctor_id}/slots", response_model=List[DoctorSlot])
async def get_doctor_slots(doctor_id: str, slot_date: Optional[date] = None):
    """Get available slots for a doctor"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        query = supabase.table("doctor_slots").select("*").eq("doctor_id", doctor_id).eq("is_available", True)
        
        if slot_date:
            query = query.eq("slot_date", slot_date.isoformat())
        
        result = query.execute()
        return result.data if result.data else []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
