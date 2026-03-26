from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class Appointment(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str  # e.g., "scheduled", "completed", "cancelled"

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str = "scheduled"

class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[str] = None