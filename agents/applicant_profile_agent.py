import logging
from typing import Dict, Any
from mcp_servers.applicant_db import ApplicantDBServer

logger = logging.getLogger(__name__)


def analyze_applicant_profile(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze applicant profile using ApplicantDB MCP server."""
    logger.info(f"Analyzing profile for applicant {state['applicant_id']}")

    db_server = ApplicantDBServer()

    applicant_data = {
        "applicant_id": state["applicant_id"],
        "age": state["age"],
        "income": state["income"],
        "employment_type": state["employment_type"],
        "location": state["location"],
    }

    profile = db_server.get_applicant_history(state["applicant_id"])
    employment_info = db_server.get_employment_info(state["employment_type"])

    income_stability_score = calculate_income_stability(
        state["age"],
        state["income"],
        state["employment_type"],
        profile.get("previous_applications", []),
    )

    employment_risk = assess_employment_risk(
        state["employment_type"], employment_info
    )

    credit_history_summary = generate_credit_history_summary(
        profile.get("credit_history", {})
    )

    application_completeness = check_application_completeness(applicant_data)
    missing_fields = identify_missing_fields(applicant_data)

    result = {
        "income_stability_score": income_stability_score,
        "employment_risk": employment_risk,
        "credit_history_summary": credit_history_summary,
        "application_completeness": application_completeness,
        "missing_fields": missing_fields,
        "applicant_age": state["age"],
        "applicant_income": state["income"],
    }

    logger.info(f"Profile analysis complete: {result}")
    return result


def calculate_income_stability(
    age: int, income: float, employment_type: str, previous_applications: list
) -> float:
    """Calculate income stability score based on multiple factors."""
    score = 0.0

    if 25 <= age <= 65:
        score += 30
    elif 18 <= age < 25:
        score += 20
    elif age > 65:
        score += 15

    if income >= 100000:
        score += 30
    elif income >= 50000:
        score += 20
    elif income >= 25000:
        score += 10

    if employment_type in ["Salaried", "Government"]:
        score += 25
    elif employment_type in ["Self-Employed", "Business"]:
        score += 15
    elif employment_type == "Freelancer":
        score += 5

    if len(previous_applications) > 0:
        successful_apps = sum(
            1 for app in previous_applications if app.get("status") == "approved"
        )
        if successful_apps > 0:
            score += min(15, successful_apps * 5)
    print(f"income stability {min(score / 100.0, 1.0)}")
    return min(score / 100.0, 1.0)


def assess_employment_risk(employment_type: str, employment_info: dict) -> str:
    """Assess employment risk based on employment type."""
    risk_mapping = {
        "Salaried": "Low",
        "Government": "Very Low",
        "Self-Employed": "High",
        "Business": "High",
        "Freelancer": "Very High",
        "Unemployed": "Critical",
    }
    return risk_mapping.get(employment_type, "Medium")


def generate_credit_history_summary(credit_history: dict) -> str:
    """Generate a summary of credit history."""
    if not credit_history:
        return "No credit history available"

    summary_parts = []
    if credit_history.get("total_accounts"):
        summary_parts.append(f"Total accounts: {credit_history['total_accounts']}")
    if credit_history.get("active_accounts"):
        summary_parts.append(f"Active accounts: {credit_history['active_accounts']}")
    if credit_history.get("delinquencies"):
        summary_parts.append(f"Delinquencies: {credit_history['delinquencies']}")

    return "; ".join(summary_parts) if summary_parts else "Limited credit history"


def check_application_completeness(applicant_data: dict) -> bool:
    """Check if application has all required fields."""
    required_fields = [
        "applicant_id",
        "age",
        "income",
        "employment_type",
        "location",
    ]
    return all(field in applicant_data and applicant_data[field] for field in required_fields)


def identify_missing_fields(applicant_data: dict) -> list:
    """Identify missing fields in application."""
    required_fields = [
        "applicant_id",
        "age",
        "income",
        "employment_type",
        "location",
    ]
    return [
        field
        for field in required_fields
        if field not in applicant_data or not applicant_data[field]
    ]
