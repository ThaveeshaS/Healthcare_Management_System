from fastapi import FastAPI, HTTPException, status
from models import Medicine, MedicineCreate, MedicineUpdate
import database as db

app = FastAPI(title="Pharmacy Microservice", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Pharmacy Microservice is running"}

@app.get("/api/medicines", response_model=list[Medicine])
def get_all():
    return db.get_all()

@app.get("/api/medicines/{medicine_id}", response_model=Medicine)
def get_by_id(medicine_id: int):
    medicine = db.get_by_id(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@app.post("/api/medicines", response_model=Medicine, status_code=status.HTTP_201_CREATED)
def create(medicine: MedicineCreate):
    return db.create(medicine)

@app.put("/api/medicines/{medicine_id}", response_model=Medicine)
def update(medicine_id: int, medicine: MedicineUpdate):
    updated = db.update(medicine_id, medicine)
    if not updated:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return updated

@app.delete("/api/medicines/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(medicine_id: int):
    if not db.delete(medicine_id):
        raise HTTPException(status_code=404, detail="Medicine not found")
    return None