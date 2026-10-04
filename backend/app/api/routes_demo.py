"""
Demo Mode API Endpoints for ReLearn
Provides 5 preset competition-ready scenarios that walk judges through
the closed-loop diagnostic, intervention, and empirical reassessment pipeline.
All executions flow through the actual ML and database pipeline.
"""
from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/api/demo", tags=["Demo Mode"])

DEMO_SCENARIOS = [
    {
        "id": "scenario_range_endpoint",
        "title": "Scenario 1: Range Endpoint Inclusion (M001)",
        "domain": "python_programming",
        "concept": "Python range() boundaries",
        "question_id": "Q_PY_RANGE_01",
        "misconception_id": "M001",
        "description": "Learner incorrectly predicts that range(1, 5) generates 5 numbers [1, 2, 3, 4, 5], believing the upper bound is inclusive.",
        "student_submission": {
            "modality": "text+code",
            "text": "The loop will print 1, 2, 3, 4, 5 because range(1, 5) includes both the start and ending values.",
            "code": ""
        },
        "transfer_question_id": "Q_TRANS_M001_01",
        "transfer_submission_correct": {
            "text": "The output is 2, 3, 4, 5 because in Python range(2, 6) the upper bound 6 is excluded.",
            "code": ""
        }
    },
    {
        "id": "scenario_off_by_one",
        "title": "Scenario 2: Off-by-One Loop Count (M002)",
        "domain": "python_programming",
        "concept": "Loop Iteration & Counting",
        "question_id": "Q_PY_COUNT_01",
        "misconception_id": "M002",
        "description": "Learner miscounts total loop iterations by confounding 0-based indexing with cardinality (predicting 6 executions instead of 5).",
        "student_submission": {
            "modality": "text+code",
            "text": "The loop runs 6 times because it starts counting at 0 and goes up through 5.",
            "code": ""
        },
        "transfer_question_id": "Q_TRANS_M002_01",
        "transfer_submission_correct": {
            "text": "The loop runs exactly 4 times and prints 0, 1, 2, 3.",
            "code": ""
        }
    },
    {
        "id": "scenario_assign_vs_equality",
        "title": "Scenario 3: Assignment vs Equality (M003)",
        "domain": "python_programming",
        "concept": "Variables & Conditionals",
        "question_id": "Q_PY_ASSIGN_01",
        "misconception_id": "M003",
        "description": "Learner assumes single '=' in an if-condition tests equality rather than raising a SyntaxError in Python.",
        "student_submission": {
            "modality": "text+code",
            "text": "It checks if status is admin and prints Access Granted because single equals compares the values.",
            "code": "if status = 'admin':"
        },
        "transfer_question_id": "Q_TRANS_M003_01",
        "transfer_submission_correct": {
            "text": "Change = to == because == is the comparison operator for equality in conditionals.",
            "code": "if score == 100:"
        }
    },
    {
        "id": "scenario_recursion_base_case",
        "title": "Scenario 4: Missing Recursion Base Case (M005)",
        "domain": "python_programming",
        "concept": "Recursion",
        "question_id": "Q_PY_RECURSION_01",
        "misconception_id": "M005",
        "description": "Learner believes recursion naturally terminates when a counter reaches zero, without an explicit base case guard.",
        "student_submission": {
            "modality": "text+code",
            "text": "The function counts down 3, 2, 1, 0 and naturally stops at 0 returning None.",
            "code": ""
        },
        "transfer_question_id": "Q_TRANS_M005_01",
        "transfer_submission_correct": {
            "text": "Needs an explicit base case: if n <= 1: return 1 to halt the recursive call stack.",
            "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
        }
    },
    {
        "id": "scenario_variable_scope",
        "title": "Scenario 5: Variable Scope Shadowing (M004)",
        "domain": "python_programming",
        "concept": "Functions & Variable Scope",
        "question_id": "Q_PY_SCOPE_01",
        "misconception_id": "M004",
        "description": "Learner assumes local variable assignment permanently mutates the enclosing global variable.",
        "student_submission": {
            "modality": "text+code",
            "text": "Both print 50 because calling update() modifies val globally to 50.",
            "code": ""
        },
        "transfer_question_id": "Q_TRANS_M004_01",
        "transfer_submission_correct": {
            "text": "Outer counter remains 5 because the local assignment inside increment() only creates a local variable.",
            "code": ""
        }
    }
]

@router.get("/scenarios")
def get_demo_scenarios() -> List[Dict[str, Any]]:
    """Returns curated competition demo scenarios."""
    return DEMO_SCENARIOS
