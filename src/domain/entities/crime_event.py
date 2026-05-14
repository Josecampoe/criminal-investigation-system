"""
Domain entity: CrimeEvent.

Represents a chronological milestone within a criminal investigation.
Events are recorded in a doubly-linked timeline so investigators can
navigate forward and backward through the sequence of facts.
"""

from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any


@dataclass
class CrimeEvent:
    """
    A chronological fact recorded during a criminal investigation.

    Attributes:
        event_id:          Unique identifier for the event.
        event_title:       Short descriptive title of the event.
        event_description: Detailed narrative of what occurred.
        event_date:        Date/time of the event (YYYY-MM-DD HH:MM:SS).
        event_location:    Geographic location where the event occurred.
        involved_suspects: List of suspect names involved in this event.
    """

    event_id: str
    event_title: str
    event_description: str
    event_date: str
    event_location: str
    involved_suspects: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Enforce domain invariants at construction time."""
        for field_name, value in {
            "event_id": self.event_id,
            "event_title": self.event_title,
            "event_description": self.event_description,
            "event_date": self.event_date,
            "event_location": self.event_location,
        }.items():
            if not value or not value.strip():
                raise ValueError(f"'{field_name}' must not be blank.")

    # ------------------------------------------------------------------
    # Serialisation support
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a JSON-serialisable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CrimeEvent":
        """Reconstruct a CrimeEvent from a plain dictionary."""
        return cls(**data)

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"Event [{self.event_id}] | "
            f"{self.event_date} | "
            f"{self.event_title} | "
            f"Location: {self.event_location} | "
            f"Suspects: {len(self.involved_suspects)}"
        )
