"""
Diagnosis API Endpoints for ReLearn
Handles submission ingestion, ML prediction, candidate differentiation, and probe answers.
"""
from fastapi import APIRouter, HTTPException
from app.schemas.api_models import DiagnoseRequest, ProbeAnswerRequest
from app.diagnosis.engine import diagnosis_engine
from app.diagnosis.diagnostic_questions import diagnostic_engine
from app.learner_model.engine import learner_engine

router = APIRouter(prefix="/api", tags=["Diagnosis"])

@router.post("/diagnose")
def diagnose_submission(payload: DiagnoseRequest):
    """
    Analyzes learner submission, extracts AST and n-gram signals,
    predicts misconception with calibrated probability distribution,
    and returns differentiation and evidence.
    """
    try:
        raw_submission = {
            "modality": payload.submission.modality,
            "text": payload.submission.text,
            "code": payload.submission.code,
            "metadata": payload.submission.metadata
        }

        diagnosis = diagnosis_engine.diagnose_submission(
            domain_id=payload.domain_id,
            question_id=payload.question_id,
            raw_submission=raw_submission,
            learner_id=payload.learner_id
        )

        # Update persistent learner model with diagnosed state
        if diagnosis["prediction"]["misconception_id"] != "NONE":
            learner_engine.record_diagnosis(
                learner_id=payload.learner_id,
                question_id=payload.question_id,
                misconception_id=diagnosis["prediction"]["misconception_id"],
                confidence=diagnosis["prediction"]["confidence"],
                evidence=diagnosis["evidence"]
            )

        return diagnosis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/probe/answer")
def answer_diagnostic_probe(payload: ProbeAnswerRequest):
    """Evaluates learner's choice on a disambiguation probe question to refine the diagnosis."""
    res = diagnostic_engine.evaluate_probe_response(
        probe_id=payload.probe_id,
        selected_option_index=payload.selected_option_index
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])

    # If disambiguated to a misconception, update learner model
    misc_id = res.get("disambiguated_misconception_id")
    if misc_id and misc_id != "NONE":
        learner_engine.record_diagnosis(
            learner_id=payload.learner_id,
            question_id=payload.probe_id,
            misconception_id=misc_id,
            confidence=0.92,
            evidence=[f"Disambiguated via diagnostic probe: {res['selected_option']}"]
        )

    return res
