"""
Domain Registry for ReLearn
Manages registered academic domains and extension placeholders.
"""
from typing import Dict, List, Optional
from .base import BaseDomain, DomainConcept, NormalizedSubmission
from .programming import PythonProgrammingDomain

class MathematicsRoadmapDomain(BaseDomain):
    @property
    def domain_id(self) -> str:
        return "mathematics"

    @property
    def name(self) -> str:
        return "Mathematics (Calculus & Linear Algebra)"

    @property
    def is_implemented(self) -> bool:
        return False

    def normalize_input(self, raw_input: Dict) -> NormalizedSubmission:
        return NormalizedSubmission(
            modality=raw_input.get("modality", "text"),
            text_reasoning=raw_input.get("text", ""),
            metadata={"status": "Roadmap Extension"}
        )

    def validate_syntax(self, code: str) -> Dict:
        return {"valid": True, "note": "LaTeX / Math parser coming soon"}

    def get_concepts(self) -> List[DomainConcept]:
        return [
            DomainConcept(id="limit_boundary", name="Limits & Continuous Boundaries", description="Left vs right limits."),
            DomainConcept(id="matrix_mult", name="Matrix Non-Commutativity", description="AB != BA in matrix multiplication.")
        ]

class PhysicsRoadmapDomain(BaseDomain):
    @property
    def domain_id(self) -> str:
        return "physics"

    @property
    def name(self) -> str:
        return "Physics (Newtonian Mechanics)"

    @property
    def is_implemented(self) -> bool:
        return False

    def normalize_input(self, raw_input: Dict) -> NormalizedSubmission:
        return NormalizedSubmission(
            modality=raw_input.get("modality", "text"),
            text_reasoning=raw_input.get("text", ""),
            metadata={"status": "Roadmap Extension"}
        )

    def validate_syntax(self, code: str) -> Dict:
        return {"valid": True, "note": "Vector parser coming soon"}

    def get_concepts(self) -> List[DomainConcept]:
        return [
            DomainConcept(id="inertial_frames", name="Inertial Reference Frames", description="Velocity relative to observer."),
            DomainConcept(id="normal_force", name="Normal Force vs Weight", description="Action-reaction vs equilibrium forces.")
        ]

class DomainRegistry:
    def __init__(self):
        self._domains: Dict[str, BaseDomain] = {}
        self.register(PythonProgrammingDomain())
        self.register(MathematicsRoadmapDomain())
        self.register(PhysicsRoadmapDomain())

    def register(self, domain: BaseDomain):
        self._domains[domain.domain_id] = domain

    def get(self, domain_id: str) -> Optional[BaseDomain]:
        return self._domains.get(domain_id)

    def list_all(self) -> List[Dict]:
        return [
            {
                "id": d.domain_id,
                "name": d.name,
                "is_implemented": d.is_implemented,
                "concept_count": len(d.get_concepts())
            }
            for d in self._domains.values()
        ]

domain_registry = DomainRegistry()
