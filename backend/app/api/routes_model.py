"""
Model Analytics and Metrics API Endpoints for ReLearn
Serves empirical ML performance data, confusion matrix, and taxonomy definitions.
No fabricated metrics; all data originates from evaluated test runs.
"""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/model", tags=["Model Analytics"])

@router.get("/metrics")
def get_model_metrics():
    """Returns actual evaluated metrics on the held-out test dataset."""
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    metrics_path = base_dir / "backend" / "app" / "ml" / "artifacts" / "metrics.json"

    if not metrics_path.exists():
        raise HTTPException(status_code=404, detail="Model metrics artifact not found. Please train model.")

    with open(metrics_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/confusion-matrix")
def get_confusion_matrix():
    """Returns confusion matrix array and class labels for UI heatmap visualization."""
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    metrics_path = base_dir / "backend" / "app" / "ml" / "artifacts" / "metrics.json"

    with open(metrics_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        test_metrics = data.get("test_metrics", {})
        return {
            "classes": test_metrics.get("classes", []),
            "matrix": test_metrics.get("confusion_matrix", []),
            "accuracy": test_metrics.get("accuracy"),
            "macro_f1": test_metrics.get("macro_f1")
        }

@router.get("/taxonomy")
def get_misconception_taxonomy():
    """Returns full formal misconception taxonomy."""
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    tax_path = base_dir / "data" / "misconception_taxonomy.json"
    with open(tax_path, "r", encoding="utf-8") as f:
        return json.load(f).get("taxonomies", [])
