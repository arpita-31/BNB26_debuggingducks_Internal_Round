"""
Reassessment Engine for ReLearn
Selects unseen transfer questions and coordinates the resolution verification loop.
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .resolution_checker import resolution_checker

class ReassessmentEngine:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.questions_file = base_dir / "data" / "questions_bank.json"
        self._transfer_questions: List[Dict[str, Any]] = []
        self._load_questions()

    def _load_questions(self):
        if self.questions_file.exists():
            with open(self.questions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._transfer_questions = data.get("transfer_reassessment_questions", [])

    def get_reassessment_question(
        self,
        misconception_id: str,
        original_question_id: str = None
    ) -> Optional[Dict[str, Any]]:
        """Selects an unseen transfer question mapped to the targeted misconception."""
        candidates = [
            q for q in self._transfer_questions
            if q.get("target_misconception") == misconception_id
            and q.get("id") != original_question_id
        ]
        
        if not candidates:
            # Fallback to any transfer question if specific misconception doesn't have a custom one
            candidates = self._transfer_questions

        return candidates[0] if candidates else None

    def evaluate_resolution(
        self,
        reassessment_question_id: str,
        misconception_id: str,
        learner_response: str,
        learner_code: str = ""
    ) -> Dict[str, Any]:
        """Evaluates learner response on the reassessment question to determine resolution."""
        q_meta = next((q for q in self._transfer_questions if q["id"] == reassessment_question_id), None)
        if not q_meta:
            q_meta = {"target_misconception": misconception_id, "validation_rules": {}}

        return resolution_checker.verify_reassessment(
            misconception_id=misconception_id,
            question_meta=q_meta,
            learner_response_text=learner_response,
            learner_code=learner_code
        )

reassessment_engine = ReassessmentEngine()
