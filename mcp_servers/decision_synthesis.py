"""DecisionSynthesis MCP Server - Synthesizes loan decisions."""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class DecisionSynthesisServer:
    """MCP Server for decision synthesis and policy enforcement."""

    def __init__(self):
        self.policies = self._initialize_policies()

    def _initialize_policies(self) -> Dict[str, Any]:
        """Initialize lending policies."""
        return {
            "min_credit_score": 600,
            "max_dti": 0.50,
            "max_loan_to_income": 5.0,
            "approval_age_range": (21, 75),
            "processing_fee_percent": 0.01,
            "interest_rate_base": 0.05,
        }

    def synthesize_decision(
        self,
        applicant_profile: Dict,
        financial_risk: Dict,
        application_data: Dict,
    ) -> Dict[str, Any]:
        """Synthesize final decision based on all factors."""
        decision_factors = []
        risk_score = 0.0
        confidence = 0.5

        policy_violations = self.check_policy_violations(
            applicant_profile, financial_risk, application_data
        )

        if policy_violations:
            return {
                "classification": "Reject",
                "risk_score": 0.9,
                "confidence": 0.95,
                "reasons": policy_violations,
            }

        credit_factor = self.evaluate_credit_profile(
            applicant_profile, financial_risk
        )
        financial_factor = self.evaluate_financial_stability(
            applicant_profile, financial_risk
        )
        employment_factor = self.evaluate_employment_stability(applicant_profile)

        risk_score = (
            credit_factor * 0.35
            + financial_factor * 0.35
            + employment_factor * 0.30
        )
        confidence = self.calculate_decision_confidence(
            applicant_profile, financial_risk
        )

        if risk_score > 0.7:
            classification = "Reject"
        elif risk_score > 0.5:
            classification = "Review"
        else:
            classification = "Approve"

        return {
            "classification": classification,
            "risk_score": risk_score,
            "confidence": confidence,
            "factors": decision_factors,
        }

    def check_policy_violations(
        self, applicant_profile: Dict, financial_risk: Dict, application_data: Dict
    ) -> List[str]:
        """Check for policy violations."""
        violations = []
        policies = self.policies

        credit_score = application_data.get("credit_score", 0)
        if credit_score < policies["min_credit_score"]:
            violations.append(
                f"Credit score {credit_score} below minimum {policies['min_credit_score']}"
            )

        dti = financial_risk.get("debt_to_income_ratio", 0)
        if dti > policies["max_dti"]:
            violations.append(f"DTI {dti:.2%} exceeds maximum {policies['max_dti']:.2%}")

        employment_risk = applicant_profile.get("employment_risk", "Medium")
        if employment_risk == "Critical":
            violations.append("Critical employment risk level")

        if financial_risk.get("anomaly_detected"):
            violations.append(f"Anomaly detected: {financial_risk.get('anomaly_details')}")

        return violations

    def evaluate_credit_profile(
        self, applicant_profile: Dict, financial_risk: Dict
    ) -> float:
        """Evaluate credit profile (0.0 = best, 1.0 = worst)."""
        risk_level = financial_risk.get("credit_score_risk_level", "Medium")
        risk_map = {
            "Very Low": 0.1,
            "Low": 0.25,
            "Medium": 0.5,
            "High": 0.75,
            "Very High": 0.95,
        }
        return risk_map.get(risk_level, 0.5)

    def evaluate_financial_stability(
        self, applicant_profile: Dict, financial_risk: Dict
    ) -> float:
        """Evaluate financial stability (0.0 = best, 1.0 = worst)."""
        dti = financial_risk.get("debt_to_income_ratio", 0)
        loan_risk = financial_risk.get("loan_amount_risk", "Medium")

        dti_score = min(dti * 2, 1.0)

        loan_risk_map = {
            "Low": 0.1,
            "Medium": 0.4,
            "High": 0.7,
            "Very High": 0.95,
        }
        loan_score = loan_risk_map.get(loan_risk, 0.5)

        return (dti_score * 0.6 + loan_score * 0.4)

    def evaluate_employment_stability(self, applicant_profile: Dict) -> float:
        """Evaluate employment stability (0.0 = best, 1.0 = worst)."""
        employment_risk = applicant_profile.get("employment_risk", "Medium")
        employment_map = {
            "Very Low": 0.05,
            "Low": 0.15,
            "Medium": 0.4,
            "High": 0.7,
            "Very High": 0.9,
            "Critical": 1.0,
        }
        return employment_map.get(employment_risk, 0.4)

    def calculate_decision_confidence(
        self, applicant_profile: Dict, financial_risk: Dict
    ) -> float:
        """Calculate confidence level of decision."""
        confidence = 0.5

        if applicant_profile.get("application_completeness"):
            confidence += 0.25

        if not financial_risk.get("anomaly_detected"):
            confidence += 0.15

        missing_fields = len(applicant_profile.get("missing_fields", []))
        confidence -= min(missing_fields * 0.08, 0.2)

        return max(min(confidence, 1.0), 0.1)

    def calculate_interest_rate(
        self,
        base_rate: float,
        credit_score: int,
        dti: float,
        employment_risk: str,
    ) -> float:
        """Calculate interest rate based on risk factors."""
        rate = base_rate

        if credit_score < 600:
            rate += 0.05
        elif credit_score < 700:
            rate += 0.02
        elif credit_score >= 750:
            rate -= 0.01

        if dti > 0.5:
            rate += 0.03
        elif dti > 0.4:
            rate += 0.01

        employment_premium = {
            "Very Low": -0.005,
            "Low": 0.0,
            "Medium": 0.01,
            "High": 0.03,
            "Very High": 0.05,
            "Critical": 0.1,
        }
        rate += employment_premium.get(employment_risk, 0.01)

        return max(rate, 0.02)

    def get_approval_conditions(self, decision_data: Dict) -> List[str]:
        """Get any conditions for approval."""
        conditions = []

        if decision_data.get("risk_score", 0) > 0.6:
            conditions.append("Requires co-borrower or higher income verification")

        if decision_data.get("confidence", 1.0) < 0.7:
            conditions.append("Additional documentation required")

        if decision_data.get("credit_score", 0) < 650:
            conditions.append("Annual credit score review required")

        return conditions
