"""
Resolution Checker for ReLearn
Evaluates whether a diagnosed misconception has genuinely been resolved
using unseen transfer questions, boundary invariants, and reasoning checks.
"""
from typing import Dict, Any, List
import re

class ResolutionChecker:
    def verify_reassessment(
        self,
        misconception_id: str,
        question_meta: Dict[str, Any],
        learner_response_text: str,
        learner_code: str = ""
    ) -> Dict[str, Any]:
        """
        Evaluates learner performance on an unseen transfer question.
        Checks for presence of correct outputs, absence of misconception indicators,
        and coherent conceptual invariants.
        """
        text = learner_response_text.strip().lower()
        validation = question_meta.get("validation_rules", {})
        must_contain = validation.get("must_contain", [])
        must_not_contain = validation.get("must_not_contain", [])
        invariants = validation.get("concept_invariants", [])

        # 1. Output content checks
        contains_correct_tokens = all(
            token.lower() in text or token in learner_code
            for token in must_contain
        ) if must_contain else True

        # 2. Misconception signal check with negation awareness
        # If learner says "excludes 6" or "6 is excluded" or "not 6", it's proof of understanding!
        def is_negated(token: str, full_text: str) -> bool:
            negation_patterns = [
                rf"exclude[s|d]?\s+{re.escape(token)}",
                rf"{re.escape(token)}\s+is\s+exclude[s|d]?",
                rf"not\s+{re.escape(token)}",
                rf"stops\s+before\s+{re.escape(token)}",
                rf"without\s+{re.escape(token)}",
                rf"excluding\s+{re.escape(token)}"
            ]
            return any(re.search(pat, full_text) for pat in negation_patterns)

        contains_forbidden_tokens = False
        for token in must_not_contain:
            if token.lower() in text or token in learner_code:
                if not is_negated(token.lower(), text):
                    contains_forbidden_tokens = True
                    break

        # 3. Concept invariant reasoning check
        has_sound_reasoning = any(
            inv.lower() in text for inv in invariants
        ) if invariants else True

        # Synthesize resolution verdict
        is_success = contains_correct_tokens and not contains_forbidden_tokens

        evidence_reasons = []
        if contains_correct_tokens:
            evidence_reasons.append("Correctly identified the expected execution values on unseen problem.")
        if not contains_forbidden_tokens:
            evidence_reasons.append(f"Successfully avoided the {misconception_id} fallacy (no forbidden tokens detected).")
        else:
            evidence_reasons.append(f"Still exhibits signals of {misconception_id} in unseen transfer context.")

        if has_sound_reasoning:
            evidence_reasons.append("Demonstrated valid conceptual understanding of the underlying invariant.")

        # Determine granular resolution state
        if is_success and has_sound_reasoning:
            status = "RESOLVED"
            delta = 0.52
        elif is_success and not has_sound_reasoning:
            status = "IMPROVING"
            delta = 0.35
        elif not is_success and contains_forbidden_tokens:
            status = "PERSISTENT"
            delta = -0.10
        else:
            status = "PARTIALLY_RESOLVED"
            delta = 0.15

        return {
            "misconception_id": misconception_id,
            "status": status,
            "is_resolved": (status in ["RESOLVED", "IMPROVING"]),
            "evidence": " ".join(evidence_reasons),
            "mastery_delta": delta,
            "details": {
                "contains_correct_tokens": contains_correct_tokens,
                "contains_forbidden_tokens": contains_forbidden_tokens,
                "has_sound_reasoning": has_sound_reasoning
            }
        }

resolution_checker = ResolutionChecker()
