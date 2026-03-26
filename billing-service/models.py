from pydantic import BaseModel
from typing import Optional
from datetime import date

class Bill(BaseModel):
    id: int
    patient_id: int
    amount: float
    status: str  # "paid" or "unpaid"
    date: date

class BillCreate(BaseModel):
    patient_id: int
    amount: float
    status: str = "unpaid"
    date: date

class BillUpdate(BaseModel):
    patient_id: Optional[int] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    date: Optional[date] = None # type: ignore