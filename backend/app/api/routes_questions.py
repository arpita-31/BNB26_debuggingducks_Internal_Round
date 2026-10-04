"""
Questions and Domains API Endpoints for ReLearn
Serves domain catalogs, concepts, and primary learning session questions.
"""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.domain.registry import domain_registry

router = APIRouter(prefix="/api", tags=["Questions & Domains"])

@router.get("/domains")
def get_domains():
    """Lists registered academic domains and their implementation readiness."""
    return domain_registry.list_all()

@router.get("/questions")
def get_questions():
    """Returns all primary learning questions."""
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    q_path = base_dir / "data" / "questions_bank.json"
    if not q_path.exists():
        raise HTTPException(status_code=404, detail="Questions bank not found.")

    with open(q_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("questions", [])

@router.get("/questions/{question_id}")
def get_question_by_id(question_id: str):
    """Retrieves specific question details."""
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    q_path = base_dir / "data" / "questions_bank.json"
    with open(q_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for q in data.get("questions", []) + data.get("transfer_reassessment_questions", []):
            if q["id"] == question_id:
                return q
    raise HTTPException(status_code=404, detail=f"Question '{question_id}' not found.")
