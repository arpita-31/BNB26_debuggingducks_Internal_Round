"""
Test Runner for ReLearn Test Suite using Python Standard Library unittest
"""
import sys
from pathlib import Path

# Add root and backend to path
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(backend_dir))

import unittest

# Import all test functions and wrap in TestCase
from tests.test_ml_pipeline import (
    test_preprocessor_ast_signals,
    test_preprocessor_lexical_markers,
    test_classifier_prediction_and_calibration
)
from tests.test_diagnosis_differentiation import (
    test_diagnose_m001_inclusive_bound,
    test_differentiation_between_m001_and_m002
)
from tests.test_intervention_resolution import (
    test_intervention_scaffold_retrieval,
    test_micro_practice_verification,
    test_unseen_reassessment_resolution
)
from tests.test_learner_model import (
    test_state_machine_transitions,
    test_learner_profile_and_mastery,
    test_adaptive_recommendation
)
from tests.test_api_endpoints import (
    test_health_endpoint,
    test_domains_and_questions,
    test_diagnose_endpoint,
    test_intervention_and_reassessment_endpoints,
    test_model_metrics_endpoints,
    test_demo_scenarios_endpoint
)

class ReLearnMasterTestSuite(unittest.TestCase):
    def test_01_ast_signals(self):
        test_preprocessor_ast_signals()

    def test_02_lexical_markers(self):
        test_preprocessor_lexical_markers()

    def test_03_classifier_and_calibration(self):
        test_classifier_prediction_and_calibration()

    def test_04_diagnose_m001(self):
        test_diagnose_m001_inclusive_bound()

    def test_05_differentiation_and_probe(self):
        test_differentiation_between_m001_and_m002()

    def test_06_intervention_scaffold(self):
        test_intervention_scaffold_retrieval()

    def test_07_micro_practice(self):
        test_micro_practice_verification()

    def test_08_unseen_reassessment_resolution(self):
        test_unseen_reassessment_resolution()

    def test_09_state_machine_transitions(self):
        test_state_machine_transitions()

    def test_10_learner_profile_and_mastery(self):
        test_learner_profile_and_mastery()

    def test_11_adaptive_recommendation(self):
        test_adaptive_recommendation()

    def test_12_health_endpoint(self):
        test_health_endpoint()

    def test_13_domains_and_questions(self):
        test_domains_and_questions()

    def test_14_diagnose_endpoint(self):
        test_diagnose_endpoint()

    def test_15_intervention_and_reassessment_api(self):
        test_intervention_and_reassessment_endpoints()

    def test_16_model_metrics_endpoints(self):
        test_model_metrics_endpoints()

    def test_17_demo_scenarios_endpoint(self):
        test_demo_scenarios_endpoint()

if __name__ == "__main__":
    unittest.main(verbosity=2)
