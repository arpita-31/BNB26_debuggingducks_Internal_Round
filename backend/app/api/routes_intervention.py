"""
Intervention API Endpoints for ReLearn
Serves targeted multi-stage pedagogical scaffolds and evaluates micro-practice answers.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.api_models import InterventionRequest, MicroPracticeRequest
from app.intervention.engine import intervention_engine

router = APIRouter(prefix="/api", tags=["Intervention"])

@router.post("/intervention")
def get_intervention(payload: InterventionRequest):
    """Retrieves misconception-specific multi-stage pedagogical scaffold."""
    return intervention_engine.get_intervention_for_misconception(
        misconception_id=payload.misconception_id,
        confidence=payload.confidence,
        learner_id=payload.learner_id
    )

@router.post("/intervention/practice")
def check_micro_practice(payload: MicroPracticeRequest):
    """Validates the learner's response to an interactive intervention micro-check."""
    res = intervention_engine.verify_micro_practice(
        misconception_id=payload.misconception_id,
        selected_option_index=payload.selected_option_index
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res
