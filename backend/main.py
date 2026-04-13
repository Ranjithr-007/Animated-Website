from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from . import models
from .database import engine, get_db

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nila Builders Backend API")

# Setup CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for form validation
class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    consentGiven: bool

    class Config:
        from_attributes = True

@app.post("/api/leads")
async def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    if not lead.consentGiven:
        raise HTTPException(status_code=400, detail="Privacy consent is required.")
        
    db_lead = models.Lead(
        full_name=lead.name,
        email=lead.email,
        phone_number=lead.phone,
        consent_given=lead.consentGiven
    )
    
    try:
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return {"status": "success", "message": "Lead captured successfully", "lead_id": db_lead.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Nila Builders API is running. Test the connection at /api/leads"}
