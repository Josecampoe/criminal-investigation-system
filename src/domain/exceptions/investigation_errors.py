"""
Domain exceptions for the Criminal Investigation System.

Each exception models a specific, named failure within the business domain.
They inherit from a common base (InvestigationError) so callers can catch
either the root or specific variants, following the Open/Closed Principle.
"""


class InvestigationError(Exception):
    """Base exception for all domain-level failures in the investigation system."""

    def __init__(self, message: str = "An investigation system error occurred.") -> None:
        super().__init__(message)


class EmptyAuditTrailError(InvestigationError):
    """
    Raised when an undo or peek operation is attempted on an empty audit trail.

    Signals that there are no recorded actions available to retrieve or revert.
    """

    def __init__(
        self,
        message: str = "The audit trail is empty. No actions available to process.",
    ) -> None:
        super().__init__(message)


class NoPendingCasesError(InvestigationError):
    """
    Raised when a case retrieval is attempted from an empty pending queue.

    Signals that there are no criminal cases awaiting assignment.
    """

    def __init__(
        self,
        message: str = "No pending cases. The case backlog is empty.",
    ) -> None:
        super().__init__(message)


class InvalidPriorityError(InvestigationError):
    """
    Raised when an unrecognised priority value is used for filtering or counting.

    Signals that the caller must supply a valid CasePriority enum member.
    """

    def __init__(
        self,
        message: str = "The supplied priority is not a valid CasePriority value.",
    ) -> None:
        super().__init__(message)


class EvidenceNotFoundError(InvestigationError):
    """
    Raised when a forensic evidence lookup fails to locate the requested item.

    Signals that no evidence with the given identifier exists in the register.
    """

    def __init__(
        self,
        message: str = "The requested evidence could not be found in the forensic register.",
    ) -> None:
        super().__init__(message)


class EventNotFoundError(InvestigationError):
    """
    Raised when a crime event lookup fails to locate the requested timeline entry.

    Signals that no event with the given identifier exists in the chronology.
    """

    def __init__(
        self,
        message: str = "The requested event could not be found in the crime timeline.",
    ) -> None:
        super().__init__(message)


class EmptyTimelineError(InvestigationError):
    """
    Raised when a navigation or read operation is attempted on an empty timeline.

    Signals that no crime events have been recorded yet.
    """

    def __init__(
        self,
        message: str = "The crime timeline is empty. No events have been recorded.",
    ) -> None:
        super().__init__(message)
