"""
Composition Root — Criminal Investigation System.

This is the application entry point. Its ONLY responsibility is to:
1. Instantiate concrete infrastructure adapters.
2. Inject them into the application use cases.
3. Inject the use cases into the presentation (MainWindow).
4. Start the Tkinter event loop.

No business logic lives here. Changes in infrastructure or UI
require changes only in this file, never in the domain or application layers.
"""

import sys
import os

# Ensure the project root is on the path so absolute imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Infrastructure adapters (concrete implementations) ──────────────
from src.infrastructure.persistence.in_memory_case_backlog import InMemoryCaseBacklog
from src.infrastructure.persistence.in_memory_audit_trail import InMemoryAuditTrail
from src.infrastructure.persistence.linked_list_evidence_register import LinkedListEvidenceRegister
from src.infrastructure.persistence.doubly_linked_crime_timeline import DoublyLinkedCrimeTimeline

# ── Application use cases ────────────────────────────────────────────
from src.application.use_cases.case_assignment import CaseAssignment
from src.application.use_cases.action_registration import ActionRegistration
from src.application.use_cases.evidence_custody import EvidenceCustody
from src.application.use_cases.crime_chronology import CrimeChronology

# ── Presentation layer ───────────────────────────────────────────────
from src.presentation.main_window import MainWindow


def main() -> None:
    """Wire all components and launch the desktop application."""

    # 1. Infrastructure adapters
    case_backlog = InMemoryCaseBacklog()
    audit_trail = InMemoryAuditTrail()
    evidence_register = LinkedListEvidenceRegister()
    crime_timeline = DoublyLinkedCrimeTimeline()

    # 2. Application use cases (inject adapters via constructor)
    case_assignment = CaseAssignment(case_backlog)
    action_registration = ActionRegistration(audit_trail)
    evidence_custody = EvidenceCustody(evidence_register)
    crime_chronology = CrimeChronology(crime_timeline)

    # 3. Presentation window (inject use cases)
    window = MainWindow(
        case_assignment=case_assignment,
        action_registration=action_registration,
        evidence_custody=evidence_custody,
        crime_chronology=crime_chronology,
    )

    # 4. Start the event loop
    window.run()


if __name__ == "__main__":
    main()
