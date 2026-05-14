"""
Domain port (interface) for the crime event timeline.

Defines the abstract contract for any implementation managing
a navigable chronological timeline of crime events. Application
use-cases depend on this protocol, not on specific data structures.
"""

from typing import List, Optional, Protocol, Set, runtime_checkable

from src.domain.entities.crime_event import CrimeEvent


@runtime_checkable
class CrimeTimelinePort(Protocol):
    """
    Abstract contract for navigating and managing a crime event timeline.

    The timeline provides bidirectional traversal (forward/backward),
    event insertion at the front or back, removal, and filtering.
    """

    def add_event(self, event: CrimeEvent) -> None:
        """Append a new event to the end of the timeline."""
        ...

    def insert_founding_event(self, event: CrimeEvent) -> None:
        """Insert an event at the beginning of the timeline (origin point)."""
        ...

    def remove_event(self, event_id: str) -> None:
        """Remove an event from the timeline by its identifier."""
        ...

    def advance(self) -> Optional[CrimeEvent]:
        """Move the investigation focus forward in time; return the new event."""
        ...

    def rewind(self) -> Optional[CrimeEvent]:
        """Move the investigation focus backward in time; return the event."""
        ...

    def get_current_event(self) -> CrimeEvent:
        """Return the event currently under investigation focus."""
        ...

    def go_to_origin(self) -> CrimeEvent:
        """Move focus to the very first event in the timeline."""
        ...

    def go_to_latest(self) -> CrimeEvent:
        """Move focus to the most recent event in the timeline."""
        ...

    def filter_by_location(self, location: str) -> List[CrimeEvent]:
        """Return all events that occurred in the specified location."""
        ...

    def get_all_suspects(self) -> Set[str]:
        """Return a de-duplicated set of all suspects across the timeline."""
        ...

    def get_all_events(self) -> List[CrimeEvent]:
        """Return all events in chronological order."""
        ...

    def is_empty(self) -> bool:
        """Return True when no events have been recorded."""
        ...
