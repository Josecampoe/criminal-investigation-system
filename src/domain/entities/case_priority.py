"""
Domain enumeration for criminal case priority levels.

Defines the urgency scale for classifying criminal cases
within the investigation system. Higher integer values
represent greater urgency and faster response requirements.
"""

from enum import Enum


class CasePriority(Enum):
    """
    Represents the urgency levels assigned to a criminal case.

    Values:
        LOW (1):      Minor cases with no immediate threat.
        MEDIUM (2):   Moderate cases requiring timely attention.
        HIGH (3):     Serious cases demanding priority response.
        CRITICAL (4): Maximum-urgency cases requiring immediate action.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
