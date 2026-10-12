# ⚡ Quick Start Guide

Get the Loan Approval System running in 5 minutes!

## Prerequisites

- Python 3.8+
- pip
- Anthropic API key

## Installation (2 minutes)

### Step 1: Setup Environment

```bash
# Navigate to project directory
cd loan-approval-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## Start Services (1 minute)

### Option A: Start Everything at Once

```bash
chmod +x start_services.sh
./start_services.sh
```

Then open:
- **UI**: http://127.0.0.1:8501
- **API**: http://127.0.0.1:8000

### Option B: Start Separately

**Terminal 1** - Backend:
```bash
./start_backend.sh
# Or: python -m uvicorn backend.app:app --reload
```

**Terminal 2** - UI:
```bash
./start_ui.sh
# Or: streamlit run ui/chatbot.py
```

## Test the System (2 minutes)

### Via Web UI

1. Open http://127.0.0.1:8501
2. Fill in the form:
   - Age: 35
   - Income: 100,000
   - Employment: Salaried
   - Credit Score: 750
   - Loan Amount: 200,000
   - Tenure: 60 months
   - Liabilities: 30,000
   - Location: New York
3. Click "Analyze Application"
4. View results!

### Via API

```bash
curl -X POST http://127.0.0.1:8000/analyze-application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST001",
    "age": 35,
    "income": 100000,
    "employment_type": "Salaried",
    "credit_score": 750,
    "loan_amount": 200000,
    "loan_tenure_months": 60,
    "existing_liabilities": 30000,
    "location": "New York"
  }'
```

## Understanding Results

### Decision Types

- **Approve** ✅ - Application approved, ready for disbursement
- **Reject** ❌ - Application rejected (doesn't meet criteria)
- **Review** 📋 - Requires manual review by underwriter

### Risk Score

- **0-30%** - Low risk (likely approve)
- **30-50%** - Moderate risk (may review)
- **50-70%** - High risk (likely review/reject)
- **70%+** - Very high risk (likely reject)

### Confidence Level

- **80-100%** - High confidence in decision
- **60-80%** - Good confidence
- **<60%** - Low confidence (may need review)

## Sample Applications

Try these test cases:

### Test 1: Strong Applicant (Expected: Approve)
```json
{
  "age": 40,
  "income": 150000,
  "employment_type": "Government",
  "credit_score": 800,
  "loan_amount": 250000,
  "loan_tenure_months": 60,
  "existing_liabilities": 50000,
  "location": "New York"
}
```

### Test 2: Weak Applicant (Expected: Reject)
```json
{
  "age": 25,
  "income": 25000,
  "employment_type": "Freelancer",
  "credit_score": 550,
  "loan_amount": 400000,
  "loan_tenure_months": 120,
  "existing_liabilities": 100000,
  "location": "Unknown"
}
```

### Test 3: Average Applicant (Expected: Review)
```json
{
  "age": 32,
  "income": 60000,
  "employment_type": "Self-Employed",
  "credit_score": 680,
  "loan_amount": 200000,
  "loan_tenure_months": 84,
  "existing_liabilities": 80000,
  "location": "California"
}
```

## API Documentation

### Interactive Docs

Once backend is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Main Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/analyze-application` | Analyze loan application |
| GET | `/health` | Health check |
| GET | `/case/{case_id}` | Get case status |
| GET | `/compliance-report` | Get compliance report |

## Troubleshooting

### Can't connect to API
```bash
# Check if backend is running
curl http://127.0.0.1:8000/health

# If not, start backend
./start_backend.sh
```

### API key error
```bash
# Verify API key in .env
cat .env | grep ANTHROPIC_API_KEY

# Should see: ANTHROPIC_API_KEY=sk-ant-xxxxx

# If missing, update .env and restart
```

### Port already in use
```bash
# Backend port 8000
lsof -i :8000
kill -9 <PID>

# UI port 8501
lsof -i :8501
kill -9 <PID>
```

### Slow responses
- First request takes ~2-3 seconds (normal)
- Subsequent requests are faster
- Check logs: `tail -f logs/loan_approval.log`

## Next Steps

- 📚 Read [README.md](README.md) for full documentation
- 🏗️ See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- 🧪 Try [TESTING.md](TESTING.md) for advanced testing
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

## Key Features

✅ Multi-agent agentic AI orchestration  
✅ Real-time loan decision analysis  
✅ Explainable AI outputs  
✅ Production-ready architecture  
✅ RESTful API with interactive documentation  
✅ Streamlit web interface  
✅ Comprehensive audit trail  
✅ Scalable microservices design  

## Support

- API Docs: http://127.0.0.1:8000/docs
- Check logs: `logs/loan_approval.log`
- Review ARCHITECTURE.md for design details

---

**You're all set! 🚀**

The system is now running and ready to analyze loan applications using multi-agent agentic AI!
