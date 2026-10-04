"""
Integration tests for ReLearn FastAPI Endpoints
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_domains_and_questions():
    res_domains = client.get("/api/domains")
    assert res_domains.status_code == 200
    assert any(d["id"] == "python_programming" for d in res_domains.json())

    res_q = client.get("/api/questions")
    assert res_q.status_code == 200
    assert len(res_q.json()) >= 5

def test_diagnose_endpoint():
    payload = {
        "domain_id": "python_programming",
        "question_id": "Q_PY_RANGE_01",
        "learner_id": "test_learner",
        "submission": {
            "modality": "text+code",
            "text": "1 2 3 4 5 because 5 is the upper bound and included",
            "code": ""
        }
    }
    res = client.post("/api/diagnose", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["prediction"]["misconception_id"] == "M001"
    assert data["prediction"]["confidence"] > 0.5
    assert len(data["ranked_candidates"]) > 0

def test_intervention_and_reassessment_endpoints():
    # 1. Fetch intervention
    res_int = client.post("/api/intervention", json={"misconception_id": "M001"})
    assert res_int.status_code == 200
    assert res_int.json()["misconception_id"] == "M001"

    # 2. Fetch reassessment
    res_re = client.post("/api/reassess", json={"misconception_id": "M001"})
    assert res_re.status_code == 200
    assert res_re.json()["is_unseen"] is True

    # 3. Resolve
    q_id = res_re.json()["question"]["id"]
    res_res = client.post("/api/resolve", json={
        "reassessment_id": q_id,
        "misconception_id": "M001",
        "concept_id": "python_range",
        "learner_response": "2 3 4 5 because the upper bound 6 is excluded"
    })
    assert res_res.status_code == 200
    assert res_res.json()["is_resolved"] is True

def test_model_metrics_endpoints():
    res = client.get("/api/model/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert "test_metrics" in metrics
    assert metrics["test_metrics"]["accuracy"] > 0.70

    res_cm = client.get("/api/model/confusion-matrix")
    assert res_cm.status_code == 200
    assert "matrix" in res_cm.json()

def test_demo_scenarios_endpoint():
    res = client.get("/api/demo/scenarios")
    assert res.status_code == 200
    assert len(res.json()) == 5
