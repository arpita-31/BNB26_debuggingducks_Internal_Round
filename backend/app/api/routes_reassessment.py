"""
Reassessment and Resolution API Endpoints for ReLearn
Serves unseen transfer questions and empirically verifies misconception resolution.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.api_models import ReassessmentRequest, ResolutionRequest
from app.reassessment.engine import reassessment_engine
from app.learner_model.engine import learner_engine

router = APIRouter(prefix="/api", tags=["Reassessment & Resolution"])

@router.post("/reassess")
def get_reassessment_question(payload: ReassessmentRequest):
    """Retrieves an unseen transfer problem targeted at the specified misconception."""
    question = reassessment_engine.get_reassessment_question(
        misconception_id=payload.misconception_id,
        original_question_id=payload.original_question_id
    )
    if not question:
        raise HTTPException(status_code=404, detail="No transfer reassessment question available.")
    return {
        "status": "READY",
        "misconception_id": payload.misconception_id,
        "is_unseen": True,
        "question": question
    }

@router.post("/resolve")
def resolve_misconception(payload: ResolutionRequest):
    """
    Evaluates learner's submission on the transfer problem.
    Verifies conceptual invariants, computes resolution status,
    and updates the persistent learner model mastery.
    """
    eval_result = reassessment_engine.evaluate_resolution(
        reassessment_question_id=payload.reassessment_id,
        misconception_id=payload.misconception_id,
        learner_response=payload.learner_response,
        learner_code=payload.learner_code
    )

    # Persist cognitive state change in learner model
    model_update = learner_engine.record_resolution(
        learner_id=payload.learner_id,
        misconception_id=payload.misconception_id,
        concept_id=payload.concept_id,
        resolution_status=eval_result["status"],
        mastery_delta=eval_result["mastery_delta"]
    )

    return {
        "reassessment_id": payload.reassessment_id,
        "misconception_id": payload.misconception_id,
        "resolution_status": eval_result["status"],
        "is_resolved": eval_result["is_resolved"],
        "evidence": eval_result["evidence"],
        "mastery_before": model_update.get("mastery_before"),
        "mastery_after": model_update.get("mastery_after"),
        "new_state": model_update.get("new_status")
    }
