from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models
import os
import json
from datetime import datetime

# Create Tables (Simple migration for now)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Contract Analysis API", version="1.0")

# CORS Setup
origins = ["*"] # Adjust for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0"}

from .services import (
    analyze_contract_logic, 
    chat_with_contract_logic, 
    compare_contracts_logic, 
    audit_contract_logic, 
    validate_security_logic,
    translate_contract_logic,
    check_alerts_logic
)
from .schemas import (
    AnalysisRequest, ContractAnalysisResponse,
    ChatRequest, ChatResponse,
    CompareRequest, CompareResponse,
    AuditRequest,
    SecurityRequest, SecurityResponse,
    TranslateRequest, TranslateResponse,
    AlertCheckRequest, AlertResponse
)

# ... (Analyze endpoint code) ...

@app.post("/translate", response_model=TranslateResponse)
async def translate_endpoint(request: TranslateRequest):
    return await translate_contract_logic(request.text, request.target_language)

@app.post("/alerts/check", response_model=AlertResponse)
async def check_alerts_endpoint(request: AlertCheckRequest, db: Session = Depends(get_db)):
    contracts = db.query(models.Contract).all()
    return await check_alerts_logic(contracts, request.trigger_email)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = await chat_with_contract_logic(request.contract_text, request.query)
    return {"response": result}

@app.post("/compare", response_model=CompareResponse)
async def compare_endpoint(request: CompareRequest):
    result = await compare_contracts_logic(request.text_a, request.text_b)
    return {"comparison_markdown": result}

@app.post("/audit")
async def audit_endpoint(request: AuditRequest):
    # Returns Dict, schema can be optimized later
    return await audit_contract_logic(request.contract_text)

@app.post("/security/validate", response_model=SecurityResponse)
async def security_validate_endpoint(request: SecurityRequest):
    return await validate_security_logic(request.action_type, request.user_data)


# Imports moved to top

@app.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract_endpoint(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Endpoint to trigger AI analysis and save to DB.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    # Run AI Analysis
    result = await analyze_contract_logic(request.text)
    
    # Save to Database
    db_contract = models.Contract(
        filename=request.filename or "API Upload",
        content_summary=result.get("contract_summary", "")[:2000], # Trucate for summary column
        upload_date=datetime.utcnow(),
        lifecycle_status=result.get("lifecycle_status", "Draft"),
        compliance_score=str(result.get("compliance_score", 0)),
        contract_text=request.text,
        analysis_json=json.dumps(result)
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    
    return result

@app.get("/contracts")
def read_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve contract history.
    """
    contracts = db.query(models.Contract).order_by(models.Contract.upload_date.desc()).offset(skip).limit(limit).all()
    return contracts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
