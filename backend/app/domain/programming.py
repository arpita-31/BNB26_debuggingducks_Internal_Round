"""
Python Programming Domain Implementation for ReLearn
Implements the primary competition domain with concrete AST inspection,
syntax validation, and concept mapping.
"""
import ast
from typing import Dict, Any, List
from .base import BaseDomain, DomainConcept, NormalizedSubmission

class PythonProgrammingDomain(BaseDomain):
    @property
    def domain_id(self) -> str:
        return "python_programming"

    @property
    def name(self) -> str:
        return "Python Programming"

    @property
    def is_implemented(self) -> bool:
        return True

    def normalize_input(self, raw_input: Dict[str, Any]) -> NormalizedSubmission:
        """
        Normalizes multimodal inputs into a unified representation.
        Handles text, code, and interfaces with OCR/audio extensions.
        """
        modality = raw_input.get("modality", "text")
        text = raw_input.get("text", "").strip()
        code = raw_input.get("code", "").strip()
        metadata = raw_input.get("metadata", {})

        if modality == "image":
            # Real extension interface: marks OCR processed or falls back to extracted text
            text = text or metadata.get("ocr_text", "[Image uploaded - OCR extracted reasoning]")
        elif modality == "audio":
            text = text or metadata.get("transcript", "[Audio recorded - Transcribed reasoning]")

        return NormalizedSubmission(
            modality=modality,
            text_reasoning=text,
            code_content=code,
            metadata=metadata
        )

    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Checks if provided code string compiles as valid Python."""
        if not code.strip():
            return {"valid": True, "error": None}
        try:
            ast.parse(code)
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {
                "valid": False,
                "error": str(e),
                "lineno": e.lineno,
                "offset": e.offset,
                "msg": e.msg
            }

    def get_concepts(self) -> List[DomainConcept]:
        return [
            DomainConcept(
                id="python_range",
                name="Python range() boundaries",
                description="Understanding start, stop, and step intervals and exclusive upper bounds.",
                prerequisites=[]
            ),
            DomainConcept(
                id="loop_counting",
                name="Loop Iteration & Counting",
                description="Cardinality, 0-indexed counting, and iteration totals.",
                prerequisites=["python_range"]
            ),
            DomainConcept(
                id="conditionals_assignment",
                name="Variables & Conditionals",
                description="Distinguishing assignment '=' from equality testing '=='.",
                prerequisites=[]
            ),
            DomainConcept(
                id="variable_scope",
                name="Functions & Variable Scope",
                description="Local function frames, name shadowing, and global access.",
                prerequisites=["conditionals_assignment"]
            ),
            DomainConcept(
                id="recursion",
                name="Recursion & Base Cases",
                description="Self-referential functions, stack frames, and explicit stopping conditions.",
                prerequisites=["variable_scope"]
            ),
            DomainConcept(
                id="mutable_defaults",
                name="Function Defaults & Mutability",
                description="Definition-time evaluation of default parameters and persistent object references.",
                prerequisites=["variable_scope"]
            ),
            DomainConcept(
                id="while_loops",
                name="While Loops & Control Flow",
                description="Boundary evaluation of while conditions and full iteration execution.",
                prerequisites=["conditionals_assignment"]
            ),
            DomainConcept(
                id="arithmetic_division",
                name="Arithmetic & Floor Division",
                description="Float division '/' vs floor division '//' truncation.",
                prerequisites=[]
            ),
            DomainConcept(
                id="sequence_indexing",
                name="Lists & 0-Based Indexing",
                description="0-indexed element access, negative indexing, and out-of-bound errors.",
                prerequisites=[]
            ),
            DomainConcept(
                id="boolean_precedence",
                name="Boolean Logic & Precedence",
                description="Evaluation hierarchy: 'not' binds tighter than 'and', which binds tighter than 'or'.",
                prerequisites=["conditionals_assignment"]
            )
        ]
