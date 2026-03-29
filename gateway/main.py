from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import httpx
from typing import Any
from middleware import LoggingMiddleware
from models import (
    AppointmentCreate,
    AppointmentUpdate,
    BillCreate,
    BillUpdate,
    DoctorCreate,
    DoctorUpdate,
    MedicineCreate,
    MedicineUpdate,
    PatientCreate,
    PatientUpdate,
)
# from auth import get_current_user  # uncomment if using JWT

app = FastAPI(title="API Gateway", version="1.0.0")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Service URLs
SERVICES = {
    "patient": "http://localhost:8001",
    "doctor": "http://localhost:8002",
    "appointment": "http://localhost:8003",
    "billing": "http://localhost:8004",
    "pharmacy": "http://localhost:8005"
}

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}

# Optional login endpoint for JWT
# from auth import Token, User, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# from datetime import timedelta
#
# @app.post("/login", response_model=Token)
# async def login(user: User):
#     authenticated = authenticate_user(user.username, user.password)
#     if not authenticated:
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# Patient routes
@app.get("/gateway/patients")
async def get_all_patients():
    return await forward_request("patient", "/api/patients", "GET")

@app.get("/gateway/patients/{patient_id}")
async def get_patient(patient_id: int):
    return await forward_request("patient", f"/api/patients/{patient_id}", "GET")

@app.post("/gateway/patients")
async def create_patient(body: PatientCreate):
    payload = jsonable_encoder(body)
    return await forward_request("patient", "/api/patients", "POST", json=payload)

@app.put("/gateway/patients/{patient_id}")
async def update_patient(patient_id: int, body: PatientUpdate):
    payload = jsonable_encoder(body, exclude_none=True)
    return await forward_request("patient", f"/api/patients/{patient_id}", "PUT", json=payload)

@app.delete("/gateway/patients/{patient_id}")
async def delete_patient(patient_id: int):
    return await forward_request("patient", f"/api/patients/{patient_id}", "DELETE")

# Doctor routes
@app.get("/gateway/doctors")
async def get_all_doctors():
    return await forward_request("doctor", "/api/doctors", "GET")

@app.get("/gateway/doctors/{doctor_id}")
async def get_doctor(doctor_id: int):
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "GET")

@app.post("/gateway/doctors")
async def create_doctor(body: DoctorCreate):
    payload = jsonable_encoder(body)
    return await forward_request("doctor", "/api/doctors", "POST", json=payload)

@app.put("/gateway/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, body: DoctorUpdate):
    payload = jsonable_encoder(body, exclude_none=True)
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "PUT", json=payload)

@app.delete("/gateway/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int):
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "DELETE")

# Appointment routes
@app.get("/gateway/appointments")
async def get_all_appointments():
    return await forward_request("appointment", "/api/appointments", "GET")

@app.get("/gateway/appointments/{appointment_id}")
async def get_appointment(appointment_id: int):
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "GET")

@app.post("/gateway/appointments")
async def create_appointment(body: AppointmentCreate):
    payload = jsonable_encoder(body)
    return await forward_request("appointment", "/api/appointments", "POST", json=payload)

@app.put("/gateway/appointments/{appointment_id}")
async def update_appointment(appointment_id: int, body: AppointmentUpdate):
    payload = jsonable_encoder(body, exclude_none=True)
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "PUT", json=payload)

@app.delete("/gateway/appointments/{appointment_id}")
async def delete_appointment(appointment_id: int):
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "DELETE")

# Billing routes

@app.get("/gateway/bills")
async def get_all_bills():
    return await forward_request("billing", "/api/bills", "GET")

@app.get("/gateway/bills/{bill_id}")
async def get_bill(bill_id: int):
    return await forward_request("billing", f"/api/bills/{bill_id}", "GET")

@app.post("/gateway/bills")
async def create_bill(body: BillCreate):
    # jsonable_encoder converts 'date' objects to ISO strings automatically
    payload = jsonable_encoder(body)
    return await forward_request("billing", "/api/bills", "POST", json=payload)

@app.put("/gateway/bills/{bill_id}")
async def update_bill(bill_id: int, body: BillUpdate):
    # exclude_none=True ensures we only send fields the user wants to change
    payload = jsonable_encoder(body, exclude_none=True)
    return await forward_request("billing", f"/api/bills/{bill_id}", "PUT", json=payload)

@app.delete("/gateway/bills/{bill_id}")
async def delete_bill(bill_id: int):
    return await forward_request("billing", f"/api/bills/{bill_id}", "DELETE")

# Pharmacy routes
@app.get("/gateway/medicines")
async def get_all_medicines():
    return await forward_request("pharmacy", "/api/medicines", "GET")

@app.get("/gateway/medicines/{medicine_id}")
async def get_medicine(medicine_id: int):
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "GET")

@app.post("/gateway/medicines")
async def create_medicine(body: MedicineCreate):
    payload = jsonable_encoder(body)
    return await forward_request("pharmacy", "/api/medicines", "POST", json=payload)

@app.put("/gateway/medicines/{medicine_id}")
async def update_medicine(medicine_id: int, body: MedicineUpdate):
    payload = jsonable_encoder(body, exclude_none=True)
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "PUT", json=payload)

@app.delete("/gateway/medicines/{medicine_id}")
async def delete_medicine(medicine_id: int):
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "DELETE")