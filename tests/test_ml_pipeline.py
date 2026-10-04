"""
Unit tests for ReLearn ML Pipeline
"""
from app.ml.preprocessor import ResponsePreprocessor
from app.ml.feature_extractor import FeatureExtractor
from app.ml.classifier import MisconceptionClassifier

def test_preprocessor_ast_signals():
    prep = ResponsePreprocessor()
    code = "for i in range(1, 5):\n    print(i)"
    signals = prep.extract_ast_signals(code)
    assert signals["has_for_loop"] is True
    assert signals["has_range_call"] is True
    assert signals["range_args_count"] == 2

def test_preprocessor_lexical_markers():
    prep = ResponsePreprocessor()
    text = "The loop includes the upper bound 5 because it runs up to and including 5."
    markers = prep.extract_lexical_markers(text)
    assert "signal_inclusive_bound" in markers

def test_classifier_prediction_and_calibration():
    # Mini training check
    texts = [
        "range(1, 5) includes the upper bound 5",
        "loop runs 6 times because it counted from 0",
        "if x = 5 assigns instead of equals",
        "range excludes 5 and prints 1 2 3 4"
    ]
    codes = ["", "", "if x = 5:", "for i in range(1, 5): pass"]
    labels = ["M001", "M002", "M003", "NONE"]

    classifier = MisconceptionClassifier()
    classifier.train(texts, codes, labels)
    assert classifier.is_trained is True

    # Test diagnosis inference
    diag = classifier.diagnose("The upper bound 5 is included in range(1, 5)")
    assert diag["predicted_id"] in ["M001", "M002", "M003", "NONE"]
    assert 0.0 <= diag["confidence"] <= 1.0
    assert len(diag["ranked_candidates"]) > 0
