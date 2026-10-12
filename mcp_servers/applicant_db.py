"""ApplicantDB MCP Server - Manages applicant profile data and history."""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ApplicantDBServer:
    """MCP Server for applicant database operations."""

    def __init__(self):
        self.applicants_db = self._initialize_sample_database()

    def _initialize_sample_database(self) -> Dict[str, Any]:
        """Initialize with sample applicant data."""
        return {
            "APP001": {
                "name": "John Doe",
                "age": 35,
                "income": 75000,
                "employment_type": "Salaried",
                "location": "New York",
                "credit_history": {
                    "total_accounts": 4,
                    "active_accounts": 3,
                    "delinquencies": 0,
                },
                "previous_applications": [
                    {"date": "2023-01-15", "status": "approved", "amount": 50000}
                ],
                "kyc_verified": True,
            },
            "APP002": {
                "name": "Jane Smith",
                "age": 28,
                "income": 120000,
                "employment_type": "Self-Employed",
                "location": "California",
                "credit_history": {
                    "total_accounts": 5,
                    "active_accounts": 4,
                    "delinquencies": 1,
                },
                "previous_applications": [],
                "kyc_verified": True,
            },
        }

    def get_applicant_history(self, applicant_id: str) -> Dict[str, Any]:
        """Retrieve applicant history and profile."""
        if applicant_id in self.applicants_db:
            applicant = self.applicants_db[applicant_id]
            return {
                "applicant_id": applicant_id,
                "name": applicant.get("name", "Unknown"),
                "kyc_verified": applicant.get("kyc_verified", False),
                "credit_history": applicant.get("credit_history", {}),
                "previous_applications": applicant.get("previous_applications", []),
                "total_previous_applications": len(
                    applicant.get("previous_applications", [])
                ),
            }
        else:
            return {
                "applicant_id": applicant_id,
                "name": "Unknown",
                "kyc_verified": False,
                "credit_history": {},
                "previous_applications": [],
                "total_previous_applications": 0,
            }

    def get_employment_info(self, employment_type: str) -> Dict[str, Any]:
        """Get employment type risk information."""
        employment_data = {
            "Salaried": {
                "risk_level": "Low",
                "stability_score": 0.85,
                "income_continuity": "High",
                "default_rate": 0.02,
            },
            "Government": {
                "risk_level": "Very Low",
                "stability_score": 0.95,
                "income_continuity": "Very High",
                "default_rate": 0.005,
            },
            "Self-Employed": {
                "risk_level": "High",
                "stability_score": 0.55,
                "income_continuity": "Low",
                "default_rate": 0.08,
            },
            "Business": {
                "risk_level": "High",
                "stability_score": 0.6,
                "income_continuity": "Medium",
                "default_rate": 0.07,
            },
            "Freelancer": {
                "risk_level": "Very High",
                "stability_score": 0.4,
                "income_continuity": "Very Low",
                "default_rate": 0.15,
            },
            "Unemployed": {
                "risk_level": "Critical",
                "stability_score": 0.0,
                "income_continuity": "None",
                "default_rate": 0.5,
            },
        }
        return employment_data.get(
            employment_type,
            {
                "risk_level": "Medium",
                "stability_score": 0.5,
                "income_continuity": "Medium",
                "default_rate": 0.05,
            },
        )

    def verify_kyc(self, applicant_id: str) -> bool:
        """Verify KYC status."""
        if applicant_id in self.applicants_db:
            return self.applicants_db[applicant_id].get("kyc_verified", False)
        return False

    def get_credit_score_trend(self, applicant_id: str) -> Dict[str, Any]:
        """Get credit score trend over time."""
        return {
            "applicant_id": applicant_id,
            "trend": [
                {"date": "2024-01", "score": 720},
                {"date": "2024-02", "score": 725},
                {"date": "2024-03", "score": 730},
            ],
            "current_score": 730,
        }

    def check_fraud_indicators(self, applicant_id: str, data: Dict) -> bool:
        """Check for fraud indicators."""
        fraud_flags = []

        if data.get("age", 0) < 18:
            fraud_flags.append("Underage applicant")

        if data.get("income", 0) < 0:
            fraud_flags.append("Invalid income")

        if len(fraud_flags) > 0:
            logger.warning(f"Fraud flags for {applicant_id}: {fraud_flags}")
            return True

        return False
