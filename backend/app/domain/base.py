"""
Domain Abstraction Layer for ReLearn
Allows the cognitive diagnostic architecture to scale from Python Programming
to Mathematics, Physics, and SQL without re-architecting the core loop.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class DomainConcept(BaseModel):
    id: str
    name: str
    description: str
    prerequisites: List[str] = Field(default_factory=list)

class NormalizedSubmission(BaseModel):
    modality: str = "text"  # "text", "code", "image", "audio"
    text_reasoning: str = ""
    code_content: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseDomain(ABC):
    @property
    @abstractmethod
    def domain_id(self) -> str:
        """Unique domain identifier (e.g., 'python_programming', 'mathematics')."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable domain name."""
        pass

    @property
    @abstractmethod
    def is_implemented(self) -> bool:
        """Indicates whether this domain is fully implemented or a roadmap extension."""
        pass

    @abstractmethod
    def normalize_input(self, raw_input: Dict[str, Any]) -> NormalizedSubmission:
        """Transforms raw multimodal submission into normalized representation."""
        pass

    @abstractmethod
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validates domain-specific syntax or expression correctness."""
        pass

    @abstractmethod
    def get_concepts(self) -> List[DomainConcept]:
        """Returns the list of core concepts covered in this domain."""
        pass
