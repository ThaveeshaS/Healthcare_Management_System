from fastapi import FastAPI, HTTPException, status
from models import Appointment, AppointmentCreate, AppointmentUpdate
import database as db

app = FastAPI(title="Appointment Microservice", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Appointment Microservice is running"}

@app.get("/api/appointments", response_model=list[Appointment])
def get_all():
    return db.get_all()

@app.get("/api/appointments/{appointment_id}", response_model=Appointment)
def get_by_id(appointment_id: int):
    appointment = db.get_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.post("/api/appointments", response_model=Appointment, status_code=status.HTTP_201_CREATED)
def create(appointment: AppointmentCreate):
    return db.create(appointment)

@app.put("/api/appointments/{appointment_id}", response_model=Appointment)
def update(appointment_id: int, appointment: AppointmentUpdate):
    updated = db.update(appointment_id, appointment)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated

@app.delete("/api/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(appointment_id: int):
    if not db.delete(appointment_id):
        raise HTTPException(status_code=404, detail="Appointment not found")
    return None