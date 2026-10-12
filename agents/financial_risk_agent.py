import logging
from typing import Dict, Any
from mcp_servers.risk_rules_db import RiskRulesDBServer

logger = logging.getLogger(__name__)


def analyze_financial_risk(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze financial risk using RiskRulesDB MCP server."""
    logger.info(f"Analyzing financial risk for {state['applicant_id']}")

    risk_db = RiskRulesDBServer()

    debt_to_income_ratio = calculate_dti(
        state["existing_liabilities"], state["loan_amount"], state["income"]
    )

    credit_score_risk = assess_credit_score_risk(state["credit_score"])

    loan_amount_risk = assess_loan_amount_risk(state["loan_amount"], state["income"])

    anomaly_result = detect_anomalies(state)

    reasoning = generate_reasoning(
        debt_to_income_ratio, credit_score_risk, loan_amount_risk, anomaly_result
    )

    result = {
        "debt_to_income_ratio": debt_to_income_ratio,
        "credit_score_risk_level": credit_score_risk,
        "loan_amount_risk": loan_amount_risk,
        "anomaly_detected": anomaly_result["detected"],
        "anomaly_details": anomaly_result["details"],
        "reasoning": reasoning,
    }

    logger.info(f"Financial risk analysis complete: {result}")
    return result


def calculate_dti(liabilities: float, loan_amount: float, income: float) -> float:
    """Calculate debt-to-income ratio."""
    if income <= 0:
        return 1.0
    total_monthly_payment = (liabilities + loan_amount) / 12
    dti = (total_monthly_payment * 100) / income
    return min(dti / 100, 1.0)


def assess_credit_score_risk(credit_score: int) -> str:
    """Assess risk level based on credit score."""
    if credit_score >= 750:
        return "Very Low"
    elif credit_score >= 700:
        return "Low"
    elif credit_score >= 650:
        return "Medium"
    elif credit_score >= 600:
        return "High"
    else:
        return "Very High"


def assess_loan_amount_risk(loan_amount: float, income: float) -> str:
    """Assess loan amount risk based on income."""
    if income <= 0:
        return "Critical"
    loan_to_income_ratio = (loan_amount / income)
    if loan_to_income_ratio <= 2:
        return "Low"
    elif loan_to_income_ratio <= 3:
        return "Medium"
    elif loan_to_income_ratio <= 5:
        return "High"
    else:
        return "Very High"


def detect_anomalies(state: Dict[str, Any]) -> Dict[str, Any]:
    """Detect potential anomalies in the application."""
    anomalies = []

    if state.get("age", 0) < 21:
        anomalies.append("Applicant is underage")

    if state.get("credit_score", 0) < 300:
        anomalies.append("Unusually low credit score")

    dti = calculate_dti(
        state["existing_liabilities"], state["loan_amount"], state["income"]
    )
    if dti > 0.5:
        anomalies.append(f"Very high DTI ratio: {dti:.2%}")

    if state.get("loan_amount", 0) > state.get("income", 0) * 10:
        anomalies.append("Loan amount significantly exceeds annual income")

    if state.get("employment_type") == "Unemployed" and state.get("income", 0) > 0:
        anomalies.append("Income reported despite unemployment status")

    return {
        "detected": len(anomalies) > 0,
        "details": "; ".join(anomalies) if anomalies else "No anomalies detected",
    }


def generate_reasoning(
    dti: float, credit_risk: str, loan_risk: str, anomaly_result: dict
) -> str:
    """Generate reasoning for the financial risk assessment."""
    reasoning_parts = [
        f"DTI ratio: {dti:.2%}",
        f"Credit risk level: {credit_risk}",
        f"Loan amount risk: {loan_risk}",
    ]

    if anomaly_result["detected"]:
        reasoning_parts.append(f"Anomalies: {anomaly_result['details']}")

    return "; ".join(reasoning_parts)
