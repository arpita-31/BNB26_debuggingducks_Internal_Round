# Re:Learn — n8n Orchestration Workflow Guide

This directory contains the production-ready n8n orchestration workflow definition for **Re:Learn**.

---

## 1. Architectural Philosophy: Orchestration vs ML Core

In Re:Learn, **n8n acts strictly as an orchestration, routing, and lifecycle coordinator**, while the core machine learning inference, AST analysis, and probability calibration reside directly inside the FastAPI backend.

This ensures:
1. The machine learning pipeline operates with sub-10ms latency directly in Python.
2. The system functions deterministically and offline even if n8n is paused or restarting.
3. n8n coordinates webhooks, external notifications, cross-service calls, and learner state persistence.

---

## 2. Webhook Configuration

- **Webhook URL (Local)**: `http://localhost:5678/webhook/relearn-answer`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`

### Expected Request Payload
```json
{
  "learner_id": "user_001",
  "question_id": "Q_PY_RANGE_01",
  "response": "range(1, 5) produces 1 2 3 4 5 because the upper bound 5 is included",
  "response_type": "text",
  "domain_id": "python_programming"
}
```

### Expected Response Payload
```json
{
  "status": "success",
  "orchestrator": "n8n / ReLearn Engine",
  "timestamp": "2026-10-04T09:30:00Z",
  "workflow_execution": {
    "execution_id": "exec_20261004093000",
    "steps": [
      "1. Webhook Payload Ingested & Schema Validated",
      "2. ML Misconception Diagnosis Executed (Predicted: M001)",
      "3. Confidence Calibration Check (80.7% vs 60.0% threshold)",
      "4. Fetched Targeted Intervention: 'Visual Interval Model for Python range()'",
      "5. Persistent Learner State Updated (Misconception M001: ACTIVE)",
      "6. Curriculum Recommendation Engine Triggered"
    ]
  },
  "response": {
    "correct": false,
    "misconception_id": "M001",
    "misconception_name": "Range Upper-Bound Inclusion",
    "confidence": 0.8071,
    "intervention_id": "I_M001",
    "intervention_title": "Visual Interval Model for Python range()",
    "next_action": "take_intervention"
  }
}
```

---

## 3. Required Environment Variables

When deploying n8n, configure these environment variables:

| Variable | Description | Example / Default |
|---|---|---|
| `RELEARN_BACKEND_URL` | Base URL of the FastAPI ReLearn backend | `http://localhost:8000` |
| `N8N_PORT` | Port for the n8n instance | `5678` |
| `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS` | Security setting | `true` |

---

## 4. How to Import the Workflow into n8n

1. Start your local n8n instance:
   ```bash
   npx n8n
   # or with docker
   docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
   ```
2. Open `http://localhost:5678` in your browser.
3. Click **Workflows** → **Add Workflow**.
4. In the top-right menu, select **Import from File...** and choose:
   `n8n/relearn_orchestration_workflow.json`
5. Click **Activate Workflow**.

---

## 5. Testing Without External n8n (FastAPI Orchestration Fallback)

To ensure competition judges can test the orchestration pipeline even without installing n8n:
The FastAPI backend exposes the identical orchestration route at:
`POST /api/n8n/orchestrate`

### Quick Test via cURL
```bash
curl -X POST http://localhost:8000/api/n8n/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "learner_id": "demo_learner",
    "question_id": "Q_PY_RANGE_01",
    "response": "1 2 3 4 5 because 5 is the stopping point so it gets printed",
    "response_type": "text"
  }'
```
