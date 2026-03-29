from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str
    email: str


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


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


class BillCreate(BaseModel):
    patient_id: int
    date: date
    payment_method: str  # Added to match billing service
    amount: float
    status: str = "unpaid"
    items: str           # Added to match billing service

class BillUpdate(BaseModel):
    patient_id: Optional[int] = None
    date: Optional[date] = None
    payment_method: Optional[str] = None # Added
    amount: Optional[float] = None
    status: Optional[str] = None
    items: Optional[str] = None          # Added

class MedicineCreate(BaseModel):
    medicine_name: str
    category: str
    dosage: str
    expiry_date: date
    price: float
    doctor_note: str


class MedicineUpdate(BaseModel):
    medicine_name: Optional[str] = None
    category: Optional[str] = None
    dosage: Optional[str] = None
    expiry_date: Optional[date] = None
    price: Optional[float] = None
    doctor_note: Optional[str] = None
