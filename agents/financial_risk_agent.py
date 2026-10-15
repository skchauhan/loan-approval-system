import logging
from typing import Dict, Any
from mcp_servers.risk_rules_db import RiskRulesDBServer

logger = logging.getLogger(__name__)


def analyze_financial_risk(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze financial risk using RiskRulesDB MCP server."""
    logger.info(f"Analyzing financial risk for {state['applicant_id']}")

    risk_db = RiskRulesDBServer()

    # Check blacklist first
    is_blacklisted = risk_db.check_black_list(state["applicant_id"])
    if is_blacklisted:
        logger.warning(f"Applicant {state['applicant_id']} is blacklisted")
        return {
            "blacklisted": True,
            "reasoning": "Applicant is on the blacklist",
            "risk_level": "Critical",
        }

    # Check age eligibility
    age_eligible = risk_db.check_age_eligibility(state.get("age", 0))

    # Calculate DTI using risk_db
    monthly_liabilities = state["existing_liabilities"] / 12
    monthly_income = state["income"] / 12
    debt_to_income_ratio, dti_risk = risk_db.calculate_debt_to_income(
        monthly_liabilities, monthly_income
    )

    # Get credit score risk from risk_db
    credit_score_risk = risk_db.get_credit_score_risk(state["credit_score"])

    # Validate loan amount using risk_db
    loan_validation = risk_db.validate_loan_amount(
        state["loan_amount"], state["income"]
    )

    # Get location risk
    location_risk = risk_db.get_location_risk(state.get("location", ""))

    # Detect fraud patterns
    fraud_check = risk_db.detect_application_fraud(state)

    # Detect other anomalies
    anomaly_result = detect_anomalies(state)

    reasoning = generate_reasoning(
        debt_to_income_ratio,
        dti_risk,
        credit_score_risk,
        loan_validation,
        location_risk,
        fraud_check,
        anomaly_result,
        age_eligible,
    )

    result = {
        "debt_to_income_ratio": debt_to_income_ratio,
        "dti_risk_level": dti_risk,
        "credit_score_risk_level": credit_score_risk,
        "loan_validation": loan_validation,
        "location_risk": location_risk,
        "age_eligible": age_eligible,
        "fraud_detected": fraud_check["fraud_detected"],
        "fraud_score": fraud_check["fraud_score"],
        "fraud_indicators": fraud_check["indicators"],
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
    dti: float,
    dti_risk: str,
    credit_risk: str,
    loan_validation: dict,
    location_risk: dict,
    fraud_check: dict,
    anomaly_result: dict,
    age_eligible: bool,
) -> str:
    """Generate comprehensive reasoning for the financial risk assessment."""
    reasoning_parts = [
        f"DTI ratio: {dti:.2%} ({dti_risk})",
        f"Credit risk level: {credit_risk}",
        f"Loan validation: {loan_validation['risk_level']} (LTI: {loan_validation['loan_to_income']:.2f})",
        f"Location risk: {location_risk['risk']}",
        f"Age eligible: {'Yes' if age_eligible else 'No'}",
    ]

    if not loan_validation["valid"]:
        reasoning_parts.append(
            f"Loan exceeds max recommended: ${loan_validation['max_recommended_amount']:,.0f}"
        )

    if fraud_check["fraud_detected"]:
        reasoning_parts.append(
            f"Fraud detected (score: {fraud_check['fraud_score']:.2f}): {', '.join(fraud_check['indicators'])}"
        )

    if anomaly_result["detected"]:
        reasoning_parts.append(f"Anomalies: {anomaly_result['details']}")

    return "; ".join(reasoning_parts)
