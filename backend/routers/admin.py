from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_supabase_admin
from models.hospital import (
    HospitalStatistics, Feedback, FeedbackCreate,
    SuccessResponse, ErrorResponse
)
from datetime import date, datetime, timedelta

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/statistics", response_model=HospitalStatistics)
async def get_hospital_statistics(target_date: Optional[date] = None):
    """Get hospital statistics for a specific date"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        if target_date is None:
            target_date = date.today()
        
        # Get or create statistics record
        result = supabase.table("hospital_statistics").select("*").eq("statistic_date", target_date.isoformat()).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        
        # Calculate statistics from other tables
        today_str = target_date.isoformat()
        
        # Count patients registered today
        patients_result = supabase.table("patients").select("*", count="exact").gte("registration_date", f"{today_str}T00:00:00").lte("registration_date", f"{today_str}T23:59:59").execute()
        total_patients_today = patients_result.count if hasattr(patients_result, 'count') else 0
        
        # Count appointments today
        appointments_result = supabase.table("appointments").select("*", count="exact").gte("appointment_date", f"{today_str}T00:00:00").lte("appointment_date", f"{today_str}T23:59:59").execute()
        total_appointments_today = appointments_result.count if hasattr(appointments_result, 'count') else 0
        
        # Count emergency cases
        emergency_result = supabase.table("appointments").select("*", count="exact").eq("priority", "emergency").execute()
        emergency_cases = emergency_result.count if hasattr(emergency_result, 'count') else 0
        
        # Create and store statistics
        stats_data = {
            "statistic_date": today_str,
            "total_patients_today": total_patients_today,
            "total_appointments_today": total_appointments_today,
            "emergency_cases": emergency_cases,
            "completed_visits": 0,
            "available_doctors": 0,
            "occupied_rooms": 0
        }
        
        insert_result = supabase.table("hospital_statistics").insert(stats_data).execute()
        if insert_result.data and len(insert_result.data) > 0:
            return insert_result.data[0]
        
        return HospitalStatistics(**stats_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/overview")
async def get_dashboard_overview():
    """Get overall dashboard data"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        today = date.today()
        
        # Get today's statistics
        stats_result = supabase.table("hospital_statistics").select("*").eq("statistic_date", today.isoformat()).execute()
        stats = stats_result.data[0] if stats_result.data else {}
        
        # Get pending appointments
        pending_appointments = supabase.table("appointments").select("*").eq("status", "scheduled").execute()
        
        # Get recent patients
        recent_patients = supabase.table("patients").select("*").order("registration_date", desc=True).limit(10).execute()
        
        # Get doctors on duty
        doctors_result = supabase.table("doctors").select("*").eq("is_on_leave", False).execute()
        available_doctors_count = len(doctors_result.data) if doctors_result.data else 0
        
        return {
            "statistics": stats,
            "pending_appointments": len(pending_appointments.data) if pending_appointments.data else 0,
            "recent_patients": recent_patients.data if recent_patients.data else [],
            "available_doctors": available_doctors_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emergency-cases")
async def get_emergency_cases(days: int = Query(1)):
    """Get emergency cases from last N days"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        since_date = (date.today() - timedelta(days=days)).isoformat()
        
        result = supabase.table("appointments").select("*").eq("priority", "emergency").gte("appointment_date", since_date).execute()
        
        return {
            "total": len(result.data) if result.data else 0,
            "cases": result.data if result.data else []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patients/total")
async def get_total_patients():
    """Get total patient count"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("patients").select("*", count="exact").execute()
        return {"total_patients": result.count if hasattr(result, 'count') else 0}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/doctors/available")
async def get_available_doctors():
    """Get list of available doctors"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("doctors").select("*").eq("is_on_leave", False).execute()
        return {"total": len(result.data) if result.data else 0, "doctors": result.data if result.data else []}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ Feedback Router ============
feedback_router = APIRouter(prefix="/feedback", tags=["Feedback"])

@feedback_router.post("/", response_model=Feedback)
async def submit_feedback(feedback: FeedbackCreate):
    """Submit patient feedback"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Validate rating
        if feedback.rating < 1 or feedback.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        data = {
            "patient_id": feedback.patient_id,
            "visit_id": feedback.visit_id,
            "doctor_id": feedback.doctor_id,
            "appointment_id": feedback.appointment_id,
            "rating": feedback.rating,
            "feedback_text": feedback.feedback_text,
            "categories": feedback.categories,
            "suggestions": feedback.suggestions,
            "is_anonymous": feedback.is_anonymous
        }
        
        result = supabase.table("feedback").insert(data).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to submit feedback")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@feedback_router.get("/doctor/{doctor_id}")
async def get_doctor_feedback(doctor_id: str):
    """Get feedback for a doctor"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("feedback").select("*").eq("doctor_id", doctor_id).execute()
        
        feedbacks = result.data if result.data else []
        
        if feedbacks:
            avg_rating = sum(f['rating'] for f in feedbacks) / len(feedbacks)
        else:
            avg_rating = 0
        
        return {
            "total_feedbacks": len(feedbacks),
            "average_rating": round(avg_rating, 2),
            "feedbacks": feedbacks
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@feedback_router.get("/patient/{patient_id}")
async def get_patient_feedback(patient_id: str):
    """Get feedback submitted by a patient"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("feedback").select("*").eq("patient_id", patient_id).execute()
        return result.data if result.data else []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@feedback_router.get("/summary")
async def get_feedback_summary():
    """Get overall feedback summary"""
    try:
        supabase = get_supabase_admin()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        result = supabase.table("feedback").select("*").execute()
        
        feedbacks = result.data if result.data else []
        
        if feedbacks:
            avg_rating = sum(f['rating'] for f in feedbacks) / len(feedbacks)
            rating_distribution = {
                "5_stars": len([f for f in feedbacks if f['rating'] == 5]),
                "4_stars": len([f for f in feedbacks if f['rating'] == 4]),
                "3_stars": len([f for f in feedbacks if f['rating'] == 3]),
                "2_stars": len([f for f in feedbacks if f['rating'] == 2]),
                "1_stars": len([f for f in feedbacks if f['rating'] == 1])
            }
        else:
            avg_rating = 0
            rating_distribution = {"5_stars": 0, "4_stars": 0, "3_stars": 0, "2_stars": 0, "1_stars": 0}
        
        return {
            "total_feedbacks": len(feedbacks),
            "average_rating": round(avg_rating, 2),
            "rating_distribution": rating_distribution
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
