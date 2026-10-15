import logging
from typing import Dict, Any
from mcp_servers.decision_synthesis import DecisionSynthesisServer

logger = logging.getLogger(__name__)


def make_loan_decision(state: Dict[str, Any]) -> Dict[str, Any]:
    """Make final loan decision using DecisionSynthesis MCP server."""
    logger.info(f"Making loan decision for {state['applicant_id']}")

    # decision_server = DecisionSynthesisServer()

    applicant_profile = state.get("applicant_profile", {})
    financial_risk = state.get("financial_risk", {})

    classification = determine_classification(
        applicant_profile, financial_risk, state
    )

    risk_score = calculate_risk_score(applicant_profile, financial_risk, state)

    confidence_level = calculate_confidence(applicant_profile, financial_risk)

    key_factors = extract_key_factors(applicant_profile, financial_risk, state)

    explanation = generate_explanation(
        classification, risk_score, key_factors, applicant_profile, financial_risk
    )

    result = {
        "classification": classification,
        "risk_score": risk_score,
        "confidence_level": confidence_level,
        "key_decision_factors": key_factors,
        "explanation": explanation,
    }

    logger.info(f"Loan decision made: {classification}")
    return result


def determine_classification(
    applicant_profile: dict, financial_risk: dict, state: dict
) -> str:
    """Determine loan classification: Approve, Reject, or Review."""
    risk_score = calculate_risk_score(applicant_profile, financial_risk, state)
    profile_score = applicant_profile.get("income_stability_score", 0)

    reject_triggers = [
        financial_risk.get("anomaly_detected", False),
        financial_risk.get("credit_score_risk_level") == "Very High",
        applicant_profile.get("employment_risk") == "Critical",
        state.get("credit_score", 0) < 300
    ]
    # print(f"reject_triggers: {financial_risk.get('anomaly_detected'),
    #                           financial_risk.get('credit_score_risk_level'),
    #                           applicant_profile.get('employment_risk')
    #     } \n")
    print(f"Reject reson: {reject_triggers}, credit_score: {state.get("credit_score", 0)}")

    if any(reject_triggers):
        return "Reject"

    if risk_score > 0.7 or profile_score < 0.3:
        return "Review"

    if risk_score > 0.5 or profile_score < 0.5:
        return "Review"

    return "Approve"


def calculate_risk_score(
    applicant_profile: dict, financial_risk: dict, state: dict
) -> float:
    """Calculate overall risk score (0.0 to 1.0)."""
    components = {}

    components["credit_score"] = 1.0 - (state.get("credit_score", 0) / 850.0)

    dti = financial_risk.get("debt_to_income_ratio", 0)
    components["dti"] = min(dti, 1.0)

    employment_risk_map = {
        "Very Low": 0.0,
        "Low": 0.15,
        "Medium": 0.3,
        "High": 0.6,
        "Very High": 0.8,
        "Critical": 1.0,
    }
    employment_risk = applicant_profile.get("employment_risk", "Medium")
    components["employment"] = employment_risk_map.get(employment_risk, 0.3)

    if financial_risk.get("anomaly_detected"):
        components["anomaly"] = 0.5

    income_stability = applicant_profile.get("income_stability_score", 0.5)
    components["income_stability"] = 1.0 - income_stability

    weights = {
        "credit_score": 0.3,
        "dti": 0.25,
        "employment": 0.2,
        "anomaly": 0.15,
        "income_stability": 0.1,
    }

    risk_score = sum(
        components.get(key, 0) * weights[key] for key in weights.keys()
    )
    return min(risk_score, 1.0)


def calculate_confidence(applicant_profile: dict, financial_risk: dict) -> float:
    """Calculate confidence level of the decision (0.0 to 1.0)."""
    confidence = 0.5

    if applicant_profile.get("application_completeness", False):
        confidence += 0.2

    missing_fields = len(applicant_profile.get("missing_fields", []))
    confidence -= min(missing_fields * 0.05, 0.15)

    if not financial_risk.get("anomaly_detected", False):
        confidence += 0.15

    return max(min(confidence, 1.0), 0.1)


def extract_key_factors(
    applicant_profile: dict, financial_risk: dict, state: dict
) -> list:
    """Extract key decision factors."""
    factors = []

    credit_score = state.get("credit_score", 0)
    if credit_score >= 750:
        factors.append("Excellent credit score")
    elif credit_score >= 700:
        factors.append("Good credit score")
    elif credit_score < 600:
        factors.append("Poor credit score")

    employment_risk = applicant_profile.get("employment_risk", "Medium")
    if employment_risk == "Low" or employment_risk == "Very Low":
        factors.append("Stable employment")

    dti = financial_risk.get("debt_to_income_ratio", 0)
    if dti < 0.3:
        factors.append("Low debt-to-income ratio")
    elif dti > 0.5:
        factors.append("High debt-to-income ratio")

    income_stability = applicant_profile.get("income_stability_score", 0)
    if income_stability > 0.7:
        factors.append("Strong income stability")

    if financial_risk.get("anomaly_detected"):
        factors.append(f"Anomaly: {financial_risk.get('anomaly_details', 'Unknown')}")

    return factors if factors else ["Application requires expert review"]


def generate_explanation(
    classification: str,
    risk_score: float,
    key_factors: list,
    applicant_profile: dict,
    financial_risk: dict,
) -> str:
    """Generate detailed explanation for the decision."""
    explanation = f"Decision: {classification}. "
    explanation += f"Overall risk score: {risk_score:.2%}. "

    if key_factors:
        explanation += f"Key factors: {', '.join(key_factors[:3])}. "

    if financial_risk.get("anomaly_detected"):
        explanation += f"Note: {financial_risk.get('anomaly_details')} "

    if classification == "Review":
        explanation += (
            "This application requires manual review by our underwriting team."
        )
    elif classification == "Approve":
        explanation += "Application meets our lending criteria."
    else:
        explanation += "Application does not meet our current lending criteria."

    return explanation
