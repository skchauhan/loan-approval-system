"""NotificationSystem MCP Server - Handles notifications and compliance."""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class NotificationSystemServer:
    """MCP Server for notifications and audit trail."""

    def __init__(self):
        self.notifications_log = []
        self.audit_trail = []

    def send_approval_notification(self, notification_data: Dict) -> bool:
        """Send approval notification."""
        message = {
            "type": "approval",
            "applicant_id": notification_data.get("applicant_id"),
            "case_id": notification_data.get("case_id"),
            "timestamp": datetime.now().isoformat(),
            "subject": "Loan Application Approved",
            "body": f"Your loan application has been approved. Case #{notification_data.get('case_id')}",
        }

        self.notifications_log.append(message)
        self._log_audit(
            notification_data.get("applicant_id"),
            "Approval notification sent",
            notification_data,
        )
        logger.info(f"Approval notification sent: {message}")
        return True

    def send_rejection_notification(self, notification_data: Dict) -> bool:
        """Send rejection notification."""
        message = {
            "type": "rejection",
            "applicant_id": notification_data.get("applicant_id"),
            "case_id": notification_data.get("case_id"),
            "timestamp": datetime.now().isoformat(),
            "subject": "Loan Application Decision",
            "body": f"Your application has been reviewed. Case #{notification_data.get('case_id')}",
        }

        self.notifications_log.append(message)
        self._log_audit(
            notification_data.get("applicant_id"),
            "Rejection notification sent",
            notification_data,
        )
        logger.info(f"Rejection notification sent: {message}")
        return True

    def send_review_notification(self, notification_data: Dict) -> bool:
        """Send review notification."""
        message = {
            "type": "review",
            "applicant_id": notification_data.get("applicant_id"),
            "case_id": notification_data.get("case_id"),
            "timestamp": datetime.now().isoformat(),
            "subject": "Application Under Review",
            "body": f"Your application is under review by our team. Case #{notification_data.get('case_id')}",
        }

        self.notifications_log.append(message)
        self._log_audit(
            notification_data.get("applicant_id"),
            "Review notification sent",
            notification_data,
        )
        logger.info(f"Review notification sent: {message}")
        return True

    def create_audit_record(self, decision_data: Dict) -> Dict[str, Any]:
        """Create audit record for compliance."""
        record = {
            "case_id": decision_data.get("case_id"),
            "applicant_id": decision_data.get("applicant_id"),
            "timestamp": datetime.now().isoformat(),
            "decision": decision_data.get("decision"),
            "risk_score": decision_data.get("risk_score"),
            "credit_score": decision_data.get("credit_score"),
            "decision_rationale": decision_data.get("decision_rationale"),
            "factors_considered": decision_data.get("factors_considered", []),
        }

        self.audit_trail.append(record)
        logger.info(f"Audit record created: {record['case_id']}")
        return record

    def get_notification_history(
        self, applicant_id: str = None
    ) -> List[Dict[str, Any]]:
        """Get notification history."""
        if applicant_id:
            return [
                n
                for n in self.notifications_log
                if n.get("applicant_id") == applicant_id
            ]
        return self.notifications_log

    def get_audit_trail(self, applicant_id: str = None) -> List[Dict[str, Any]]:
        """Get audit trail."""
        if applicant_id:
            return [
                a for a in self.audit_trail if a.get("applicant_id") == applicant_id
            ]
        return self.audit_trail

    def _log_audit(
        self, applicant_id: str, action: str, data: Dict = None
    ) -> None:
        """Log action for audit purposes."""
        audit_entry = {
            "applicant_id": applicant_id,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }
        self.audit_trail.append(audit_entry)
        logger.info(f"Audit logged: {action} for {applicant_id}")

    def send_escalation_notification(self, notification_data: Dict) -> bool:
        """Send escalation notification to underwriting team."""
        message = {
            "type": "escalation",
            "case_id": notification_data.get("case_id"),
            "applicant_id": notification_data.get("applicant_id"),
            "timestamp": datetime.now().isoformat(),
            "priority": notification_data.get("priority", "Medium"),
            "reason": notification_data.get("reason", "Manual review required"),
            "recipient": "underwriting_team",
        }

        self.notifications_log.append(message)
        logger.info(f"Escalation notification sent: {message}")
        return True

    def generate_compliance_report(
        self, start_date: str = None, end_date: str = None
    ) -> Dict[str, Any]:
        """Generate compliance report."""
        decisions = {}
        for entry in self.audit_trail:
            decision = entry.get("data", {}).get("decision", "Unknown")
            decisions[decision] = decisions.get(decision, 0) + 1

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_applications": len(self.audit_trail),
            "decision_summary": decisions,
            "approval_rate": (
                decisions.get("Approve", 0) / len(self.audit_trail)
                if self.audit_trail
                else 0
            ),
            "rejection_rate": (
                decisions.get("Reject", 0) / len(self.audit_trail)
                if self.audit_trail
                else 0
            ),
            "review_rate": (
                decisions.get("Review", 0) / len(self.audit_trail)
                if self.audit_trail
                else 0
            ),
        }
        return report

    def create_case_file(self, case_data: Dict) -> Dict[str, Any]:
        """Create and store case file."""
        case_file = {
            "case_id": case_data.get("case_id"),
            "applicant_id": case_data.get("applicant_id"),
            "created_at": datetime.now().isoformat(),
            "status": "Active",
            "documents": [],
            "notes": [],
            "assigned_to": None,
        }
        logger.info(f"Case file created: {case_file['case_id']}")
        return case_file

    def add_case_note(
        self, case_id: str, note: str, created_by: str = "System"
    ) -> bool:
        """Add note to case file."""
        note_entry = {
            "timestamp": datetime.now().isoformat(),
            "note": note,
            "created_by": created_by,
        }
        logger.info(f"Case note added to {case_id}: {note}")
        return True
