import logging
import uuid
from datetime import datetime
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from backend.orchestration.state import ApplicationState
from agents.applicant_profile_agent import analyze_applicant_profile
from agents.financial_risk_agent import analyze_financial_risk
from agents.loan_decision_agent import make_loan_decision
from agents.compliance_agent import execute_compliance_action

logger = logging.getLogger(__name__)


class LoanApprovalOrchestrator:
    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(ApplicationState)

        graph.add_node("profile_analysis", self._profile_analysis_node)
        graph.add_node("risk_analysis", self._risk_analysis_node)
        graph.add_node("decision", self._decision_node)
        graph.add_node("compliance", self._compliance_node)
        graph.add_node("finalize", self._finalize_node)

        graph.set_entry_point("profile_analysis")
        graph.add_edge("profile_analysis", "risk_analysis")
        graph.add_edge("risk_analysis", "decision")
        graph.add_edge("decision", "compliance")
        graph.add_edge("compliance", "finalize")
        graph.add_edge("finalize", END)

        return graph.compile()

    @staticmethod
    def _profile_analysis_node(state: ApplicationState) -> Dict[str, Any]:
        logger.info(f"Analyzing applicant profile for {state['applicant_id']}")
        profile_result = analyze_applicant_profile(state)
        return {"applicant_profile": profile_result}

    @staticmethod
    def _risk_analysis_node(state: ApplicationState) -> Dict[str, Any]:
        logger.info(f"Performing financial risk analysis for {state['applicant_id']}")
        risk_result = analyze_financial_risk(state)
        return {"financial_risk": risk_result}

    @staticmethod
    def _decision_node(state: ApplicationState) -> Dict[str, Any]:
        logger.info(f"Making loan decision for {state['applicant_id']}")
        decision_result = make_loan_decision(state)
        return {
            "loan_decision": decision_result,
            "final_decision": decision_result.get("classification"),
            "risk_score": decision_result.get("risk_score"),
            "confidence_level": decision_result.get("confidence_level"),
        }

    @staticmethod
    def _compliance_node(state: ApplicationState) -> Dict[str, Any]:
        logger.info(f"Executing compliance action for {state['applicant_id']}")
        compliance_result = execute_compliance_action(state)
        return {"compliance_status": compliance_result}

    @staticmethod
    def _finalize_node(state: ApplicationState) -> Dict[str, Any]:
        logger.info(f"Finalizing decision for {state['applicant_id']}")
        return {
            "decision_rationale": (
                f"Decision: {state['final_decision']}. "
                f"Risk Score: {state['risk_score']:.2f}. "
                f"Confidence: {state['confidence_level']:.2%}"
            )
        }

    def invoke(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        case_id = str(uuid.uuid4())
        state: ApplicationState = {
            "applicant_id": application_data["applicant_id"],
            "age": application_data["age"],
            "income": application_data["income"],
            "employment_type": application_data["employment_type"],
            "credit_score": application_data["credit_score"],
            "loan_amount": application_data["loan_amount"],
            "loan_tenure_months": application_data["loan_tenure_months"],
            "existing_liabilities": application_data["existing_liabilities"],
            "location": application_data["location"],
            "timestamp": datetime.now().isoformat(),
            "case_id": case_id,
            "applicant_profile": None,
            "financial_risk": None,
            "loan_decision": None,
            "compliance_status": None,
            "final_decision": None,
            "risk_score": None,
            "confidence_level": None,
            "decision_rationale": None,
            "errors": [],
        }

        result = self.graph.invoke(state)
        return result
