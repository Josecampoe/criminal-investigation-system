"""
Infrastructure adapter: InMemoryCaseBacklog.

Concrete implementation of CaseBacklogPort using a collections.deque
for O(1) enqueue and dequeue operations, replacing the original O(N)
list.pop(0) approach. This adapter is suitable for testing and
lightweight in-process executions.
"""

from collections import deque
from typing import List

from src.domain.entities.criminal_case import CriminalCase
from src.domain.entities.case_priority import CasePriority
from src.domain.exceptions.investigation_errors import NoPendingCasesError, InvalidPriorityError


class InMemoryCaseBacklog:
    """
    Manages a FIFO backlog of pending criminal cases stored in process memory.

    Uses collections.deque to guarantee O(1) complexity for both
    add_case (right-append) and retrieve_next_case (left-pop) operations,
    correcting the O(N) performance defect of the original list implementation.
    """

    def __init__(self) -> None:
        self.__pending: deque[CriminalCase] = deque()

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def add_case(self, case: CriminalCase) -> None:
        """
        Append a case to the end of the pending backlog.

        Args:
            case: A validated CriminalCase domain entity.

        Raises:
            TypeError: If the argument is not a CriminalCase instance.
        """
        if not isinstance(case, CriminalCase):
            raise TypeError(
                f"Expected CriminalCase, got: {type(case).__name__}."
            )
        self.__pending.append(case)

    def retrieve_next_case(self) -> CriminalCase:
        """
        Remove and return the oldest pending case (FIFO / O(1)).

        Raises:
            NoPendingCasesError: When the backlog is empty.
        """
        if self.is_empty():
            raise NoPendingCasesError()
        return self.__pending.popleft()

    def clear(self) -> None:
        """Remove all pending cases from the backlog."""
        self.__pending.clear()

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def peek_next_case(self) -> CriminalCase:
        """
        Return the oldest pending case without removing it.

        Raises:
            NoPendingCasesError: When the backlog is empty.
        """
        if self.is_empty():
            raise NoPendingCasesError()
        return self.__pending[0]

    def get_all_pending(self) -> List[CriminalCase]:
        """Return an ordered snapshot (oldest first) of all pending cases."""
        return list(self.__pending)

    def filter_by_priority(self, priority: CasePriority) -> List[CriminalCase]:
        """
        Return all pending cases matching the given priority level.

        Args:
            priority: A valid CasePriority enum member.

        Raises:
            InvalidPriorityError: If the supplied value is not a CasePriority.
        """
        self._validate_priority(priority)
        return [case for case in self.__pending if case.case_priority == priority]

    def count_by_priority(self, priority: CasePriority) -> int:
        """
        Count pending cases matching the given priority.

        Raises:
            InvalidPriorityError: If the supplied value is not a CasePriority.
        """
        self._validate_priority(priority)
        return sum(1 for case in self.__pending if case.case_priority == priority)

    def is_empty(self) -> bool:
        """Return True when no pending cases exist."""
        return len(self.__pending) == 0

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_priority(priority: object) -> None:
        if not isinstance(priority, CasePriority):
            raise InvalidPriorityError(
                f"'{priority}' is not a valid CasePriority. "
                "Use CasePriority.LOW, MEDIUM, HIGH, or CRITICAL."
            )

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self.__pending)

    def __str__(self) -> str:
        if self.is_empty():
            return "Case backlog: empty. No pending cases."
        next_case = self.__pending[0]
        return (
            f"Case backlog: {len(self.__pending)} pending case(s). "
            f"Next: [{next_case.case_id}] {next_case.case_title} "
            f"(Priority: {next_case.case_priority.name})."
        )
