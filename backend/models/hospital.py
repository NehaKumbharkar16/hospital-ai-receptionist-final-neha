from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime, date, time

# ============ Enums ============
class Ward(str, Enum):
    GENERAL = "general"
    EMERGENCY = "emergency"
    MENTAL_HEALTH = "mental_health"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"

class VisitStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Priority(str, Enum):
    NORMAL = "normal"
    URGENT = "urgent"
    EMERGENCY = "emergency"

class ConfirmationMethod(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"

# ============ Department Models ============
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Specialization Models ============
class SpecializationBase(BaseModel):
    name: str
    department_id: str

class SpecializationCreate(SpecializationBase):
    pass

class Specialization(SpecializationBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Doctor Models ============
class DoctorBase(BaseModel):
    name: str
    email: str
    phone: str
    specialization_id: str
    department_id: str
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    opd_start_time: Optional[time] = None
    opd_end_time: Optional[time] = None
    consultation_fee: Optional[int] = None
    available_days: Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    opd_start_time: Optional[time] = None
    opd_end_time: Optional[time] = None
    consultation_fee: Optional[int] = None
    available_days: Optional[str] = None
    is_on_leave: Optional[bool] = None
    leave_start_date: Optional[date] = None
    leave_end_date: Optional[date] = None

class Doctor(DoctorBase):
    id: str
    is_on_leave: bool
    leave_start_date: Optional[date]
    leave_end_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============ Doctor Slot Models ============
class DoctorSlotBase(BaseModel):
    doctor_id: str
    slot_date: date
    start_time: time
    end_time: time
    capacity: int = 1

class DoctorSlotCreate(DoctorSlotBase):
    pass

class DoctorSlot(DoctorSlotBase):
    id: str
    booked: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Patient Models ============
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    age: int
    gender: Optional[Gender] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None

class PatientCreate(PatientBase):
    has_emergency_flag: Optional[bool] = False
    emergency_description: Optional[str] = None
    preferred_department_id: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    has_emergency_flag: Optional[bool] = None
    emergency_description: Optional[str] = None

class Patient(PatientBase):
    id: str
    patient_id: str
    has_emergency_flag: bool
    emergency_description: Optional[str] = None
    registration_date: datetime
    last_visit_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PatientLookup(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    patient_id: Optional[str] = None

# ============ Appointment Models ============
class AppointmentBase(BaseModel):
    patient_id: str
    doctor_id: str
    department_id: str
    appointment_date: datetime
    reason_for_visit: Optional[str] = None
    priority: Optional[Priority] = Priority.NORMAL

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    reason_for_visit: Optional[str] = None
    status: Optional[AppointmentStatus] = None
    room_number: Optional[str] = None
    notes: Optional[str] = None

class Appointment(AppointmentBase):
    id: str
    appointment_number: str
    status: AppointmentStatus
    room_number: Optional[str]
    confirmation_sent: bool
    confirmation_method: Optional[ConfirmationMethod]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============ Patient Visit Models ============
class PatientVisitBase(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescribed_tests: Optional[str] = None
    prescribed_medicines: Optional[str] = None
    visit_type: Optional[str] = None

class PatientVisitCreate(PatientVisitBase):
    pass

class PatientVisit(PatientVisitBase):
    id: str
    visit_date: datetime
    status: VisitStatus
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# ============ AI Recommendation Models ============
class AIRecommendationBase(BaseModel):
    patient_id: str
    symptom_analysis: str
    severity: Priority
    recommended_department_id: Optional[str] = None
    recommended_doctor_id: Optional[str] = None
    recommended_tests: Optional[str] = None
    immediate_actions: Optional[str] = None
    confidence_score: Optional[float] = None

class AIRecommendationCreate(AIRecommendationBase):
    pass

class AIRecommendation(AIRecommendationBase):
    id: str
    visit_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Feedback Models ============
class FeedbackBase(BaseModel):
    patient_id: str
    rating: int
    feedback_text: Optional[str] = None
    categories: Optional[str] = None
    suggestions: Optional[str] = None
    is_anonymous: bool = False

class FeedbackCreate(FeedbackBase):
    visit_id: Optional[str] = None
    appointment_id: Optional[str] = None
    doctor_id: Optional[str] = None

class Feedback(FeedbackCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Hospital Statistics Models ============
class HospitalStatistics(BaseModel):
    statistic_date: date
    total_patients_today: int
    total_appointments_today: int
    emergency_cases: int
    completed_visits: int
    average_wait_time: Optional[int] = None
    available_doctors: int
    occupied_rooms: int

    class Config:
        from_attributes = True

# ============ Chat Session Models ============
class ChatSessionBase(BaseModel):
    session_id: str
    patient_id: Optional[str] = None
    conversation_data: Optional[dict] = None

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============ Response Models ============
class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
