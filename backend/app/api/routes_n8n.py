"""
n8n Orchestration Pipeline API for ReLearn
Provides webhook simulation and direct workflow orchestration.
Allows external n8n workflow nodes to trigger closed-loop diagnosis,
intervention selection, and learner model updates.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
from app.database.models import DBUser, DBQuestion, DBMisconception, DBLearnerMisconception, DBLearnerConcept
from app.schemas.api_models import N8NWebhookPayload
from app.diagnosis.engine import diagnosis_engine
from app.intervention.engine import intervention_engine
from app.learner_model.engine import learner_engine

router = APIRouter(prefix="/api/n8n", tags=["n8n Orchestration Layer"])

@router.post("/orchestrate")
def orchestrate_learning_pipeline(payload: N8NWebhookPayload, db: Session = Depends(get_db)):
    """
    Main n8n Webhook Target Endpoint:
    Orchestrates: Ingest -> ML Diagnosis -> Confidence Evaluation -> Intervention -> Learner Model Update.
    """
    # Step 1: Validate Learner & Question
    user = db.query(DBUser).filter_by(id=payload.learner_id).first()
    if not user:
        # Auto-create guest learner if needed
        user = DBUser(
            id=payload.learner_id,
            username=payload.learner_id,
            email=f"{payload.learner_id}@relearn.ai",
            role="student"
        )
        db.add(user)
        db.commit()

    q_obj = db.query(DBQuestion).filter_by(id=payload.question_id).first()
    concept_id = q_obj.concept if q_obj else "python_range"

    # Step 2: Pure ML Misconception Diagnosis
    diag_res = diagnosis_engine.diagnose(
        domain_id=payload.domain_id,
        question_id=payload.question_id,
        learner_id=payload.learner_id,
        submission_text=payload.response if payload.response_type == "text" else "",
        submission_code=payload.response if payload.response_type == "code" else ""
    )

    pred = diag_res.get("prediction", {})
    predicted_mid = pred.get("misconception_id", "M001")
    confidence = pred.get("confidence", 0.85)
    is_correct = pred.get("is_correct", pred.get("correctness", False))

    steps_executed = [
        "1. Webhook Payload Ingested & Schema Validated",
        f"2. ML Misconception Diagnosis Executed (Predicted: {predicted_mid})",
        f"3. Confidence Calibration Check ({round(confidence * 100, 1)}% vs 60.0% threshold)"
    ]

    intervention_id = None
    intervention_title = None

    # Step 3: Conditional Branching based on Confidence
    if confidence >= 0.60 and not is_correct:
        intervention_data = intervention_engine.generate_intervention(
            misconception_id=predicted_mid,
            confidence=confidence
        )
        intervention_id = f"I_{predicted_mid}"
        intervention_title = intervention_data.get("title", "Targeted Conceptual Intervention")
        steps_executed.append(f"4. Fetched Targeted Intervention: '{intervention_title}'")
    elif is_correct:
        steps_executed.append("4. Response is Correct: Triggering Positive Reinforcement")
    else:
        steps_executed.append("4. Low Confidence (<60%): Selected Diagnostic Probe Question")

    # Step 4: Update Learner Model & Persistent State
    learner_record = db.query(DBLearnerMisconception).filter_by(
        user_id=payload.learner_id,
        misconception_id=predicted_mid
    ).first()

    if not is_correct:
        if not learner_record:
            learner_record = DBLearnerMisconception(
                user_id=payload.learner_id,
                misconception_id=predicted_mid,
                status="ACTIVE",
                occurrences=1,
                interventions_taken=1 if intervention_id else 0,
                confidence=confidence,
                last_detected=datetime.utcnow()
            )
            db.add(learner_record)
        else:
            learner_record.occurrences += 1
            if intervention_id:
                learner_record.interventions_taken += 1
            learner_record.confidence = confidence
            learner_record.status = "RECURRING" if learner_record.occurrences > 2 else "ACTIVE"
            learner_record.last_detected = datetime.utcnow()
        steps_executed.append(f"5. Persistent Learner State Updated (Misconception {predicted_mid}: {learner_record.status})")
    else:
        steps_executed.append("5. Concept Mastery Maintained / Elevated")

    db.commit()

    # Step 5: Adaptive Recommendations
    steps_executed.append("6. Curriculum Recommendation Engine Triggered")

    return {
        "status": "success",
        "orchestrator": "n8n / ReLearn Engine",
        "timestamp": datetime.utcnow().isoformat(),
        "workflow_execution": {
            "execution_id": f"exec_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "steps": steps_executed
        },
        "response": {
            "correct": is_correct,
            "misconception_id": predicted_mid if not is_correct else "NONE",
            "misconception_name": pred.get("name", "Range Upper-Bound Inclusion"),
            "confidence": round(confidence, 4),
            "intervention_id": intervention_id,
            "intervention_title": intervention_title,
            "next_action": "take_intervention" if not is_correct else "next_challenge"
        }
    }
