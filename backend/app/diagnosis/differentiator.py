"""
Misconception Differentiation Engine for ReLearn
Differentiates between overlapping misconceptions that yield identical surface outputs
by evaluating reasoning evidence, AST patterns, and confidence margins.
"""
from typing import Dict, Any, List, Optional
from .diagnostic_questions import diagnostic_engine

class MisconceptionDifferentiator:
    def __init__(self, margin_threshold: float = 0.15, min_confidence: float = 0.55):
        self.margin_threshold = margin_threshold
        self.min_confidence = min_confidence

    def analyze_candidates(
        self,
        predicted_id: str,
        confidence: float,
        second_id: Optional[str],
        margin: float,
        ranked_candidates: List[Dict[str, Any]],
        text_reasoning: str,
        code_snippet: str
    ) -> Dict[str, Any]:
        """
        Differentiates competing diagnoses. If confidence is below threshold or margin
        between top candidates is narrow, generates a targeted diagnostic probe.
        """
        is_ambiguous = (confidence < self.min_confidence) or (margin < self.margin_threshold and second_id is not None)
        
        probe = None
        differentiation_rationale = ""

        if is_ambiguous and second_id:
            probe = diagnostic_engine.find_disambiguation_probe(predicted_id, second_id)
            differentiation_rationale = (
                f"Close margin ({margin:.2%}) between '{predicted_id}' and '{second_id}'. "
                "Triggering targeted diagnostic probe to disambiguate underlying mental model."
            )
        else:
            differentiation_rationale = (
                f"Sufficient confidence margin ({margin:.2%}) separating '{predicted_id}' "
                f"from nearest alternative '{second_id or 'None'}'. High distinctiveness."
            )

        # Build pipeline stages visualization data for judges and UI
        pipeline_stages = [
            {
                "stage": 1,
                "name": "Input Ingestion",
                "status": "COMPLETED",
                "detail": f"Processed {len(text_reasoning.split())} reasoning tokens and {len(code_snippet.splitlines())} code lines."
            },
            {
                "stage": 2,
                "name": "Feature Extraction",
                "status": "COMPLETED",
                "detail": "Extracted word/char n-grams, AST loop/boundary signals, and lexical markers."
            },
            {
                "stage": 3,
                "name": "Candidate Scoring",
                "status": "COMPLETED",
                "detail": f"Evaluated posterior probabilities over {len(ranked_candidates)} classes."
            },
            {
                "stage": 4,
                "name": "Differentiation & Ambiguity Analysis",
                "status": "AMBIGUOUS" if is_ambiguous else "CONFIDENT",
                "detail": differentiation_rationale
            }
        ]

        return {
            "is_ambiguous": is_ambiguous,
            "margin": margin,
            "primary_id": predicted_id,
            "secondary_id": second_id,
            "probe": probe,
            "differentiation_rationale": differentiation_rationale,
            "pipeline_stages": pipeline_stages
        }

differentiator = MisconceptionDifferentiator()
