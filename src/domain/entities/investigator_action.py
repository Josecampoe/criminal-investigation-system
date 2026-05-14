"""
Domain entity: InvestigatorAction.

Represents a single auditable operation performed by an investigator
during the lifecycle of a criminal case. Instances are immutable to
guarantee the integrity of the audit trail — once recorded, an action
cannot be silently modified.
"""

from dataclasses import dataclass

from src.domain.entities.action_type import ActionType


@dataclass(frozen=True)
class InvestigatorAction:
    """
    Immutable record of a single investigative operation.

    An InvestigatorAction captures who did what, when, and why.
    Immutability via frozen=True ensures that once an action is
    pushed onto the audit trail, its data cannot be altered.

    Attributes:
        action_id:         Unique identifier (e.g., "ACT-001").
        action_type:       Category of operation performed.
        description:       Human-readable explanation of what was done.
        investigator_name: Full name of the responsible agent.
        timestamp:         ISO-formatted datetime string "YYYY-MM-DD HH:MM:SS".
    """

    action_id: str
    action_type: ActionType
    description: str
    investigator_name: str
    timestamp: str

    def __post_init__(self) -> None:
        """Enforce domain invariants at construction time."""
        if not isinstance(self.action_type, ActionType):
            raise TypeError(
                f"action_type must be an ActionType instance, "
                f"got: {type(self.action_type).__name__}."
            )
        self._require_non_blank("action_id", self.action_id)
        self._require_non_blank("description", self.description)
        self._require_non_blank("investigator_name", self.investigator_name)
        self._require_non_blank("timestamp", self.timestamp)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _require_non_blank(field_name: str, value: str) -> None:
        """Raise ValueError when a required text field is blank or None."""
        if not value or not value.strip():
            raise ValueError(f"'{field_name}' must not be blank.")

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"[{self.timestamp}] Action #{self.action_id} | "
            f"Type: {self.action_type.value} | "
            f"Agent: {self.investigator_name} | "
            f"Details: {self.description}"
        )
