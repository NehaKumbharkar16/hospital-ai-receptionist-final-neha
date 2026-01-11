from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Ward(str, Enum):
    GENERAL = "general"
    EMERGENCY = "emergency"
    MENTAL_HEALTH = "mental_health"

class PatientData(BaseModel):
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    patient_query: Optional[str] = None
    ward: Optional[Ward] = None

class ChatMessage(BaseModel):
    message: str
    session_id: str

class WebhookPayload(BaseModel):
    patient_name: str
    patient_age: int
    patient_query: str
    ward: Ward