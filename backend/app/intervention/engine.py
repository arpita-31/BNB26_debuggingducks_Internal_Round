"""
Intervention Engine for ReLearn
Selects, scaffolds, and serves targeted interventions based on diagnosed misconceptions.
"""
from typing import Dict, Any, Optional
from .templates import INTERVENTION_TEMPLATES

class InterventionEngine:
    def get_intervention_for_misconception(
        self,
        misconception_id: str,
        confidence: float = 1.0,
        learner_id: str = "demo_learner"
    ) -> Dict[str, Any]:
        """Retrieves targeted intervention scaffold for diagnosed misconception."""
        template = INTERVENTION_TEMPLATES.get(misconception_id)
        if not template:
            template = INTERVENTION_TEMPLATES["NONE"]

        return {
            "learner_id": learner_id,
            "misconception_id": misconception_id,
            "name": template["name"],
            "concept": template["concept"],
            "confidence_detected": round(confidence, 4),
            "pedagogical_goal": template["pedagogical_goal"],
            "stages": template["stages"],
            "total_stages": len(template["stages"])
        }

    def generate_intervention(
        self,
        misconception_id: str,
        confidence: float = 1.0,
        learner_id: str = "demo_learner"
    ) -> Dict[str, Any]:
        """Alias for get_intervention_for_misconception."""
        return self.get_intervention_for_misconception(
            misconception_id=misconception_id,
            confidence=confidence,
            learner_id=learner_id
        )

    def verify_micro_practice(
        self,
        misconception_id: str,
        selected_option_index: int
    ) -> Dict[str, Any]:
        """Evaluates learner's response to the intervention micro-practice question."""
        template = INTERVENTION_TEMPLATES.get(misconception_id)
        if not template:
            return {"error": "Invalid misconception"}

        practice_stage = next((s for s in template["stages"] if s["type"] == "micro_practice"), None)
        if not practice_stage:
            return {"is_correct": True, "feedback": "Stage completed."}

        correct_idx = practice_stage["correct_index"]
        is_correct = (selected_option_index == correct_idx)

        return {
            "is_correct": is_correct,
            "feedback": practice_stage["feedback_correct"] if is_correct else practice_stage["feedback_incorrect"],
            "correct_index": correct_idx
        }

intervention_engine = InterventionEngine()
