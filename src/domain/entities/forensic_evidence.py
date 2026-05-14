"""
Domain entity: ForensicEvidence.

Represents a single immutable piece of forensic evidence collected
during a criminal investigation. Immutability preserves chain-of-custody
integrity — once registered, evidence data cannot be silently altered.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any

from src.domain.entities.evidence_type import EvidenceType


@dataclass(frozen=True)
class ForensicEvidence:
    """
    An immutable, legally registered unit of forensic evidence.

    Attributes:
        evidence_id:     Unique identifier for the evidence item.
        evidence_type:   Forensic category of the evidence.
        description:     Detailed description of the item collected.
        collection_date: Date the evidence was collected (YYYY-MM-DD).
        collected_by:    Name of the forensic agent who collected it.
    """

    evidence_id: str
    evidence_type: EvidenceType
    description: str
    collection_date: str
    collected_by: str

    def __post_init__(self) -> None:
        """Enforce domain invariants at construction time."""
        if not isinstance(self.evidence_type, EvidenceType):
            raise TypeError(
                f"evidence_type must be an EvidenceType instance, "
                f"got: {type(self.evidence_type).__name__}."
            )
        for field, value in {
            "evidence_id": self.evidence_id,
            "description": self.description,
            "collection_date": self.collection_date,
            "collected_by": self.collected_by,
        }.items():
            if not value or not value.strip():
                raise ValueError(f"'{field}' must not be blank.")

    # ------------------------------------------------------------------
    # Serialisation support
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Convert evidence to a JSON-serialisable dictionary."""
        data = asdict(self)
        data["evidence_type"] = self.evidence_type.name
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ForensicEvidence":
        """Reconstruct a ForensicEvidence instance from a dictionary."""
        payload = data.copy()
        payload["evidence_type"] = EvidenceType[payload["evidence_type"]]
        return cls(**payload)

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"Evidence [{self.evidence_id}] | "
            f"Type: {self.evidence_type.value} | "
            f"Date: {self.collection_date} | "
            f"Agent: {self.collected_by}"
        )
