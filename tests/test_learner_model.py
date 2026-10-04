"""
Tests for Learner Model Persistence, Mastery Updates, and State Transitions
"""
from app.learner_model.state_machine import state_machine
from app.learner_model.engine import learner_engine
from app.learner_model.adaptive_curriculum import curriculum_planner

def test_state_machine_transitions():
    # Diagnostic transition
    s1 = state_machine.transition_on_diagnosis("UNKNOWN", confidence=0.88, occurrences=1)
    assert s1 == "ACTIVE"

    # Resolution transition
    s2 = state_machine.transition_on_reassessment("ACTIVE", resolution_status="RESOLVED", successes_count=1)
    assert s2 == "RESOLVED"

    # Recurrence transition
    s3 = state_machine.transition_on_diagnosis("RESOLVED", confidence=0.85, occurrences=2)
    assert s3 == "RECURRING"

def test_learner_profile_and_mastery():
    profile = learner_engine.get_learner_profile("demo_learner")
    assert profile["learner_id"] == "demo_learner"
    assert "overall_mastery" in profile
    assert len(profile["concepts"]) > 0

def test_adaptive_recommendation():
    rec = curriculum_planner.recommend_next_step("demo_learner")
    assert "action" in rec
    assert "suggested_activity" in rec
