import logging
import uuid
from datetime import datetime
from typing import Dict, Any
from mcp_servers.notification_system import NotificationSystemServer

logger = logging.getLogger(__name__)


def execute_compliance_action(state: Dict[str, Any]) -> Dict[str, Any]:
    """Execute compliance action based on decision."""
    logger.info(f"Executing compliance action for {state['applicant_id']}")

    # notification_server = NotificationSystemServer()

    decision = state.get("final_decision", "Review")

    case_id = state.get("case_id", str(uuid.uuid4()))

    action_taken = determine_action(decision)

    notification_data = {
        "applicant_id": state["applicant_id"],
        "decision": decision,
        "case_id": case_id,
        "timestamp": datetime.now().isoformat(),
        "risk_score": state.get("risk_score", 0),
        "credit_score": state.get("credit_score", 0),
    }

    notification_sent = send_notification(notification_data, decision)

    summary = generate_compliance_summary(
        decision, action_taken, case_id, notification_sent
    )

    result = {
        "action_taken": action_taken,
        "notification_sent": notification_sent,
        "case_id": case_id,
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
    }

    logger.info(f"Compliance action executed: {result}")
    return result


def determine_action(decision: str) -> str:
    """Determine compliance action based on decision."""
    action_map = {
        "Approve": "Issue approval letter and proceed with disbursement",
        "Reject": "Send rejection letter with reason and appeal instructions",
        "Review": "Escalate to manual review queue for underwriter assessment",
    }
    return action_map.get(decision, "Administrative hold pending clarification")


def send_notification(notification_data: dict, decision: str) -> bool:
    """Send notification to applicant and internal teams."""
    try:
        if decision == "Approve":
            return send_approval_notification(notification_data)
        elif decision == "Reject":
            return send_rejection_notification(notification_data)
        else:
            return send_review_notification(notification_data)
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return False


def send_approval_notification(notification_data: dict) -> bool:
    """Send approval notification."""
    message = f"""
    Dear Applicant {notification_data['applicant_id']},

    Congratulations! Your loan application (Case #{notification_data['case_id']}) has been approved.

    Our team will contact you shortly with the next steps.

    Best regards,
    Loan Approval System
    """
    logger.info(f"Approval notification sent: {message}")
    return True


def send_rejection_notification(notification_data: dict) -> bool:
    """Send rejection notification."""
    message = f"""
    Dear Applicant {notification_data['applicant_id']},

    Your loan application (Case #{notification_data['case_id']}) has been reviewed and unfortunately cannot be approved at this time.

    Please contact us for more information.

    Best regards,
    Loan Approval System
    """
    logger.info(f"Rejection notification sent: {message}")
    return True


def send_review_notification(notification_data: dict) -> bool:
    """Send review notification."""
    message = f"""
    Dear Applicant {notification_data['applicant_id']},

    Your loan application (Case #{notification_data['case_id']}) has been received and is under review.

    Our underwriting team will assess your application and contact you within 3-5 business days.

    Best regards,
    Loan Approval System
    """
    logger.info(f"Review notification sent: {message}")
    return True


def generate_compliance_summary(
    decision: str, action_taken: str, case_id: str, notification_sent: bool
) -> str:
    """Generate compliance summary."""
    summary = f"Decision: {decision}. "
    summary += f"Action: {action_taken}. "
    summary += f"Case ID: {case_id}. "
    summary += f"Notification: {'Sent' if notification_sent else 'Pending'}."
    return summary
