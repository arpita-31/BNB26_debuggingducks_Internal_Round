"""
Tests for Intervention Scaffolding and Unseen Transfer Resolution Verification
"""
from app.intervention.engine import intervention_engine
from app.reassessment.engine import reassessment_engine
from app.reassessment.resolution_checker import resolution_checker

def test_intervention_scaffold_retrieval():
    interv = intervention_engine.get_intervention_for_misconception("M001")
    assert interv["misconception_id"] == "M001"
    assert len(interv["stages"]) >= 4
    # Check for micro-practice check stage
    types = [s["type"] for s in interv["stages"]]
    assert "conceptual_reframing" in types
    assert "visual_model" in types
    assert "micro_practice" in types

def test_micro_practice_verification():
    # Correct answer check
    res_correct = intervention_engine.verify_micro_practice("M001", selected_option_index=1)
    assert res_correct["is_correct"] is True

    # Incorrect answer check
    res_wrong = intervention_engine.verify_micro_practice("M001", selected_option_index=0)
    assert res_wrong["is_correct"] is False

def test_unseen_reassessment_resolution():
    # Test unseen transfer question resolution check
    eval_res = reassessment_engine.evaluate_resolution(
        reassessment_question_id="Q_TRANS_M001_01",
        misconception_id="M001",
        learner_response="Prints 2, 3, 4, 5 because the upper bound 6 is excluded.",
        learner_code=""
    )
    assert eval_res["status"] in ["RESOLVED", "IMPROVING"]
    assert eval_res["is_resolved"] is True
    assert eval_res["mastery_delta"] > 0
