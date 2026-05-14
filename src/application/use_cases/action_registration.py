"""
Application use case: ActionRegistration.

Orchestrates recording investigative actions and reverting them.
Depends only on AuditTrailPort, never on a concrete adapter.
"""

from typing import List

from src.domain.entities.investigator_action import InvestigatorAction
from src.domain.entities.action_type import ActionType
from src.domain.ports.audit_trail_port import AuditTrailPort


class ActionRegistration:
    """
    Manages the investigator audit trail workflow.

    Responsibilities:
    - Record new investigative actions onto the audit trail.
    - Revert (undo) the most recently recorded action.
    - Provide history inspection and statistical queries.
    """

    def __init__(self, audit_trail: AuditTrailPort) -> None:
        self._trail = audit_trail

    def record_action(self, action: InvestigatorAction) -> None:
        """Push a new action onto the audit trail."""
        self._trail.record_action(action)

    def revert_last_action(self) -> InvestigatorAction:
        """
        Undo the most recent action.

        Returns:
            The action that was reverted.

        Raises:
            EmptyAuditTrailError: If no actions have been recorded.
        """
        return self._trail.revert_last_action()

    def peek_last_action(self) -> InvestigatorAction:
        """Return the most recent action without reverting it."""
        return self._trail.peek_last_action()

    def get_full_history(self) -> List[InvestigatorAction]:
        """Return all recorded actions from most recent to oldest."""
        return self._trail.get_full_history()

    def find_by_investigator(self, investigator_name: str) -> List[InvestigatorAction]:
        """Return all actions performed by a specific investigator."""
        return self._trail.find_actions_by_investigator(investigator_name)

    def count_by_type(self, action_type: ActionType) -> int:
        """Count recorded actions of a specific type."""
        return self._trail.count_by_type(action_type)

    def is_trail_empty(self) -> bool:
        """Return True when no actions have been recorded."""
        return self._trail.is_empty()

    def clear_trail(self) -> None:
        """Erase all recorded actions (administrative reset)."""
        self._trail.clear()
