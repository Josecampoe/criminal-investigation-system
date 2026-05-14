"""
Domain ports (interfaces) for the case backlog.

Defines the abstract contract any case storage implementation must fulfil.
Using typing.Protocol enforces structural subtyping without requiring
concrete inheritance — the infrastructure adapters just need to match
the method signatures (Duck Typing + Dependency Inversion Principle).
"""

from typing import List, Protocol, runtime_checkable

from src.domain.entities.criminal_case import CriminalCase
from src.domain.entities.case_priority import CasePriority


@runtime_checkable
class CaseBacklogPort(Protocol):
    """
    Abstract contract for managing the backlog of pending criminal cases.

    Any concrete implementation (in-memory, database, message broker)
    must expose these methods. The application layer depends only on this
    protocol, never on a specific implementation.
    """

    def add_case(self, case: CriminalCase) -> None:
        """Append a case to the backlog."""
        ...

    def retrieve_next_case(self) -> CriminalCase:
        """Remove and return the oldest pending case (FIFO)."""
        ...

    def peek_next_case(self) -> CriminalCase:
        """Return the oldest pending case without removing it."""
        ...

    def get_all_pending(self) -> List[CriminalCase]:
        """Return an ordered snapshot of all pending cases."""
        ...

    def filter_by_priority(self, priority: CasePriority) -> List[CriminalCase]:
        """Return all cases matching the given priority level."""
        ...

    def count_by_priority(self, priority: CasePriority) -> int:
        """Count how many pending cases match the given priority level."""
        ...

    def is_empty(self) -> bool:
        """Return True when no pending cases exist."""
        ...

    def clear(self) -> None:
        """Remove all pending cases from the backlog."""
        ...
