# 🏦 Multi-Agent Agentic AI Loan Approval System

A production-ready, scalable loan approval system using multi-agent Agentic AI architecture with LangGraph orchestration, FastAPI backend, and Streamlit UI.

## 🎯 Business Objective

- **Automate** loan application analysis using Agentic AI
- **Improve** decision speed and consistency
- **Provide** explainable, auditable decisions
- **Adopt** a scalable, loosely coupled microservices architecture

## 📋 Table of Contents

- [Architecture](#-system-architecture)
- [Components](#-components)
- [Installation](#-installation)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Development](#-development)

## 🏗️ System Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│  Presentation Layer                      │
│  (Streamlit Chatbot UI)                 │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  Microservice Layer                      │
│  (FastAPI REST Endpoints)               │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  Orchestration Layer                     │
│  (LangGraph Engine)                     │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  Agent Layer (Domain-Specific)          │
│  • Applicant Profile Agent              │
│  • Financial Risk Agent                 │
│  • Loan Decision Agent                  │
│  • Compliance Agent                     │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  Communication Layer (MCP Servers)      │
│  • ApplicantDB                          │
│  • RiskRulesDB                          │
│  • DecisionSynthesis                    │
│  • NotificationSystem                   │
└─────────────────────────────────────────┘
```

## 🔧 Components

### 1. **Presentation Layer**
- **Streamlit-based UI** for loan application submission
- Real-time results display
- Application history & analytics dashboard
- JSON report download

### 2. **Microservice Layer**
- **FastAPI** REST endpoints
- Health checks and case status endpoints
- Compliance reporting endpoints

### 3. **Orchestration Layer**
- **LangGraph** state machine orchestration
- Sequential workflow: Profile → Risk → Decision → Compliance → Finalize
- State management and decision routing

### 4. **Agent Layer** (Domain-Specific)

#### Applicant Profile Agent
- Analyzes applicant demographics and employment
- Calculates income stability score
- Assesses employment risk level
- Generates credit history summary

#### Financial Risk Agent
- Calculates debt-to-income ratio
- Assesses credit score risk
- Evaluates loan amount risk
- Detects financial anomalies

#### Loan Decision Agent
- Synthesizes decision from all factors
- Calculates composite risk score
- Determines classification (Approve/Reject/Review)
- Provides explainable decision factors

#### Compliance & Action Orchestrator Agent
- Determines action based on decision
- Sends notifications to applicant
- Creates audit records
- Manages case lifecycle

### 5. **Communication Layer** (MCP Servers)

#### ApplicantDB Server
- Applicant profile retrieval
- Employment information lookup
- KYC verification
- Fraud indicators check

#### RiskRulesDB Server
- Debt-to-income calculation
- Credit score risk assessment
- Loan amount validation
- Fraud detection

#### DecisionSynthesis Server
- Policy violation checking
- Credit profile evaluation
- Decision confidence calculation
- Interest rate calculation

#### NotificationSystem Server
- Approval/Rejection notifications
- Escalation alerts
- Audit trail management
- Compliance reporting

## 💻 Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Anthropic API key

### Step 1: Clone/Setup Project

```bash
cd /path/to/loan-approval-system
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy and edit .env file
cp .env .env.local
# Edit .env.local with your Anthropic API key
export $(cat .env.local | xargs)
```

Edit `.env` with your configuration:
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
LOG_LEVEL=INFO
ENV=development
```

## 🚀 Getting Started

### Option 1: Start Both Services (Recommended)

```bash
chmod +x start_services.sh
./start_services.sh
```

This will:
- Start FastAPI backend on `http://127.0.0.1:8000`
- Start Streamlit UI on `http://127.0.0.1:8501`

### Option 2: Start Services Separately

**Terminal 1 - Start Backend:**
```bash
chmod +x start_backend.sh
./start_backend.sh
```

**Terminal 2 - Start UI:**
```bash
chmod +x start_ui.sh
./start_ui.sh
```

### Option 3: Manual Start

**Backend:**
```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

**UI:**
```bash
streamlit run ui/chatbot.py
```

## 📖 Usage

### Web Interface

1. Open browser: `http://127.0.0.1:8501`
2. Fill loan application form:
   - Applicant ID (auto-generated)
   - Age, Income, Employment Type
   - Credit Score
   - Loan Amount & Tenure
   - Existing Liabilities
   - Location

3. Click "Analyze Application"

4. View results:
   - **Decision**: Approve/Reject/Review
   - **Risk Score**: Composite risk (0-100%)
   - **Applicant Profile**: Income stability, employment risk
   - **Financial Risk**: DTI, credit score risk, anomalies
   - **Loan Decision**: Key factors, explanation
   - **Compliance**: Action taken, notifications

### API Endpoints

#### Submit Application for Analysis
```bash
curl -X POST http://127.0.0.1:8000/analyze-application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP001",
    "age": 35,
    "income": 85000,
    "employment_type": "Salaried",
    "credit_score": 750,
    "loan_amount": 200000,
    "loan_tenure_months": 60,
    "existing_liabilities": 30000,
    "location": "New York"
  }'
```

#### Check API Health
```bash
curl http://127.0.0.1:8000/health
```

#### Get Case Status
```bash
curl http://127.0.0.1:8000/case/{case_id}
```

#### Get Compliance Report
```bash
curl http://127.0.0.1:8000/compliance-report
```

## 📚 API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📁 Project Structure

```
loan-approval-system/
├── backend/
│   ├── __init__.py
│   ├── app.py                    # FastAPI application
│   ├── config.py                 # Configuration management
│   ├── models.py                 # Pydantic models
│   └── orchestration/
│       ├── __init__.py
│       ├── state.py              # LangGraph state definition
│       └── orchestrator.py       # LangGraph orchestration engine
├── agents/
│   ├── __init__.py
│   ├── applicant_profile_agent.py
│   ├── financial_risk_agent.py
│   ├── loan_decision_agent.py
│   └── compliance_agent.py
├── mcp_servers/
│   ├── __init__.py
│   ├── applicant_db.py           # ApplicantDB MCP server
│   ├── risk_rules_db.py          # RiskRulesDB MCP server
│   ├── decision_synthesis.py     # DecisionSynthesis MCP server
│   └── notification_system.py    # NotificationSystem MCP server
├── ui/
│   ├── __init__.py
│   └── chatbot.py                # Streamlit chatbot interface
├── utils/
│   ├── __init__.py
│   └── logger.py                 # Logging configuration
├── data/
│   └── sample_applications.json  # Sample test data
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
├── start_services.sh             # Start all services
├── start_backend.sh              # Start backend only
├── start_ui.sh                   # Start UI only
├── README.md                     # This file
└── logs/                         # Application logs (auto-created)
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Backend Configuration
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000

# Logging
LOG_LEVEL=INFO

# Environment
ENV=development
```

### Customization

#### Modify Risk Thresholds
Edit `mcp_servers/risk_rules_db.py`:
```python
"dti_acceptable": 0.43,
"dti_caution": 0.50,
"credit_score_excellent": 750,
```

#### Adjust Decision Logic
Edit `agents/loan_decision_agent.py`:
```python
def determine_classification(...):
    # Customize decision rules
```

#### Update Notification Templates
Edit `mcp_servers/notification_system.py`:
```python
def send_approval_notification(...):
    # Customize message
```

## 🧪 Testing

### Test with Sample Application

Use the sample applications in `data/sample_applications.json`:

```bash
# Terminal 1: Start backend
./start_backend.sh

# Terminal 2: Test API
python -c "
import requests
import json

with open('data/sample_applications.json') as f:
    data = json.load(f)
    app = data['sample_applications'][0]
    
    response = requests.post(
        'http://127.0.0.1:8000/analyze-application',
        json=app
    )
    print(json.dumps(response.json(), indent=2))
"
```

### Run with Streamlit

```bash
streamlit run ui/chatbot.py
```

Then use the web interface to submit applications.

## 📊 Output Example

```json
{
  "case_id": "abc-123-def",
  "applicant_id": "APP001",
  "decision": "Approve",
  "risk_score": 0.35,
  "confidence_level": 0.85,
  "applicant_profile": {
    "income_stability_score": 0.80,
    "employment_risk": "Low",
    "credit_history_summary": "Total accounts: 4; Active accounts: 3",
    "application_completeness": true,
    "missing_fields": []
  },
  "financial_risk": {
    "debt_to_income_ratio": 0.28,
    "credit_score_risk_level": "Low",
    "loan_amount_risk": "Low",
    "anomaly_detected": false,
    "anomaly_details": "No anomalies detected",
    "reasoning": "DTI: 28%; Credit risk: Low; Loan risk: Low"
  },
  "loan_decision": {
    "classification": "Approve",
    "risk_score": 0.35,
    "confidence_level": 0.85,
    "key_decision_factors": [
      "Good credit score",
      "Stable employment",
      "Low debt-to-income ratio",
      "Strong income stability"
    ],
    "explanation": "Decision: Approve. Risk Score: 35%. Application meets lending criteria."
  },
  "compliance_status": {
    "action_taken": "Issue approval letter and proceed with disbursement",
    "notification_sent": true,
    "case_id": "abc-123-def",
    "timestamp": "2024-03-15T10:30:00",
    "summary": "Decision: Approve. Action: Proceed. Notification: Sent."
  },
  "timestamp": "2024-03-15T10:30:00"
}
```

## 🔐 Security Considerations

- Sensitive data (API keys) stored in `.env` (not version controlled)
- Input validation on all endpoints
- CORS enabled for development (modify for production)
- Audit trail for compliance
- Error handling without exposing system details

## 🚀 Production Deployment

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t loan-approval .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=xxx loan-approval
```

### Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests.

### Environment Hardening

- Use `.env.production` with secure values
- Enable HTTPS/TLS
- Restrict CORS origins
- Implement rate limiting
- Add authentication for API endpoints

## 📈 Monitoring & Logging

Logs are saved to `logs/loan_approval.log`:

```bash
tail -f logs/loan_approval.log
```

Key metrics to monitor:
- Application processing time
- Decision distribution (Approve/Reject/Review)
- Error rates
- API response times

## 🐛 Troubleshooting

### Issue: "Cannot connect to API"
- Ensure backend is running: `./start_backend.sh`
- Check backend logs: `tail -f logs/loan_approval.log`
- Verify port 8000 is not in use: `lsof -i :8000`

### Issue: "ANTHROPIC_API_KEY not found"
- Set in `.env`: `ANTHROPIC_API_KEY=your_key`
- Export: `export ANTHROPIC_API_KEY=your_key`
- Verify: `echo $ANTHROPIC_API_KEY`

### Issue: Slow response times
- Check network connectivity
- Review API logs for bottlenecks
- Verify model selection in `config.py`

## 📝 Development

### Add New Agent

1. Create file: `agents/new_agent.py`
2. Implement agent function
3. Add to orchestrator workflow
4. Update models if needed

### Extend MCP Servers

1. Edit corresponding file in `mcp_servers/`
2. Add new methods
3. Update agents that use it

### Modify Decision Logic

Edit decision thresholds in:
- `agents/loan_decision_agent.py`
- `mcp_servers/risk_rules_db.py`

## 📞 Support

For issues or questions:
1. Check logs: `logs/loan_approval.log`
2. Review API docs: `http://127.0.0.1:8000/docs`
3. Check sample applications: `data/sample_applications.json`

## 📜 License

Proprietary - For authorized evaluation only

## 🙏 Acknowledgments

- Built with **LangGraph** for orchestration
- Powered by **Anthropic Claude** AI
- UI built with **Streamlit**
- Backend powered by **FastAPI**

---

**Version**: 1.0.0  
**Last Updated**: 2024-03-15  
**Status**: Production Ready ✅
