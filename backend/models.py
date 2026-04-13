from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Lead(Base):
    __tablename__ = "brochure_leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    phone_number = Column(String(15), nullable=False)
    consent_given = Column(Boolean, default=False)
    download_date = Column(DateTime(timezone=True), server_default=func.now())
