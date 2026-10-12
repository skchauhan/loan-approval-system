# 🚀 Deployment Guide

Complete guide for deploying the Loan Approval System to production environments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [AWS Deployment](#aws-deployment)
- [Monitoring & Maintenance](#monitoring--maintenance)

## Local Development

### Prerequisites

```bash
python --version  # 3.8+
pip --version     # 22.0+
```

### Setup

```bash
# Clone repository
cd loan-approval-system

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env .env.local
# Edit .env.local with your settings

# Start services
./start_services.sh
```

### Access Points

- **API**: http://127.0.0.1:8000
- **Docs**: http://127.0.0.1:8000/docs
- **UI**: http://127.0.0.1:8501

## Docker Deployment

### Build Docker Image

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command (backend)
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t loan-approval:latest .

# Run backend
docker run -d \
  --name loan-approval-backend \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-xxxxx \
  -v $(pwd)/logs:/app/logs \
  loan-approval:latest

# Run UI (requires backend)
docker run -d \
  --name loan-approval-ui \
  -p 8501:8501 \
  --link loan-approval-backend \
  -e API_BASE_URL=http://loan-approval-backend:8000 \
  loan-approval:latest \
  streamlit run ui/chatbot.py --server.address=0.0.0.0
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      LOG_LEVEL: INFO
      ENV: production
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  ui:
    build: .
    ports:
      - "8501:8501"
    command: streamlit run ui/chatbot.py --server.address=0.0.0.0
    environment:
      API_BASE_URL: http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - backend
      - ui
    restart: unless-stopped
```

Deploy with Docker Compose:

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Docker image pushed to registry

### Manifests

Create `k8s/deployment.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: loan-approval-config
data:
  LOG_LEVEL: "INFO"
  ENV: "production"
---
apiVersion: v1
kind: Secret
metadata:
  name: loan-approval-secrets
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "sk-ant-xxxxx"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-approval-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: loan-approval-backend
  template:
    metadata:
      labels:
        app: loan-approval-backend
    spec:
      containers:
      - name: backend
        image: your-registry/loan-approval:latest
        ports:
        - containerPort: 8000
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: loan-approval-secrets
              key: ANTHROPIC_API_KEY
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: loan-approval-config
              key: LOG_LEVEL
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: loan-approval-backend-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: loan-approval-backend
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-approval-ui
spec:
  replicas: 1
  selector:
    matchLabels:
      app: loan-approval-ui
  template:
    metadata:
      labels:
        app: loan-approval-ui
    spec:
      containers:
      - name: ui
        image: your-registry/loan-approval:latest
        command: ["streamlit", "run", "ui/chatbot.py", "--server.address=0.0.0.0"]
        ports:
        - containerPort: 8501
        env:
        - name: API_BASE_URL
          value: "http://loan-approval-backend-service:80"
---
apiVersion: v1
kind: Service
metadata:
  name: loan-approval-ui-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8501
  selector:
    app: loan-approval-ui
```

Deploy:

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get deployments
kubectl get services

# View logs
kubectl logs -f deployment/loan-approval-backend

# Scale replicas
kubectl scale deployment loan-approval-backend --replicas=3
```

## AWS Deployment

### Using ECS (Elastic Container Service)

1. **Push image to ECR**:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker build -t loan-approval .
docker tag loan-approval:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/loan-approval:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/loan-approval:latest
```

2. **Create ECS Task Definition** in AWS Console or CLI

3. **Create ECS Service** with ALB for load balancing

### Using Lambda + API Gateway

1. **Package for Lambda**:
```bash
pip install -r requirements.txt -t package/
cp -r backend agents mcp_servers package/
cd package && zip -r ../lambda-deployment.zip . && cd ..
```

2. **Upload to Lambda** and configure API Gateway

3. **Set environment variables** in Lambda console

## Monitoring & Maintenance

### Health Checks

```bash
# Check backend health
curl http://your-domain:8000/health

# Check API responsiveness
curl -X POST http://your-domain:8000/analyze-application \
  -H "Content-Type: application/json" \
  -d '{"applicant_id":"TEST001",...}'
```

### Logging & Metrics

```bash
# View application logs
tail -f logs/loan_approval.log

# Monitor system resources
docker stats loan-approval-backend

# Export logs to monitoring system
# Configure in backend/app.py for CloudWatch, DataDog, etc.
```

### Backup & Recovery

```bash
# Backup application data
tar -czf backup-$(date +%Y%m%d).tar.gz logs/ data/

# Restore from backup
tar -xzf backup-20240315.tar.gz
```

### Updates & Rollout

```bash
# Zero-downtime deployment
kubectl set image deployment/loan-approval-backend \
  backend=your-registry/loan-approval:v2.0 \
  --record

# Rollback if needed
kubectl rollout undo deployment/loan-approval-backend
```

## Production Checklist

- [ ] API key stored securely (not in code)
- [ ] HTTPS/TLS enabled
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Authentication added for sensitive endpoints
- [ ] Database backups configured
- [ ] Monitoring & alerting setup
- [ ] Log aggregation configured
- [ ] Disaster recovery plan documented
- [ ] Security scanning enabled
- [ ] Performance optimization done
- [ ] Load testing completed

---

**Last Updated**: 2024-03-15
