"""
Training Script for ReLearn ML Pipeline
Trains the calibrated classifier, evaluates on held-out test data,
and persists production artifacts.
"""
import json
import joblib
from pathlib import Path
from typing import Dict, Any

from app.ml.classifier import MisconceptionClassifier
from app.ml.evaluator import ModelEvaluator

def run_training_pipeline() -> Dict[str, Any]:
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = base_dir / "data"
    artifacts_dir = Path(__file__).resolve().parent / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load Datasets
    with open(data_dir / "training_dataset.json", "r", encoding="utf-8") as f:
        train_data = json.load(f)["samples"]

    with open(data_dir / "test_dataset.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)["samples"]

    with open(data_dir / "misconception_taxonomy.json", "r", encoding="utf-8") as f:
        taxonomies = json.load(f)["taxonomies"]
        taxonomy_map = {t["id"]: t for t in taxonomies}

    train_texts = [s["learner_response"] for s in train_data]
    train_codes = [s.get("question_code", "") for s in train_data]
    train_labels = [s["misconception_id"] for s in train_data]

    test_texts = [s["learner_response"] for s in test_data]
    test_codes = [s.get("question_code", "") for s in test_data]
    test_labels = [s["misconception_id"] for s in test_data]

    # 2. Train Calibrated Classifier
    classifier = MisconceptionClassifier()
    classifier.train(train_texts, train_codes, train_labels)

    # 3. Predict on Test Set
    test_preds = []
    test_probas = []
    for t, c in zip(test_texts, test_codes):
        diag = classifier.diagnose(t, c, taxonomy_map)
        test_preds.append(diag["predicted_id"])
        test_probas.append({cand["id"]: cand["probability"] for cand in diag["ranked_candidates"]})

    # 4. Evaluate Test Set
    all_classes = sorted(list(set(train_labels + test_labels)))
    evaluator = ModelEvaluator(classes=all_classes)
    test_metrics = evaluator.evaluate(test_labels, test_preds, test_probas)

    # 5. Evaluate Baseline Comparison
    X_train = classifier.feature_extractor.transform(train_texts, train_codes)
    X_test = classifier.feature_extractor.transform(test_texts, test_codes)
    y_train_binary = [s["correct"] for s in train_data]
    y_test_binary = [s["correct"] for s in test_data]

    baseline_metrics = evaluator.evaluate_baseline_comparison(
        X_train, y_train_binary,
        X_test, y_test_binary,
        relearn_macro_f1=test_metrics["macro_f1"],
        relearn_accuracy=test_metrics["accuracy"]
    )

    # 6. Save Artifacts
    full_report = {
        "dataset_statistics": {
            "training_samples": len(train_data),
            "test_samples": len(test_data),
            "num_classes": len(all_classes),
            "classes": all_classes
        },
        "test_metrics": test_metrics,
        "baseline_comparison": baseline_metrics
    }

    # Save trained classifier
    model_path = artifacts_dir / "model.joblib"
    joblib.dump(classifier, model_path)

    # Save metrics JSON
    metrics_path = artifacts_dir / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2)

    print("=" * 60)
    print("ReLearn ML Pipeline Training Completed Successfully")
    print(f"Training Samples: {len(train_data)} | Held-Out Test Samples: {len(test_data)}")
    print(f"Test Accuracy: {test_metrics['accuracy'] * 100:.2f}%")
    print(f"Macro F1 Score: {test_metrics['macro_f1']:.4f}")
    print(f"Weighted F1 Score: {test_metrics['weighted_f1']:.4f}")
    print(f"Model saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")
    print("=" * 60)

    return full_report

if __name__ == "__main__":
    run_training_pipeline()
