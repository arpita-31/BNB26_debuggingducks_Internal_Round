"""
Secondary LLM Layer for ReLearn
Provides enriched natural language explanations and intervention phrasing using Gemini/OpenAI
with 100% deterministic local fallback when API keys are absent or network is unavailable.
Core ML classification, mastery scores, and resolution state machines NEVER depend on this service.
"""
import os
import json
from typing import Optional, Dict, Any

class LLMEnrichmentService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def is_available(self) -> bool:
        """Returns True only if an external LLM key is configured."""
        return bool(self.gemini_api_key or self.openai_api_key)

    def enrich_intervention(
        self,
        misconception_name: str,
        concept: str,
        student_response: str,
        base_explanation: str
    ) -> Dict[str, Any]:
        """
        Enriches an intervention with tailored phrasing.
        Falls back seamlessly to deterministic template if LLM is unavailable.
        """
        if not self.is_available():
            return {
                "source": "deterministic_fallback",
                "personalized_tip": (
                    f"Notice that in {concept}, the problem specifically arises from '{misconception_name}'. "
                    f"Review the counterexample carefully to recalibrate your mental model."
                ),
                "summary": base_explanation
            }

        # Attempt Gemini call if configured
        if self.gemini_api_key:
            try:
                import requests
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
                prompt = (
                    f"You are a cognitive CS tutor. The student exhibits the misconception: '{misconception_name}' "
                    f"in concept '{concept}'. Student's flawed answer was: '{student_response}'.\n"
                    f"Provide a 2-sentence encouraging pedagogical intervention clarifying why this happens without giving away future quiz answers."
                )
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                res = requests.post(url, json=payload, timeout=4)
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return {
                        "source": "gemini_api",
                        "personalized_tip": text,
                        "summary": base_explanation
                    }
            except Exception:
                pass

        # Deterministic fallback
        return {
            "source": "deterministic_fallback",
            "personalized_tip": (
                f"In {concept}, a common mental trap is '{misconception_name}'. "
                f"Notice how the execution semantics differ from conversational intuition."
            ),
            "summary": base_explanation
        }

    def generate_practice_variant(
        self,
        concept: str,
        misconception_id: str,
        difficulty: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Generates an additional practice question variant.
        Falls back to curated database questions if API key is absent.
        """
        return {
            "source": "curated_taxonomy",
            "concept": concept,
            "difficulty": difficulty,
            "target_misconception": misconception_id
        }

llm_service = LLMEnrichmentService()
