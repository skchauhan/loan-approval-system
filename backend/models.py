from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ApplicantInfo(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    location: str


class LoanApplicationRequest(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    loan_tenure_months: int
    existing_liabilities: float
    location: str
    timestamp: Optional[datetime] = None


class ApplicantProfileResponse(BaseModel):
    income_stability_score: float
    employment_risk: str
    credit_history_summary: str
    application_completeness: bool
    missing_fields: list


class FinancialRiskResponse(BaseModel):
    debt_to_income_ratio: float
    credit_score_risk_level: str
    loan_amount_risk: str
    anomaly_detected: bool
    anomaly_details: str
    reasoning: str


class LoanDecisionResponse(BaseModel):
    classification: str  # Approve, Reject, or Review
    risk_score: float
    confidence_level: float
    key_decision_factors: list
    explanation: str


class ComplianceResponse(BaseModel):
    action_taken: str
    notification_sent: bool
    case_id: str
    timestamp: datetime
    summary: str


class FinalDecisionResponse(BaseModel):
    case_id: str
    applicant_id: str
    decision: str
    risk_score: float
    confidence_level: float
    applicant_profile: ApplicantProfileResponse
    financial_risk: FinancialRiskResponse
    loan_decision: LoanDecisionResponse
    compliance_status: ComplianceResponse
    timestamp: datetime
