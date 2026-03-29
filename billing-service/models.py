from pydantic import BaseModel
from typing import Optional
from datetime import date

class Bill(BaseModel):
    id: int
    patient_id: int
    date: date
    payment_method: str
    amount: float
    status: str      # e.g., "paid", "unpaid", "pending"
    items: str       # description of items/services

class BillCreate(BaseModel):
    patient_id: int
    date: date
    payment_method: str
    amount: float
    status: str
    items: str

class BillUpdate(BaseModel):
    patient_id: Optional[int] = None
    date: Optional[date] = None
    payment_method: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    items: Optional[str] = None