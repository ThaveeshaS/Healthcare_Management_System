from fastapi import FastAPI, HTTPException, status
from models import Bill, BillCreate, BillUpdate
import database as db

app = FastAPI(title="Billing Microservice", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Billing Microservice is running"}

@app.get("/api/bills", response_model=list[Bill])
def get_all():
    return db.get_all()

@app.get("/api/bills/{bill_id}", response_model=Bill)
def get_by_id(bill_id: int):
    bill = db.get_by_id(bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill

@app.post("/api/bills", response_model=Bill, status_code=status.HTTP_201_CREATED)
def create(bill: BillCreate):
    return db.create(bill)

@app.put("/api/bills/{bill_id}", response_model=Bill)
def update(bill_id: int, bill: BillUpdate):
    updated = db.update(bill_id, bill)
    if not updated:
        raise HTTPException(status_code=404, detail="Bill not found")
    return updated

@app.delete("/api/bills/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(bill_id: int):
    if not db.delete(bill_id):
        raise HTTPException(status_code=404, detail="Bill not found")
    return None