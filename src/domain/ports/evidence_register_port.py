"""
Domain port (interface) for the forensic evidence register.

Defines the abstract contract for any storage implementation that manages
the chain-of-custody register for forensic evidence. Application use-cases
depend on this protocol, not on any concrete adapter.
"""

from typing import List, Protocol, runtime_checkable

from src.domain.entities.forensic_evidence import ForensicEvidence
from src.domain.entities.evidence_type import EvidenceType


@runtime_checkable
class EvidenceRegisterPort(Protocol):
    """
    Abstract contract for a forensic evidence register.

    Implementations manage the ordered list of evidence items and must
    support append, priority-prepend, remove, and filtering operations.
    """

    def append_evidence(self, evidence: ForensicEvidence) -> None:
        """Add evidence to the end of the register."""
        ...

    def prepend_critical_evidence(self, evidence: ForensicEvidence) -> None:
        """Insert high-priority evidence at the front of the register."""
        ...

    def remove_evidence(self, evidence_id: str) -> None:
        """Remove an evidence item by its unique identifier."""
        ...

    def find_by_id(self, evidence_id: str) -> ForensicEvidence:
        """Retrieve evidence by its unique identifier."""
        ...

    def filter_by_agent(self, agent_name: str) -> List[ForensicEvidence]:
        """Return all evidence collected by a specific agent."""
        ...

    def filter_by_type(self, evidence_type: EvidenceType) -> List[ForensicEvidence]:
        """Return all evidence of a given forensic category."""
        ...

    def get_all(self) -> List[ForensicEvidence]:
        """Return the full inventory of registered evidence."""
        ...

    def is_empty(self) -> bool:
        """Return True when no evidence has been registered."""
        ...
