"""
Domain entity: CriminalCase.

Represents a criminal case registered in the system awaiting assignment
to an investigator. The entity enforces domain invariants at construction
time and provides a clear, readable string representation.
"""

from dataclasses import dataclass

from src.domain.entities.case_priority import CasePriority


@dataclass
class CriminalCase:
    """
    A criminal case pending assignment within the investigation system.

    Attributes:
        case_id:               Unique identifier (e.g., "CASE-2024-001").
        case_title:            Descriptive title of the criminal event.
        case_priority:         Urgency level defined by CasePriority.
        assigned_investigator: Name of the assigned agent (empty if unassigned).
        registration_date:     ISO-formatted datetime "YYYY-MM-DD HH:MM:SS".
    """

    case_id: str
    case_title: str
    case_priority: CasePriority
    assigned_investigator: str
    registration_date: str

    def __post_init__(self) -> None:
        """Enforce domain invariants at construction time."""
        if not isinstance(self.case_priority, CasePriority):
            raise TypeError(
                f"case_priority must be a CasePriority instance, "
                f"got: {type(self.case_priority).__name__}."
            )
        self._require_non_blank("case_id", self.case_id)
        self._require_non_blank("case_title", self.case_title)
        self._require_non_blank("registration_date", self.registration_date)

    # ------------------------------------------------------------------
    # Business behaviour
    # ------------------------------------------------------------------

    def assign_to(self, investigator_name: str) -> None:
        """
        Assign this case to an investigator.

        Args:
            investigator_name: Full name of the investigator taking ownership.

        Raises:
            ValueError: If the name is blank or None.
        """
        self._require_non_blank("investigator_name", investigator_name)
        self.assigned_investigator = investigator_name

    def is_assigned(self) -> bool:
        """Return True when the case has been assigned to an investigator."""
        return bool(self.assigned_investigator and self.assigned_investigator.strip())

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
        investigator_label = (
            self.assigned_investigator if self.is_assigned() else "Unassigned"
        )
        return (
            f"Case #{self.case_id} | "
            f"Title: {self.case_title} | "
            f"Priority: {self.case_priority.name} | "
            f"Agent: {investigator_label} | "
            f"Registered: {self.registration_date}"
        )
