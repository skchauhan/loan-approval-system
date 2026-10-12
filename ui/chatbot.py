"""Streamlit-based chatbot UI for loan approval system."""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, Any

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        padding-top: 0rem;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

API_BASE_URL = "http://127.0.0.1:8000"


def init_session_state():
    """Initialize session state variables."""
    if "case_history" not in st.session_state:
        st.session_state.case_history = []
    if "current_case" not in st.session_state:
        st.session_state.current_case = None
    if "api_status" not in st.session_state:
        st.session_state.api_status = "unknown"


def check_api_health() -> bool:
    """Check if API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def submit_application(application_data: Dict[str, Any]) -> Dict[str, Any]:
    """Submit application to backend API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze-application",
            json=application_data,
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to API. Please ensure the FastAPI server is running on http://127.0.0.1:8000"
        )
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def display_decision_card(decision_data: Dict[str, Any]):
    """Display decision result in a formatted card."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Decision",
            decision_data.get("decision", "N/A"),
            delta=None,
            delta_color="normal",
        )

    with col2:
        risk_score = decision_data.get("risk_score", 0)
        st.metric("Risk Score", f"{risk_score:.2%}")

    with col3:
        confidence = decision_data.get("confidence_level", 0)
        st.metric("Confidence", f"{confidence:.2%}")

    st.divider()


def display_applicant_profile(profile_data: Dict[str, Any]):
    """Display applicant profile analysis."""
    st.subheader("📋 Applicant Profile")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Income Stability Score",
            f"{profile_data.get('income_stability_score', 0):.2%}",
        )
        st.metric(
            "Employment Risk", profile_data.get("employment_risk", "Unknown")
        )

    with col2:
        st.metric(
            "Application Complete",
            "✅ Yes" if profile_data.get("application_completeness") else "❌ No",
        )
        if profile_data.get("missing_fields"):
            st.warning(f"Missing Fields: {', '.join(profile_data['missing_fields'])}")

    st.info(f"Credit History: {profile_data.get('credit_history_summary', 'N/A')}")


def display_financial_risk(risk_data: Dict[str, Any]):
    """Display financial risk analysis."""
    st.subheader("💰 Financial Risk Analysis")
    col1, col2 = st.columns(2)

    with col1:
        dti = risk_data.get("debt_to_income_ratio", 0)
        st.metric("Debt-to-Income Ratio", f"{dti:.2%}")
        st.metric("Credit Score Risk", risk_data.get("credit_score_risk_level", "Unknown"))

    with col2:
        st.metric("Loan Amount Risk", risk_data.get("loan_amount_risk", "Unknown"))
        anomaly = risk_data.get("anomaly_detected", False)
        st.metric("Anomalies Detected", "⚠️ Yes" if anomaly else "✅ No")

    if risk_data.get("anomaly_details"):
        st.warning(f"Anomaly Details: {risk_data['anomaly_details']}")

    st.info(f"Analysis Reasoning: {risk_data.get('reasoning', 'N/A')}")


def display_loan_decision(decision_data: Dict[str, Any]):
    """Display loan decision details."""
    st.subheader("🎯 Loan Decision")

    key_factors = decision_data.get("key_decision_factors", [])
    if key_factors:
        st.write("**Key Decision Factors:**")
        for factor in key_factors:
            st.write(f"• {factor}")

    st.info(f"**Explanation:** {decision_data.get('explanation', 'N/A')}")


def display_compliance_status(compliance_data: Dict[str, Any]):
    """Display compliance status."""
    st.subheader("✅ Compliance & Action")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Case ID", compliance_data.get("case_id", "N/A")[:8] + "...")
        st.metric(
            "Notification Sent",
            "✅ Yes" if compliance_data.get("notification_sent") else "❌ No",
        )

    with col2:
        st.write(f"**Action Taken:** {compliance_data.get('action_taken', 'N/A')}")
        timestamp = compliance_data.get("timestamp", "N/A")
        st.write(f"**Timestamp:** {timestamp}")

    st.info(f"**Summary:** {compliance_data.get('summary', 'N/A')}")


def main():
    """Main Streamlit application."""
    init_session_state()

    st.title("🏦 Loan Approval System")
    st.markdown("### Multi-Agent Agentic AI Decision System")

    if not check_api_health():
        st.error(
            "⚠️ **API Server Not Connected**\n\n"
            "Please start the FastAPI server:\n"
            "```bash\npython -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload\n```"
        )
        return

    st.success("✅ API Server Connected")
    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["📝 New Application", "📊 View Results", "📈 Analytics"]
    )

    with tab1:
        st.subheader("Submit Loan Application")

        with st.form("loan_application_form"):
            col1, col2 = st.columns(2)

            with col1:
                applicant_id = st.text_input(
                    "Applicant ID",
                    value=f"APP{datetime.now().strftime('%Y%m%d%H%M%S')}",
                )
                age = st.number_input("Age", min_value=18, max_value=100, value=35)
                income = st.number_input(
                    "Annual Income ($)", min_value=0.0, value=75000.0
                )
                employment_type = st.selectbox(
                    "Employment Type",
                    [
                        "Salaried",
                        "Government",
                        "Self-Employed",
                        "Business",
                        "Freelancer",
                    ],
                )
                location = st.selectbox(
                    "Location",
                    ["New York", "California", "Texas", "Florida", "Other"],
                )

            with col2:
                credit_score = st.number_input(
                    "Credit Score", min_value=300, max_value=850, value=750
                )
                loan_amount = st.number_input(
                    "Loan Amount ($)", min_value=0.0, value=150000.0
                )
                loan_tenure_months = st.number_input(
                    "Loan Tenure (Months)", min_value=6, max_value=360, value=60
                )
                existing_liabilities = st.number_input(
                    "Existing Liabilities ($)", min_value=0.0, value=50000.0
                )

            submit_button = st.form_submit_button(
                "🚀 Analyze Application", use_container_width=True
            )

            if submit_button:
                with st.spinner("Analyzing application through multi-agent system..."):
                    application_data = {
                        "applicant_id": applicant_id,
                        "age": age,
                        "income": income,
                        "employment_type": employment_type,
                        "credit_score": credit_score,
                        "loan_amount": loan_amount,
                        "loan_tenure_months": loan_tenure_months,
                        "existing_liabilities": existing_liabilities,
                        "location": location,
                    }

                    result = submit_application(application_data)

                    if result:
                        st.session_state.current_case = result
                        st.session_state.case_history.append(result)

                        st.success("✅ Application Analyzed Successfully!")
                        # st.balloons()

    with tab2:
        st.subheader("Application Analysis Results")

        if st.session_state.current_case:
            case_data = st.session_state.current_case

            display_decision_card(case_data)

            col_profile, col_risk = st.columns(2)
            with col_profile:
                display_applicant_profile(case_data.get("applicant_profile", {}))

            with col_risk:
                display_financial_risk(case_data.get("financial_risk", {}))

            display_loan_decision(case_data.get("loan_decision", {}))
            display_compliance_status(case_data.get("compliance_status", {}))

            st.divider()

            if st.button("📥 Download Report (JSON)"):
                json_str = json.dumps(case_data, indent=2, default=str)
                st.download_button(
                    label="Download JSON Report",
                    data=json_str,
                    file_name=f"loan_report_{case_data.get('case_id', 'unknown')}.json",
                    mime="application/json",
                )

        else:
            st.info("📋 Submit an application to view results here.")

    with tab3:
        st.subheader("Application History & Analytics")

        if st.session_state.case_history:
            st.write(f"**Total Applications:** {len(st.session_state.case_history)}")

            decisions = {}
            for case in st.session_state.case_history:
                decision = case.get("decision", "Unknown")
                decisions[decision] = decisions.get(decision, 0) + 1

            if decisions:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Approved", decisions.get("Approve", 0))
                with col2:
                    st.metric("Rejected", decisions.get("Reject", 0))
                with col3:
                    st.metric("Under Review", decisions.get("Review", 0))

            st.bar_chart(decisions)

            st.subheader("Case History")
            for idx, case in enumerate(st.session_state.case_history, 1):
                with st.expander(
                    f"Case {idx}: {case.get('applicant_id')} - {case.get('decision')}"
                ):
                    st.json(case)

        else:
            st.info("📊 No applications submitted yet.")

    st.divider()
    st.markdown(
        """
        ---
        **Multi-Agent Agentic AI Loan Approval System**
        - 🤖 Powered by LangGraph & Claude AI
        - 🔄 Multi-agent orchestration with specialized domains
        - 📊 Real-time decision analysis
        - ✅ Explainable AI outputs
        """
    )


if __name__ == "__main__":
    main()
