from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content_summary = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)
    lifecycle_status = Column(String)
    compliance_score = Column(String) # Keeping as String to match legacy, though Float/Integer is better for Postgres
    contract_text = Column(Text) # Store original text for Search/Chat/Analytics
    analysis_json = Column(Text) # JSON blob
