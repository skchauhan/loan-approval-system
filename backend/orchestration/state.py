from typing import TypedDict, Optional, Any, List


class ApplicationState(TypedDict):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    loan_tenure_months: int
    existing_liabilities: float
    location: str
    timestamp: str
    case_id: str

    applicant_profile: Optional[dict]
    financial_risk: Optional[dict]
    loan_decision: Optional[dict]
    compliance_status: Optional[dict]

    final_decision: Optional[str]
    risk_score: Optional[float]
    confidence_level: Optional[float]
    decision_rationale: Optional[str]
    errors: Optional[List[str]]
