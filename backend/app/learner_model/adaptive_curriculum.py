"""
Adaptive Curriculum Planner for ReLearn
Selects optimal pedagogical next actions based on the persistent learner model.
"""
from typing import Dict, Any, List
from .engine import learner_engine

class AdaptiveCurriculumPlanner:
    def recommend_next_step(self, learner_id: str) -> Dict[str, Any]:
        """Calculates next learning activity adapted to learner's cognitive state."""
        profile = learner_engine.get_learner_profile(learner_id)
        active_misconceptions = profile.get("active_misconceptions", [])
        concepts = profile.get("concepts", [])

        # Priority 1: If there is an ACTIVE or RECURRING misconception, address it immediately
        urgent_misc = next(
            (m for m in active_misconceptions if m["status"] in ["ACTIVE", "RECURRING"]),
            None
        )
        if urgent_misc:
            return {
                "action": "TARGETED_INTERVENTION",
                "urgency": "HIGH",
                "misconception_id": urgent_misc["misconception_id"],
                "reason": (
                    f"Misconception {urgent_misc['misconception_id']} is currently {urgent_misc['status']}. "
                    "Targeted cognitive scaffold is required before proceeding."
                ),
                "suggested_activity": "Launch Guided Scaffold & Visual Reframing"
            }

        # Priority 2: If there is a SUSPECTED misconception, administer a diagnostic problem
        suspected_misc = next(
            (m for m in active_misconceptions if m["status"] == "SUSPECTED"),
            None
        )
        if suspected_misc:
            return {
                "action": "DIAGNOSTIC_VERIFICATION",
                "urgency": "MEDIUM",
                "misconception_id": suspected_misc["misconception_id"],
                "reason": "Potential misconception suspected. Reassess with disambiguating probe.",
                "suggested_activity": "Administer Diagnostic Probe"
            }

        # Priority 3: Lowest mastery concept
        sorted_concepts = sorted(concepts, key=lambda c: c["mastery"])
        if sorted_concepts:
            target_concept = sorted_concepts[0]
            if target_concept["mastery"] < 0.7:
                return {
                    "action": "PRACTICE_CONCEPT",
                    "urgency": "NORMAL",
                    "concept_id": target_concept["concept_id"],
                    "reason": f"Reinforce understanding of '{target_concept['name']}' (Mastery: {target_concept['mastery'] * 100:.0f}%).",
                    "suggested_activity": "Next Conceptual Challenge"
                }

        # Priority 4: All tracked concepts mastered -> Advance to next curriculum module
        return {
            "action": "ADVANCE_CURRICULUM",
            "urgency": "LOW",
            "concept_id": "next_module",
            "reason": "All active concepts mastered. Ready for next advanced programming topic.",
            "suggested_activity": "Advance to Data Structures (Lists, Dicts & Tuples)"
        }

curriculum_planner = AdaptiveCurriculumPlanner()
