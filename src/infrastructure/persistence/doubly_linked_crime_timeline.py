"""
Infrastructure adapter: DoublyLinkedCrimeTimeline.

Concrete implementation of CrimeTimelinePort using a custom doubly-linked
list, enabling O(1) forward and backward navigation between crime events.
A separate 'focus' pointer tracks the event currently under investigation
without modifying the list structure.
"""

import json
import os
from typing import List, Optional, Set

from src.domain.entities.crime_event import CrimeEvent
from src.domain.exceptions.investigation_errors import EventNotFoundError, EmptyTimelineError


class _TimelineNode:
    """Internal doubly-linked node wrapping a single CrimeEvent."""

    __slots__ = ("event", "previous_node", "next_node")

    def __init__(self, event: CrimeEvent) -> None:
        self.event: CrimeEvent = event
        self.previous_node: Optional["_TimelineNode"] = None
        self.next_node: Optional["_TimelineNode"] = None


class DoublyLinkedCrimeTimeline:
    """
    A navigable doubly-linked crime event timeline.

    Investigators can move their analysis focus forward (toward the most
    recent events) or backward (toward the origin of the case) in O(1)
    time. Insertion and removal are also supported.
    """

    def __init__(self) -> None:
        self.__origin: Optional[_TimelineNode] = None
        self.__latest: Optional[_TimelineNode] = None
        self.__focus: Optional[_TimelineNode] = None
        self.__count: int = 0

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def add_event(self, event: CrimeEvent) -> None:
        """
        Append a new event to the end of the timeline (O(1)).

        Args:
            event: A validated CrimeEvent domain entity.

        Raises:
            TypeError: If the argument is not a CrimeEvent instance.
        """
        self._validate_event(event)
        node = _TimelineNode(event)
        if self.is_empty():
            self.__origin = self.__latest = self.__focus = node
        else:
            node.previous_node = self.__latest
            self.__latest.next_node = node
            self.__latest = node
        self.__count += 1

    def insert_founding_event(self, event: CrimeEvent) -> None:
        """
        Insert an event at the very beginning of the timeline (O(1)).

        Args:
            event: A validated CrimeEvent domain entity.

        Raises:
            TypeError: If the argument is not a CrimeEvent instance.
        """
        self._validate_event(event)
        node = _TimelineNode(event)
        if self.is_empty():
            self.__origin = self.__latest = self.__focus = node
        else:
            node.next_node = self.__origin
            self.__origin.previous_node = node
            self.__origin = node
        self.__count += 1

    def remove_event(self, event_id: str) -> None:
        """
        Remove an event by its unique identifier.

        Raises:
            EmptyTimelineError: If the timeline has no events.
            EventNotFoundError: If the event_id does not exist.
        """
        if self.is_empty():
            raise EmptyTimelineError()

        current = self.__origin
        while current is not None:
            if current.event.event_id == event_id:
                self._unlink_node(current)
                self.__count -= 1
                return
            current = current.next_node

        raise EventNotFoundError(
            f"Event ID '{event_id}' was not found in the timeline."
        )

    # ------------------------------------------------------------------
    # Navigation operations
    # ------------------------------------------------------------------

    def advance(self) -> Optional[CrimeEvent]:
        """
        Move the investigation focus forward; return the new event or None
        if already at the end of the timeline.
        """
        self._require_non_empty()
        if self.__focus.next_node is not None:
            self.__focus = self.__focus.next_node
            return self.__focus.event
        return None

    def rewind(self) -> Optional[CrimeEvent]:
        """
        Move the investigation focus backward; return the event or None
        if already at the timeline origin.
        """
        self._require_non_empty()
        if self.__focus.previous_node is not None:
            self.__focus = self.__focus.previous_node
            return self.__focus.event
        return None

    def get_current_event(self) -> CrimeEvent:
        """Return the event currently under investigation focus."""
        self._require_non_empty()
        return self.__focus.event

    def go_to_origin(self) -> CrimeEvent:
        """Move focus to the first event in the timeline."""
        self._require_non_empty()
        self.__focus = self.__origin
        return self.__focus.event

    def go_to_latest(self) -> CrimeEvent:
        """Move focus to the most recent event in the timeline."""
        self._require_non_empty()
        self.__focus = self.__latest
        return self.__focus.event

    # ------------------------------------------------------------------
    # Read / filter operations
    # ------------------------------------------------------------------

    def filter_by_location(self, location: str) -> List[CrimeEvent]:
        """Return all events matching the given location (case-insensitive)."""
        return [e for e in self if location.lower() in e.event_location.lower()]

    def get_all_suspects(self) -> Set[str]:
        """Return a de-duplicated set of suspects across all timeline events."""
        suspects: Set[str] = set()
        for event in self:
            suspects.update(event.involved_suspects)
        return suspects

    def get_all_events(self) -> List[CrimeEvent]:
        """Return all events in chronological order."""
        return list(self)

    def is_empty(self) -> bool:
        """Return True when no events have been recorded."""
        return self.__origin is None

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def save_to_json(self, filepath: str) -> None:
        """Persist the timeline to a JSON file."""
        data = [event.to_dict() for event in self]
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_from_json(self, filepath: str) -> None:
        """Load timeline events from a JSON file (skips if file not found)."""
        if not os.path.exists(filepath):
            return
        with open(filepath, "r", encoding="utf-8") as file:
            for record in json.load(file):
                self.add_event(CrimeEvent.from_dict(record))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_event(self, event: object) -> None:
        if not isinstance(event, CrimeEvent):
            raise TypeError(
                f"Expected CrimeEvent, got: {type(event).__name__}."
            )

    def _require_non_empty(self) -> None:
        if self.is_empty():
            raise EmptyTimelineError()

    def _unlink_node(self, node: _TimelineNode) -> None:
        """Detach a node from the doubly-linked structure and repair pointers."""
        if self.__count == 1:
            self.__origin = self.__latest = self.__focus = None
        elif node == self.__origin:
            self.__origin = node.next_node
            self.__origin.previous_node = None
            if self.__focus == node:
                self.__focus = self.__origin
        elif node == self.__latest:
            self.__latest = node.previous_node
            self.__latest.next_node = None
            if self.__focus == node:
                self.__focus = self.__latest
        else:
            node.previous_node.next_node = node.next_node
            node.next_node.previous_node = node.previous_node
            if self.__focus == node:
                self.__focus = node.next_node

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __iter__(self):
        current = self.__origin
        while current is not None:
            yield current.event
            current = current.next_node

    def __len__(self) -> int:
        return self.__count

    def __str__(self) -> str:
        if self.is_empty():
            return "Crime timeline: empty. No events recorded."
        return (
            f"Crime timeline: {self.__count} event(s). "
            f"Origin: '{self.__origin.event.event_title}'."
        )
