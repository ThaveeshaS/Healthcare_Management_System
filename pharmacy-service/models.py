from pydantic import BaseModel
from typing import Optional

class Medicine(BaseModel):
    id: int
    name: str
    stock: int
    price: float

class MedicineCreate(BaseModel):
    name: str
    stock: int
    price: float

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None