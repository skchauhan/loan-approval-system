"""FastAPI microservice for loan approval system."""

import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.config import config
from backend.models import (
    LoanApplicationRequest,
    FinalDecisionResponse,
    ApplicantProfileResponse,
    FinancialRiskResponse,
    LoanDecisionResponse,
    ComplianceResponse,
)
from backend.orchestration.orchestrator import LoanApprovalOrchestrator

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Loan Approval System",
    description="Multi-Agent Agentic AI Loan Approval System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = LoanApprovalOrchestrator()


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Loan Approval System",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "loan-approval-microservice",
        "environment": config.ENV,
    }


@app.post("/analyze-application", tags=["Loan Analysis"])
async def analyze_application(
    request: LoanApplicationRequest,
) -> FinalDecisionResponse:
    """
    Analyze loan application through multi-agent orchestration.

    Args:
        request: Loan application data

    Returns:
        Final decision with detailed analysis
    """
    try:
        logger.info(f"Received application for {request.applicant_id}")

        application_data = {
            "applicant_id": request.applicant_id,
            "age": request.age,
            "income": request.income,
            "employment_type": request.employment_type,
            "credit_score": request.credit_score,
            "loan_amount": request.loan_amount,
            "loan_tenure_months": request.loan_tenure_months,
            "existing_liabilities": request.existing_liabilities,
            "location": request.location,
        }

        result = orchestrator.invoke(application_data)

        response = FinalDecisionResponse(
            case_id=result.get("case_id", ""),
            applicant_id=result.get("applicant_id", ""),
            decision=result.get("final_decision", "Review"),
            risk_score=result.get("risk_score", 0.5),
            confidence_level=result.get("confidence_level", 0.5),
            applicant_profile=ApplicantProfileResponse(
                **result.get("applicant_profile", {})
            ),
            financial_risk=FinancialRiskResponse(
                **result.get("financial_risk", {})
            ),
            loan_decision=LoanDecisionResponse(**result.get("loan_decision", {})),
            compliance_status=ComplianceResponse(
                **result.get("compliance_status", {})
            ),
            timestamp=datetime.now(),
        )

        logger.info(f"Analysis complete for {request.applicant_id}: {response.decision}")
        return response

    except Exception as e:
        logger.error(f"Error analyzing application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/case/{case_id}", tags=["Case Status"])
async def get_case_status(case_id: str):
    """Get status of a specific case."""
    try:
        return {
            "case_id": case_id,
            "status": "Processing",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error retrieving case: {str(e)}")
        raise HTTPException(status_code=404, detail="Case not found")


@app.get("/compliance-report", tags=["Reports"])
async def get_compliance_report():
    """Get compliance report."""
    try:
        return {
            "report_date": datetime.now().isoformat(),
            "total_applications": 0,
            "approval_rate": 0.0,
            "rejection_rate": 0.0,
            "review_rate": 0.0,
        }
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=config.FASTAPI_HOST,
        port=config.FASTAPI_PORT,
    )
