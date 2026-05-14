"""
Infrastructure adapter: InMemoryAuditTrail.

Concrete LIFO implementation of AuditTrailPort using a plain Python list.
For LIFO (Stack) semantics, list.append() and list.pop() are both O(1),
making this the correct and optimal data structure for an audit trail.

Business-query methods (search by investigator, count by type) are correctly
isolated here in the infrastructure layer, not mixed into the storage structure.
"""

from typing import List

from src.domain.entities.investigator_action import InvestigatorAction
from src.domain.entities.action_type import ActionType
from src.domain.exceptions.investigation_errors import EmptyAuditTrailError


class InMemoryAuditTrail:
    """
    Manages the investigator action audit trail in process memory (LIFO).

    Records investigative operations chronologically and supports
    reverting the most recent action in O(1) time.
    """

    def __init__(self) -> None:
        self.__trail: List[InvestigatorAction] = []

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def record_action(self, action: InvestigatorAction) -> None:
        """
        Push a new action onto the audit trail.

        Args:
            action: A validated InvestigatorAction domain entity.

        Raises:
            TypeError: If the argument is not an InvestigatorAction instance.
        """
        if not isinstance(action, InvestigatorAction):
            raise TypeError(
                f"Expected InvestigatorAction, got: {type(action).__name__}."
            )
        self.__trail.append(action)

    def revert_last_action(self) -> InvestigatorAction:
        """
        Remove and return the most recently recorded action (undo / O(1)).

        Raises:
            EmptyAuditTrailError: When no actions have been recorded.
        """
        if self.is_empty():
            raise EmptyAuditTrailError()
        return self.__trail.pop()

    def clear(self) -> None:
        """Erase all recorded actions from the trail."""
        self.__trail.clear()

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def peek_last_action(self) -> InvestigatorAction:
        """
        Return the most recent action without removing it.

        Raises:
            EmptyAuditTrailError: When no actions have been recorded.
        """
        if self.is_empty():
            raise EmptyAuditTrailError()
        return self.__trail[-1]

    def get_full_history(self) -> List[InvestigatorAction]:
        """Return all recorded actions ordered from most recent to oldest."""
        return list(reversed(self.__trail))

    def find_actions_by_investigator(self, investigator_name: str) -> List[InvestigatorAction]:
        """
        Return all actions performed by a specific investigator (most recent first).

        Args:
            investigator_name: Full name of the investigator to search for.

        Raises:
            ValueError: If the name is blank or None.
        """
        if not investigator_name or not investigator_name.strip():
            raise ValueError("investigator_name must not be blank.")
        matching = [
            action for action in self.__trail
            if action.investigator_name == investigator_name
        ]
        return list(reversed(matching))

    def count_by_type(self, action_type: ActionType) -> int:
        """
        Count how many recorded actions match the given type.

        Args:
            action_type: A valid ActionType enum member.

        Raises:
            TypeError: If the argument is not an ActionType instance.
        """
        if not isinstance(action_type, ActionType):
            raise TypeError(
                f"Expected ActionType, got: {type(action_type).__name__}."
            )
        return sum(1 for action in self.__trail if action.action_type == action_type)

    def is_empty(self) -> bool:
        """Return True when no actions have been recorded."""
        return len(self.__trail) == 0

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self.__trail)

    def __str__(self) -> str:
        if self.is_empty():
            return "Audit trail: empty. No actions recorded."
        top = self.__trail[-1]
        return (
            f"Audit trail: {len(self.__trail)} action(s) recorded. "
            f"Latest: [{top.action_type.value}] by {top.investigator_name}."
        )
