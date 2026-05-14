"""
Application use case: CrimeChronology.

Orchestrates adding, navigating and querying crime events through
the CrimeTimelinePort abstraction.
"""

from typing import List, Optional, Set

from src.domain.entities.crime_event import CrimeEvent
from src.domain.ports.crime_timeline_port import CrimeTimelinePort


class CrimeChronology:
    """
    Manages the chronological reconstruction of criminal events.

    Responsibilities:
    - Add new events to the timeline (at the end or as the origin).
    - Navigate the timeline forward and backward.
    - Filter events and consolidate suspect lists.
    """

    def __init__(self, timeline: CrimeTimelinePort) -> None:
        self._timeline = timeline

    def add_event(self, event: CrimeEvent) -> None:
        """Append a new event to the end of the crime timeline."""
        self._timeline.add_event(event)

    def insert_founding_event(self, event: CrimeEvent) -> None:
        """Insert an event as the new origin of the investigation."""
        self._timeline.insert_founding_event(event)

    def remove_event(self, event_id: str) -> None:
        """Remove an erroneous or duplicate event from the timeline."""
        self._timeline.remove_event(event_id)

    def advance_focus(self) -> Optional[CrimeEvent]:
        """Move investigation focus to the next (later) event."""
        return self._timeline.advance()

    def rewind_focus(self) -> Optional[CrimeEvent]:
        """Move investigation focus to the previous (earlier) event."""
        return self._timeline.rewind()

    def get_current_event(self) -> CrimeEvent:
        """Return the event currently under investigation focus."""
        return self._timeline.get_current_event()

    def go_to_origin(self) -> CrimeEvent:
        """Move focus to the very first event in the timeline."""
        return self._timeline.go_to_origin()

    def go_to_latest(self) -> CrimeEvent:
        """Move focus to the most recent event in the timeline."""
        return self._timeline.go_to_latest()

    def search_by_location(self, location: str) -> List[CrimeEvent]:
        """Return all events that occurred at the specified location."""
        return self._timeline.filter_by_location(location)

    def get_all_suspects(self) -> Set[str]:
        """Return the consolidated set of all suspects across all events."""
        return self._timeline.get_all_suspects()

    def get_full_timeline(self) -> List[CrimeEvent]:
        """Return all events in chronological order."""
        return self._timeline.get_all_events()

    def is_timeline_empty(self) -> bool:
        """Return True when no events have been recorded."""
        return self._timeline.is_empty()
