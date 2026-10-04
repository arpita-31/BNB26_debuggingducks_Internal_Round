"""
Verification script checking FastAPI app, static files mount, Auth, Teacher, and n8n routes
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from fastapi.testclient import TestClient
from app.main import app

def verify_all():
    print("Testing ReLearn FastAPI Application...")
    with TestClient(app) as client:
        # 1. Health check
        res_health = client.get("/api/health")
        assert res_health.status_code == 200
        print("[PASS] /api/health:", res_health.json())

        # 2. Static root index.html
        res_root = client.get("/")
        assert res_root.status_code == 200
        assert "ReLearn" in res_root.text
        print(f"[PASS] / (index.html, length: {len(res_root.text)} bytes)")

        # 3. Model metrics
        res_metrics = client.get("/api/model/metrics")
        assert res_metrics.status_code == 200
        m = res_metrics.json()["test_metrics"]
        print(f"[PASS] /api/model/metrics (Accuracy: {m['accuracy']*100:.2f}%, Macro F1: {m['macro_f1']:.4f})")

        # 4. Questions
        res_q = client.get("/api/questions")
        assert res_q.status_code == 200
        print(f"[PASS] /api/questions ({len(res_q.json())} questions)")

        # 5. Demo Scenarios
        res_demo = client.get("/api/demo/scenarios")
        assert res_demo.status_code == 200
        print(f"[PASS] /api/demo/scenarios ({len(res_demo.json())} scenarios)")

        # 6. Auth Login (Student & Teacher)
        login_student = client.post("/api/auth/login", json={
            "email": "student@relearn.ai",
            "password": "password123"
        })
        assert login_student.status_code == 200, login_student.text
        token_s = login_student.json()["access_token"]
        print(f"[PASS] /api/auth/login (Student: {login_student.json()['user']['full_name']}, Role: {login_student.json()['user']['role']})")

        login_teacher = client.post("/api/auth/login", json={
            "email": "teacher@relearn.ai",
            "password": "password123"
        })
        assert login_teacher.status_code == 200, login_teacher.text
        print(f"[PASS] /api/auth/login (Teacher: {login_teacher.json()['user']['full_name']}, Role: {login_teacher.json()['user']['role']})")

        # 7. Teacher Analytics
        res_teacher = client.get("/api/teacher/analytics")
        assert res_teacher.status_code == 200
        t_data = res_teacher.json()
        print(f"[PASS] /api/teacher/analytics (Students: {t_data['total_students']}, Avg Mastery: {t_data['average_mastery']}%, Top Misconception: {t_data['most_common_misconception']['name']})")

        # 8. Teacher Question Creation
        new_q_res = client.post("/api/teacher/questions", json={
            "subject": "Programming",
            "topic": "Python Functions",
            "concept": "variable_scope",
            "target_misconception_id": "M004",
            "difficulty": "intermediate",
            "title": "Local vs Global Scope Verification",
            "prompt": "What does this code output?",
            "code": "x = 5\ndef f():\n    x = 10\nf()\nprint(x)",
            "expected_output": "5",
            "question_type": "output_prediction",
            "explanation": "Assigning x = 10 inside f() creates a local variable shadowing x."
        })
        assert new_q_res.status_code == 200
        print(f"[PASS] /api/teacher/questions (Created: {new_q_res.json()['question']['id']} - {new_q_res.json()['question']['title']})")

        # 9. n8n Orchestration Pipeline
        n8n_res = client.post("/api/n8n/orchestrate", json={
            "learner_id": "demo_learner",
            "question_id": "Q_PY_RANGE_01",
            "response": "1 2 3 4 5 because 5 is the stopping bound and included",
            "response_type": "text",
            "domain_id": "python_programming"
        })
        assert n8n_res.status_code == 200
        n_data = n8n_res.json()
        print(f"[PASS] /api/n8n/orchestrate (Steps executed: {len(n_data['workflow_execution']['steps'])}, Next: {n_data['response']['next_action']})")

        # 10. Full closed-loop diagnosis simulation
        diag_res = client.post("/api/diagnose", json={
            "domain_id": "python_programming",
            "question_id": "Q_PY_RANGE_01",
            "learner_id": "demo_learner",
            "submission": {
                "modality": "text",
                "text": "1 2 3 4 5 because range(1, 5) includes 5",
                "code": ""
            }
        })
        assert diag_res.status_code == 200
        d_json = diag_res.json()
        print(f"[PASS] /api/diagnose (Diagnosed: {d_json['prediction']['misconception_id']} - {d_json['prediction']['name']}, Conf: {d_json['prediction']['confidence']*100:.1f}%)")

        # 11. Intervention
        interv_res = client.post("/api/intervention", json={
            "misconception_id": d_json['prediction']['misconception_id'],
            "confidence": d_json['prediction']['confidence']
        })
        assert interv_res.status_code == 200
        print(f"[PASS] /api/intervention ({len(interv_res.json()['stages'])} scaffold stages)")

        # 12. Unseen Reassessment & Resolution
        reassess_res = client.post("/api/reassess", json={
            "misconception_id": "M001"
        })
        assert reassess_res.status_code == 200
        q_trans_id = reassess_res.json()["question"]["id"]
        
        resolve_res = client.post("/api/resolve", json={
            "reassessment_id": q_trans_id,
            "misconception_id": "M001",
            "concept_id": "python_range",
            "learner_response": "2 3 4 5 because the upper bound 6 is excluded"
        })
        assert resolve_res.status_code == 200
        r_json = resolve_res.json()
        print(f"[PASS] /api/resolve (Resolution: {r_json['resolution_status']}, Mastery: {r_json['mastery_before']*100:.0f}% -> {r_json['mastery_after']*100:.0f}%)")

    print("\n==========================================")
    print("ALL 12 ENDPOINT VERIFICATIONS PASSED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    verify_all()
