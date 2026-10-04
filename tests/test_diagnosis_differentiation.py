"""
Tests for Misconception Differentiation and Ambiguity Handling
"""
from app.diagnosis.engine import diagnosis_engine
from app.diagnosis.differentiator import differentiator

def test_diagnose_m001_inclusive_bound():
    res = diagnosis_engine.diagnose_submission(
        domain_id="python_programming",
        question_id="Q_PY_RANGE_01",
        raw_submission={
            "modality": "text+code",
            "text": "It prints 1, 2, 3, 4, 5 because range(1, 5) includes the upper bound 5.",
            "code": ""
        }
    )
    assert res["prediction"]["misconception_id"] == "M001"
    assert res["prediction"]["confidence"] > 0.5
    assert len(res["evidence"]) > 0
    assert any("upper bound" in e.lower() or "inclusive" in e.lower() or "closed interval" in e.lower() for e in res["evidence"])

def test_differentiation_between_m001_and_m002():
    # Candidate ranking margin calculation
    diff = differentiator.analyze_candidates(
        predicted_id="M001",
        confidence=0.58,
        second_id="M002",
        margin=0.06,  # narrow margin < 0.15
        ranked_candidates=[{"id": "M001", "probability": 0.58}, {"id": "M002", "probability": 0.52}],
        text_reasoning="Prints 5 because of 5 items",
        code_snippet=""
    )
    assert diff["is_ambiguous"] is True
    assert diff["probe"] is not None
    assert "PROBE_M001_M002" in diff["probe"]["id"]
