"""
Infrastructure adapter: LinkedListEvidenceRegister.

Concrete implementation of EvidenceRegisterPort using a custom
singly-linked list for the forensic evidence chain of custody.
The linked list preserves the ordered, sequential nature of evidence
registration while making prepend (critical evidence) an O(1) operation.
"""

from typing import List, Optional

from src.domain.entities.forensic_evidence import ForensicEvidence
from src.domain.entities.evidence_type import EvidenceType
from src.domain.exceptions.investigation_errors import EvidenceNotFoundError


class _EvidenceNode:
    """Internal linked-list node wrapping a single ForensicEvidence item."""

    __slots__ = ("evidence", "next_node")

    def __init__(self, evidence: ForensicEvidence) -> None:
        self.evidence: ForensicEvidence = evidence
        self.next_node: Optional["_EvidenceNode"] = None


class LinkedListEvidenceRegister:
    """
    A singly-linked list that maintains the forensic chain of custody.

    Append is O(N) (maintained by a tail pointer to keep it O(1)).
    Prepend for critical evidence is O(1).
    Removal and lookup are O(N), which is acceptable for evidence registers
    where correctness and audit integrity matter more than raw speed.
    """

    def __init__(self) -> None:
        self.__head: Optional[_EvidenceNode] = None
        self.__tail: Optional[_EvidenceNode] = None
        self.__count: int = 0

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def append_evidence(self, evidence: ForensicEvidence) -> None:
        """
        Add evidence to the end of the register (O(1) with tail pointer).

        Args:
            evidence: A validated ForensicEvidence domain entity.

        Raises:
            TypeError: If the argument is not a ForensicEvidence instance.
        """
        self._validate_evidence(evidence)
        node = _EvidenceNode(evidence)
        if self.__tail is None:
            self.__head = self.__tail = node
        else:
            self.__tail.next_node = node
            self.__tail = node
        self.__count += 1

    def prepend_critical_evidence(self, evidence: ForensicEvidence) -> None:
        """
        Insert high-priority evidence at the front of the register (O(1)).

        Args:
            evidence: A validated ForensicEvidence domain entity.

        Raises:
            TypeError: If the argument is not a ForensicEvidence instance.
        """
        self._validate_evidence(evidence)
        node = _EvidenceNode(evidence)
        node.next_node = self.__head
        self.__head = node
        if self.__tail is None:
            self.__tail = node
        self.__count += 1

    def remove_evidence(self, evidence_id: str) -> None:
        """
        Remove an evidence item from the register by its unique identifier.

        Args:
            evidence_id: The unique ID of the evidence to remove.

        Raises:
            EvidenceNotFoundError: If no evidence with that ID exists.
        """
        if self.__head is None:
            raise EvidenceNotFoundError(
                f"Cannot remove: the evidence register is empty."
            )

        if self.__head.evidence.evidence_id == evidence_id:
            self.__head = self.__head.next_node
            if self.__head is None:
                self.__tail = None
            self.__count -= 1
            return

        current = self.__head
        while current.next_node is not None:
            if current.next_node.evidence.evidence_id == evidence_id:
                if current.next_node == self.__tail:
                    self.__tail = current
                current.next_node = current.next_node.next_node
                self.__count -= 1
                return
            current = current.next_node

        raise EvidenceNotFoundError(
            f"Evidence ID '{evidence_id}' not found in the register."
        )

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def find_by_id(self, evidence_id: str) -> ForensicEvidence:
        """
        Retrieve evidence by its unique identifier.

        Raises:
            EvidenceNotFoundError: If the ID does not exist.
        """
        for evidence in self:
            if evidence.evidence_id == evidence_id:
                return evidence
        raise EvidenceNotFoundError(
            f"Evidence ID '{evidence_id}' is not registered in the system."
        )

    def filter_by_agent(self, agent_name: str) -> List[ForensicEvidence]:
        """Return all evidence collected by a specific agent (case-insensitive)."""
        return [ev for ev in self if ev.collected_by.lower() == agent_name.lower()]

    def filter_by_type(self, evidence_type: EvidenceType) -> List[ForensicEvidence]:
        """Return all evidence of a given forensic category."""
        return [ev for ev in self if ev.evidence_type == evidence_type]

    def get_all(self) -> List[ForensicEvidence]:
        """Return the full ordered inventory of registered evidence."""
        return list(self)

    def is_empty(self) -> bool:
        """Return True when no evidence has been registered."""
        return self.__head is None

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_evidence(evidence: object) -> None:
        if not isinstance(evidence, ForensicEvidence):
            raise TypeError(
                f"Expected ForensicEvidence, got: {type(evidence).__name__}."
            )

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __iter__(self):
        current = self.__head
        while current is not None:
            yield current.evidence
            current = current.next_node

    def __len__(self) -> int:
        return self.__count

    def __str__(self) -> str:
        if self.is_empty():
            return "Forensic register: empty. No evidence on record."
        return f"Forensic register: {self.__count} item(s) under custody."
