"""
Learner Model API Endpoints for ReLearn
Serves persistent learner profile, concept mastery vectors, and adaptive curriculum actions.
"""
from fastapi import APIRouter, HTTPException
from app.learner_model.engine import learner_engine
from app.learner_model.adaptive_curriculum import curriculum_planner

router = APIRouter(prefix="/api", tags=["Learner Model"])

@router.get("/learner/{learner_id}")
def get_learner(learner_id: str):
    """Returns persistent profile, concept mastery, and active/resolved misconceptions."""
    return learner_engine.get_learner_profile(learner_id)

@router.get("/progress/{learner_id}")
def get_learner_progress(learner_id: str):
    """Returns concise summary metrics of learner progress."""
    profile = learner_engine.get_learner_profile(learner_id)
    return {
        "learner_id": learner_id,
        "overall_mastery": profile["overall_mastery"],
        "active_misconceptions_count": len(profile["active_misconceptions"]),
        "resolved_misconceptions_count": len(profile["resolved_misconceptions"]),
        "summary": profile["summary"]
    }

@router.get("/recommendation/{learner_id}")
def get_adaptive_recommendation(learner_id: str):
    """Calculates next learning activity adapted to learner's cognitive state."""
    return curriculum_planner.recommend_next_step(learner_id)
