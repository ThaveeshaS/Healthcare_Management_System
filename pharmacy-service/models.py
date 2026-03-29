from pydantic import BaseModel
from typing import Optional
from datetime import date

class Medicine(BaseModel):
    id: int
    medicine_name: str
    category: str
    dosage: str
    expiry_date: date
    price: float
    doctor_note: str

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