"""
Domain port (interface) for the investigator audit trail.

Defines the abstract contract that any audit-trail storage adapter
must implement. Application use-cases depend on this protocol,
enabling seamless swapping between in-memory, file-based or database
persistence without touching business logic.
"""

from typing import List, Protocol, runtime_checkable

from src.domain.entities.investigator_action import InvestigatorAction
from src.domain.entities.action_type import ActionType


@runtime_checkable
class AuditTrailPort(Protocol):
    """
    Abstract contract for managing the investigator action audit trail.

    Implementations must guarantee LIFO (last-in, first-out) semantics
    so the most recently recorded action is always the first to be reverted.
    """

    def record_action(self, action: InvestigatorAction) -> None:
        """Push a new action onto the audit trail."""
        ...

    def revert_last_action(self) -> InvestigatorAction:
        """Remove and return the most recent action (undo)."""
        ...

    def peek_last_action(self) -> InvestigatorAction:
        """Return the most recent action without removing it."""
        ...

    def get_full_history(self) -> List[InvestigatorAction]:
        """Return all recorded actions from most recent to oldest."""
        ...

    def find_actions_by_investigator(self, investigator_name: str) -> List[InvestigatorAction]:
        """Return all actions performed by a specific investigator."""
        ...

    def count_by_type(self, action_type: ActionType) -> int:
        """Count how many recorded actions match the given type."""
        ...

    def is_empty(self) -> bool:
        """Return True when no actions have been recorded."""
        ...

    def clear(self) -> None:
        """Erase all recorded actions."""
        ...
