from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Clause(BaseModel):
    clause_name: Optional[str] = "Unknown"
    clause_text: Optional[str] = None
    start_index: Optional[int] = None
    end_index: Optional[int] = None
    risk_level: str = "Low"
    risk_reason: Optional[str] = None
    highlight: bool = False

class HighlightSummary(BaseModel):
    high_risk_count: int = 0
    medium_risk_count: int = 0

class ContractAnalysisResponse(BaseModel):
    contract_type: Optional[str] = "Unknown"
    contract_summary: Optional[str] = "No summary available"
    lifecycle_status: Optional[str] = "Unknown"
    compliance_score: Optional[Any] = 0 # Allow strings/ints to prevent validation error
    document_source: Optional[str] = "Unknown"
    key_clauses_summary: List[str] = []
    clauses: List[Clause] = []
    highlight_summary: HighlightSummary
    ocr_notes: Optional[str] = None
    model_used: Optional[str] = None

class AnalysisRequest(BaseModel):
    text: str
    filename: Optional[str] = "unknown"

class ChatRequest(BaseModel):
    contract_text: str
    query: str

class CompareRequest(BaseModel):
    text_a: str
    text_b: str

class AuditRequest(BaseModel):
    contract_text: str

class SecurityRequest(BaseModel):
    action_type: str
    user_data: Dict[str, Any]

class ChatResponse(BaseModel):
    response: str

class CompareResponse(BaseModel):
    comparison_markdown: str

class SecurityResponse(BaseModel):
    signup_validation: Optional[Dict[str, Any]] = None
    login_security: Optional[Dict[str, Any]] = None
    authorization: Optional[Dict[str, Any]] = None
    role_aware_ai_policy: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class TranslateRequest(BaseModel):
    text: str
    target_language: str

class TranslateResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = "Unknown"

class AlertCheckRequest(BaseModel):
    trigger_email: bool = False # If true, simulate sending emails

class AlertResponse(BaseModel):
    alerts_generated: List[str]
    emails_sent: int



class Token(BaseModel):
    access_token: str
    token_type: str
