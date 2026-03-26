from fastapi import FastAPI, HTTPException, status
from models import Patient, PatientCreate, PatientUpdate
import database as db

app = FastAPI(title="Patient Microservice", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Patient Microservice is running"}

@app.get("/api/patients", response_model=list[Patient])
def get_all():
    return db.get_all()

@app.get("/api/patients/{patient_id}", response_model=Patient)
def get_by_id(patient_id: int):
    patient = db.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/api/patients", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create(patient: PatientCreate):
    return db.create(patient)

@app.put("/api/patients/{patient_id}", response_model=Patient)
def update(patient_id: int, patient: PatientUpdate):
    updated = db.update(patient_id, patient)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated

@app.delete("/api/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(patient_id: int):
    if not db.delete(patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return None