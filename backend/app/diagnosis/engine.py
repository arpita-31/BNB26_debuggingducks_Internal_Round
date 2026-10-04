"""
Diagnosis Engine for ReLearn
Orchestrates the complete diagnostic pipeline from normalized input to
probabilistic misconception prediction, evidence extraction, and differentiation.
"""
import json
import joblib
from pathlib import Path
from typing import Dict, Any, Optional

from app.domain.registry import domain_registry
from app.domain.base import NormalizedSubmission
from app.ml.classifier import MisconceptionClassifier
from app.ml.train import run_training_pipeline
from .differentiator import differentiator

class DiagnosisEngine:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.artifacts_dir = self.base_dir / "backend" / "app" / "ml" / "artifacts"
        self.taxonomy_file = self.base_dir / "data" / "misconception_taxonomy.json"
        
        self.model: Optional[MisconceptionClassifier] = None
        self.taxonomy_map: Dict[str, Any] = {}
        self._load_taxonomy()
        self._ensure_model_loaded()

    def _load_taxonomy(self):
        if self.taxonomy_file.exists():
            with open(self.taxonomy_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.taxonomy_map = {t["id"]: t for t in data.get("taxonomies", [])}

    def _ensure_model_loaded(self):
        model_path = self.artifacts_dir / "model.joblib"
        if model_path.exists():
            try:
                self.model = joblib.load(model_path)
                return
            except Exception as e:
                print(f"Error loading model: {e}. Retraining...")
        
        # Run training pipeline if artifact doesn't exist
        print("Training ReLearn ML model artifact on initial boot...")
        run_training_pipeline()
        self.model = joblib.load(model_path)

    def diagnose_submission(
        self,
        domain_id: str,
        question_id: str,
        raw_submission: Dict[str, Any],
        learner_id: str = "demo_learner"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end diagnosis:
        1. Modality normalization
        2. AST and syntax check
        3. Model feature extraction & classification
        4. Differentiation & margin analysis
        5. Evidence synthesis
        """
        self._ensure_model_loaded()
        domain = domain_registry.get(domain_id) or domain_registry.get("python_programming")
        norm: NormalizedSubmission = domain.normalize_input(raw_submission)

        # Syntax check
        syntax_res = domain.validate_syntax(norm.code_content)

        # ML Diagnostic Inference
        diag_res = self.model.diagnose(
            text=norm.text_reasoning,
            code=norm.code_content,
            taxonomy_map=self.taxonomy_map
        )

        # Candidate Differentiation & Ambiguity Check
        diff_res = differentiator.analyze_candidates(
            predicted_id=diag_res["predicted_id"],
            confidence=diag_res["confidence"],
            second_id=diag_res["second_id"],
            margin=diag_res["margin"],
            ranked_candidates=diag_res["ranked_candidates"],
            text_reasoning=norm.text_reasoning,
            code_snippet=norm.code_content
        )

        return {
            "learner_id": learner_id,
            "question_id": question_id,
            "domain_id": domain.domain_id,
            "modality": norm.modality,
            "syntax_valid": syntax_res["valid"],
            "syntax_error": syntax_res.get("error"),
            "prediction": {
                "misconception_id": diag_res["predicted_id"],
                "name": diag_res["predicted_name"],
                "concept": diag_res["concept"],
                "confidence": diag_res["confidence"],
                "is_correct": diag_res["is_correct"]
            },
            "differentiation": {
                "margin": diff_res["margin"],
                "secondary_id": diff_res["secondary_id"],
                "is_ambiguous": diff_res["is_ambiguous"],
                "rationale": diff_res["differentiation_rationale"]
            },
            "ranked_candidates": diag_res["ranked_candidates"],
            "alternatives": diag_res["alternatives"],
            "evidence": diag_res["evidence"],
            "diagnostic_probe": diff_res["probe"],
            "pipeline_stages": diff_res["pipeline_stages"]
        }

    def diagnose(
        self,
        domain_id: str,
        question_id: str,
        learner_id: str = "demo_learner",
        submission_text: str = "",
        submission_code: str = ""
    ) -> Dict[str, Any]:
        """Convenience method accepting raw text/code submissions."""
        modality = "code" if submission_code and not submission_text else "text"
        raw_submission = {
            "modality": modality,
            "text": submission_text,
            "code": submission_code
        }
        return self.diagnose_submission(
            domain_id=domain_id,
            question_id=question_id,
            raw_submission=raw_submission,
            learner_id=learner_id
        )

diagnosis_engine = DiagnosisEngine()
