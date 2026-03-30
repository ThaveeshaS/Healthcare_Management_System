from fastapi import FastAPI, HTTPException, status
from models import Doctor, DoctorCreate, DoctorUpdate
import database as db

app = FastAPI(title="Doctor Microservice", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Doctor Microservice is running"}

@app.get("/api/doctors", response_model=list[Doctor]) # Get all doctors
def get_all():
    return db.get_all()

@app.get("/api/doctors/{doctor_id}", response_model=Doctor) # Get doctor by ID
def get_by_id(doctor_id: int):
    doctor = db.get_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/api/doctors", response_model=Doctor, status_code=status.HTTP_201_CREATED)
def create(doctor: DoctorCreate):
    return db.create(doctor)

@app.put("/api/doctors/{doctor_id}", response_model=Doctor)
def update(doctor_id: int, doctor: DoctorUpdate):
    updated = db.update(doctor_id, doctor)
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated

@app.delete("/api/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(doctor_id: int):
    if not db.delete(doctor_id):
        raise HTTPException(status_code=404, detail="Doctor not found")
    return None