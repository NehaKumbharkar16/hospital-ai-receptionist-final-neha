from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_supabase_admin
from models.hospital import (
    AppointmentCreate, AppointmentUpdate, Appointment, AppointmentStatus,
    DepartmentCreate, Department, SpecializationCreate, Specialization
)
from datetime import datetime, date
import uuid

# ============ Appointments Router ============
appointments_router = APIRouter(prefix="/appointments", tags=["Appointments"])

@appointments_router.post("/", response_model=Appointment)
async def create_appointment(appointment: AppointmentCreate):
    """Book a new appointment"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Generate appointment number
        appointment_number = f"APT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        data = {
            "appointment_number": appointment_number,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "department_id": appointment.department_id,
            "appointment_date": appointment.appointment_date.isoformat(),
            "reason_for_visit": appointment.reason_for_visit,
            "priority": appointment.priority.value if appointment.priority else "normal",
            "status": "scheduled"
        }
        
        result = supabase.table("appointments").insert(data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to create appointment")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@appointments_router.get("/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    """Get appointment details"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("appointments").select("*").eq("id", appointment_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Appointment not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@appointments_router.put("/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, appointment: AppointmentUpdate):
    """Update appointment (reschedule, cancel, etc.)"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        data = {}
        for field, value in appointment.model_dump().items():
            if value is not None:
                if hasattr(value, 'value'):
                    data[field] = value.value
                else:
                    data[field] = value
        
        data["updated_at"] = "now()"
        
        result = supabase.table("appointments").update(data).eq("id", appointment_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to update appointment")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@appointments_router.get("/patient/{patient_id}", response_model=List[Appointment])
async def get_patient_appointments(patient_id: str):
    """Get all appointments for a patient"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("appointments").select("*").eq("patient_id", patient_id).order("appointment_date", desc=True).execute()
        return result.data if result.data else []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@appointments_router.delete("/{appointment_id}")
async def cancel_appointment(appointment_id: str):
    """Cancel an appointment"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("appointments").update({"status": "cancelled"}).eq("id", appointment_id).execute()
        if result.data:
            return {"message": "Appointment cancelled successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to cancel appointment")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ Departments Router ============
departments_router = APIRouter(prefix="/departments", tags=["Departments"])

@departments_router.post("/", response_model=Department)
async def create_department(department: DepartmentCreate):
    """Create a new department"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        data = {
            "name": department.name,
            "description": department.description
        }
        
        result = supabase.table("departments").insert(data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to create department")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@departments_router.get("/", response_model=List[Department])
async def list_departments():
    """List all departments"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("departments").select("*").execute()
        return result.data if result.data else []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@departments_router.get("/{department_id}", response_model=Department)
async def get_department(department_id: str):
    """Get department details"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("departments").select("*").eq("id", department_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Department not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
