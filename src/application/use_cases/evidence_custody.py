"""
Application use case: EvidenceCustody.

Orchestrates adding, removing and querying forensic evidence
through the EvidenceRegisterPort abstraction.
"""

from typing import List

from src.domain.entities.forensic_evidence import ForensicEvidence
from src.domain.entities.evidence_type import EvidenceType
from src.domain.ports.evidence_register_port import EvidenceRegisterPort


class EvidenceCustody:
    """
    Manages the forensic evidence chain-of-custody workflow.

    Responsibilities:
    - Register standard and critical (priority) evidence items.
    - Remove invalidated evidence entries.
    - Provide lookup and filtering operations for investigators.
    """

    def __init__(self, evidence_register: EvidenceRegisterPort) -> None:
        self._register = evidence_register

    def register_evidence(self, evidence: ForensicEvidence) -> None:
        """Append a standard evidence item to the chain of custody."""
        self._register.append_evidence(evidence)

    def register_critical_evidence(self, evidence: ForensicEvidence) -> None:
        """Prepend a high-priority evidence item for immediate attention."""
        self._register.prepend_critical_evidence(evidence)

    def invalidate_evidence(self, evidence_id: str) -> None:
        """Remove a compromised or invalidated evidence entry."""
        self._register.remove_evidence(evidence_id)

    def find_evidence(self, evidence_id: str) -> ForensicEvidence:
        """Retrieve a specific evidence item by its unique ID."""
        return self._register.find_by_id(evidence_id)

    def get_evidence_by_agent(self, agent_name: str) -> List[ForensicEvidence]:
        """Return all evidence collected by a specific forensic agent."""
        return self._register.filter_by_agent(agent_name)

    def get_evidence_by_type(self, evidence_type: EvidenceType) -> List[ForensicEvidence]:
        """Return all evidence of a given forensic category."""
        return self._register.filter_by_type(evidence_type)

    def get_full_inventory(self) -> List[ForensicEvidence]:
        """Return the complete ordered inventory of registered evidence."""
        return self._register.get_all()

    def is_register_empty(self) -> bool:
        """Return True when no evidence has been registered."""
        return self._register.is_empty()
