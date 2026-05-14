"""
Domain enumeration for types of investigator actions.

Each value describes a specific forensic or administrative
operation that an investigator performs during a case lifecycle.
These values are recorded in the audit trail and support undo operations.
"""

from enum import Enum


class ActionType(Enum):
    """
    Represents the possible investigative operations an agent can perform.

    Values:
        ADD_SUSPECT:    Register a new suspect in a case.
        REMOVE_SUSPECT: Remove an existing suspect from a case.
        ADD_EVIDENCE:   Register a new piece of evidence.
        LINK_EVIDENCE:  Associate evidence with a suspect or case.
        OPEN_CASE:      Open a new criminal investigation.
        CLOSE_CASE:     Mark a case as resolved and close it.
    """

    ADD_SUSPECT = "ADD_SUSPECT"
    REMOVE_SUSPECT = "REMOVE_SUSPECT"
    ADD_EVIDENCE = "ADD_EVIDENCE"
    LINK_EVIDENCE = "LINK_EVIDENCE"
    OPEN_CASE = "OPEN_CASE"
    CLOSE_CASE = "CLOSE_CASE"
