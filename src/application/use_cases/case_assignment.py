"""
Application use case: CaseAssignment.

Orchestrates the full flow of registering a new criminal case
and assigning the next pending case to an available investigator.
Depends only on the CaseBacklogPort abstraction, never on a concrete adapter.
"""

from typing import List

from src.domain.entities.criminal_case import CriminalCase
from src.domain.entities.case_priority import CasePriority
from src.domain.ports.case_backlog_port import CaseBacklogPort


class CaseAssignment:
    """
    Manages the criminal case assignment workflow.

    Responsibilities:
    - Accept and validate incoming cases into the backlog.
    - Retrieve the next pending case and assign it to an investigator.
    - Provide inspection views (pending list, priority filters, counts).
    """

    def __init__(self, case_backlog: CaseBacklogPort) -> None:
        self._backlog = case_backlog

    def register_case(self, case: CriminalCase) -> None:
        """Add a new criminal case to the pending backlog."""
        self._backlog.add_case(case)

    def assign_next_to(self, investigator_name: str) -> CriminalCase:
        """
        Retrieve and assign the next pending case to an investigator.

        Args:
            investigator_name: Full name of the investigator taking the case.

        Returns:
            The CriminalCase that was assigned.

        Raises:
            NoPendingCasesError: If the backlog is empty.
            ValueError: If investigator_name is blank.
        """
        case = self._backlog.retrieve_next_case()
        case.assign_to(investigator_name)
        return case

    def peek_next_case(self) -> CriminalCase:
        """Return the next case to be assigned without removing it."""
        return self._backlog.peek_next_case()

    def get_all_pending(self) -> List[CriminalCase]:
        """Return an ordered snapshot of all pending cases."""
        return self._backlog.get_all_pending()

    def filter_by_priority(self, priority: CasePriority) -> List[CriminalCase]:
        """Return all pending cases with the given priority level."""
        return self._backlog.filter_by_priority(priority)

    def count_by_priority(self, priority: CasePriority) -> int:
        """Count pending cases matching the given priority."""
        return self._backlog.count_by_priority(priority)

    def is_backlog_empty(self) -> bool:
        """Return True when no pending cases remain."""
        return self._backlog.is_empty()

    def clear_backlog(self) -> None:
        """Remove all pending cases (administrative reset)."""
        self._backlog.clear()
