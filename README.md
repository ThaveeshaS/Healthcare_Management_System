
# Healthcare_Management_System

# Step 01:

# Create virtual environment 
    python -m venv venv 
# Activate virtual environment 
    venv\Scripts\activate 
# Install the packages
    pip install -r requirements.txt 

# Step 02:

cd gateway
uvicorn main:app --reload --port 8000
http://localhost:8000/docs

cd patient-service
uvicorn main:app --reload --port 8001
http://localhost:8001/docs

cd doctor-service
uvicorn main:app --reload --port 8002
http://localhost:8002/docs

cd appointment-service
uvicorn main:app --reload --port 8003
http://localhost:8003/docs

cd billing-service
uvicorn main:app --reload --port 8004
http://localhost:8004/docs

cd pharmacy-service
uvicorn main:app --reload --port 8005
http://localhost:8005/docs


# Group members

patient-service - Thaveesha
doctor-service - Ayanima
appointment-service - Viraj
billing-service - Amesh
pharmacy-service - Sahan