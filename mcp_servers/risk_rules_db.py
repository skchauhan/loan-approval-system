"""RiskRulesDB MCP Server - Manages financial risk rules and calculations."""

import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)


class RiskRulesDBServer:
    """MCP Server for financial risk rules and analysis."""

    def __init__(self):
        self.risk_thresholds = self._initialize_risk_thresholds()

    def _initialize_risk_thresholds(self) -> Dict[str, Any]:
        """Initialize risk threshold rules."""
        return {
            "dti_acceptable": 0.43,
            "dti_caution": 0.50,
            "dti_danger": 0.60,
            "credit_score_excellent": 750,
            "credit_score_good": 700,
            "credit_score_fair": 650,
            "credit_score_poor": 600,
            "loan_to_income_safe": 2.5,
            "loan_to_income_caution": 4.0,
            "loan_to_income_danger": 6.0,
            "age_min": 21,
            "age_max": 75,
        }

    def calculate_debt_to_income(
        self, monthly_liabilities: float, monthly_income: float
    ) -> Tuple[float, str]:
        """Calculate DTI ratio and risk level."""
        if monthly_income <= 0:
            return 1.0, "Critical"

        dti = monthly_liabilities / monthly_income
        thresholds = self.risk_thresholds

        if dti <= thresholds["dti_acceptable"]:
            risk = "Low"
        elif dti <= thresholds["dti_caution"]:
            risk = "Medium"
        elif dti <= thresholds["dti_danger"]:
            risk = "High"
        else:
            risk = "Very High"

        return dti, risk

    def get_credit_score_risk(self, credit_score: int) -> str:
        """Get credit score risk level."""
        thresholds = self.risk_thresholds

        if credit_score >= thresholds["credit_score_excellent"]:
            return "Very Low"
        elif credit_score >= thresholds["credit_score_good"]:
            return "Low"
        elif credit_score >= thresholds["credit_score_fair"]:
            return "Medium"
        elif credit_score >= thresholds["credit_score_poor"]:
            return "High"
        else:
            return "Very High"

    def validate_loan_amount(
        self, loan_amount: float, annual_income: float
    ) -> Dict[str, Any]:
        """Validate loan amount against income."""
        if annual_income <= 0:
            return {
                "valid": False,
                "reason": "Invalid income",
                "loan_to_income": None,
            }

        lti = loan_amount / annual_income
        thresholds = self.risk_thresholds

        if lti <= thresholds["loan_to_income_safe"]:
            valid = True
            risk = "Low"
        elif lti <= thresholds["loan_to_income_caution"]:
            valid = True
            risk = "Medium"
        elif lti <= thresholds["loan_to_income_danger"]:
            valid = True
            risk = "High"
        else:
            valid = False
            risk = "Very High"

        return {
            "valid": valid,
            "loan_to_income": lti,
            "risk_level": risk,
            "max_recommended_amount": annual_income * thresholds["loan_to_income_safe"],
        }

    def check_age_eligibility(self, age: int) -> bool:
        """Check age eligibility for loan."""
        min_age = self.risk_thresholds["age_min"]
        max_age = self.risk_thresholds["age_max"]
        return min_age <= age <= max_age

    def check_black_list(self, applicant_id: str) -> bool:
        """Check if applicant is on blacklist."""
        blacklist = ["FRAUD001", "DEFAULT001", "BLOCKED001"]
        return applicant_id in blacklist

    def get_location_risk(self, location: str) -> Dict[str, Any]:
        """Get location-based risk assessment."""
        location_risk_map = {
            "New York": {"risk": "Low", "unemployment_rate": 0.04},
            "California": {"risk": "Low", "unemployment_rate": 0.05},
            "Texas": {"risk": "Medium", "unemployment_rate": 0.06},
            "Florida": {"risk": "Medium", "unemployment_rate": 0.07},
            "Default": {"risk": "Medium", "unemployment_rate": 0.05},
        }
        return location_risk_map.get(
            location, location_risk_map["Default"]
        )

    def evaluate_application_completeness(
        self, required_fields: Dict[str, bool]
    ) -> Tuple[bool, list]:
        """Evaluate if application has all required information."""
        missing = [field for field, present in required_fields.items() if not present]
        return len(missing) == 0, missing

    def detect_application_fraud(self, applicant_data: Dict) -> Dict[str, Any]:
        """Detect potential fraud patterns."""
        fraud_indicators = []
        fraud_score = 0

        if applicant_data.get("credit_score", 0) < 0:
            fraud_indicators.append("Negative credit score")
            fraud_score += 0.3

        if applicant_data.get("income", 0) < 0:
            fraud_indicators.append("Negative income")
            fraud_score += 0.4

        if applicant_data.get("age", 0) < 18 or applicant_data.get("age", 0) > 120:
            fraud_indicators.append("Invalid age")
            fraud_score += 0.2

        if applicant_data.get("loan_amount", 0) > applicant_data.get("income", 0) * 20:
            fraud_indicators.append("Unusually high loan amount")
            fraud_score += 0.15

        return {
            "fraud_detected": fraud_score > 0.3,
            "fraud_score": min(fraud_score, 1.0),
            "indicators": fraud_indicators,
        }
