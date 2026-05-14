"""
Presentation layer: MainWindow.

Root Tkinter window. Assembles all tab views and wires them to their
respective application use cases via Dependency Injection.
The window is the only place that knows about concrete infrastructure
adapters — every view only talks to abstract use-case interfaces.
"""

import tkinter as tk
from tkinter import ttk

from src.application.use_cases.case_assignment import CaseAssignment
from src.application.use_cases.action_registration import ActionRegistration
from src.application.use_cases.evidence_custody import EvidenceCustody
from src.application.use_cases.crime_chronology import CrimeChronology

from src.presentation.views.case_backlog_view import CaseBacklogView
from src.presentation.views.audit_trail_view import AuditTrailView
from src.presentation.views.evidence_custody_view import EvidenceCustodyView
from src.presentation.views.crime_timeline_view import CrimeTimelineView


class MainWindow:
    """
    Root application window for the Criminal Investigation System.

    Receives all use-case instances (injected from main.py) and
    mounts each into a dedicated Notebook tab.
    """

    _TITLE = "Criminal Investigation System"
    _GEOMETRY = "1100x700"
    _MIN_SIZE = (900, 580)

    def __init__(
        self,
        case_assignment: CaseAssignment,
        action_registration: ActionRegistration,
        evidence_custody: EvidenceCustody,
        crime_chronology: CrimeChronology,
    ) -> None:
        self._root = tk.Tk()
        self._root.title(self._TITLE)
        self._root.geometry(self._GEOMETRY)
        self._root.minsize(*self._MIN_SIZE)

        self._apply_theme()
        self._build_ui(
            case_assignment,
            action_registration,
            evidence_custody,
            crime_chronology,
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self._root.mainloop()

    # ------------------------------------------------------------------
    # Private builders
    # ------------------------------------------------------------------

    def _apply_theme(self) -> None:
        """Apply a clean, professional visual theme."""
        style = ttk.Style(self._root)
        # Use 'clam' for cross-platform consistency
        style.theme_use("clam")

        bg = "#1e2329"
        panel_bg = "#252b33"
        accent = "#3b82f6"
        fg = "#e2e8f0"
        entry_bg = "#2d3748"

        self._root.configure(bg=bg)

        style.configure(".", background=bg, foreground=fg, font=("Segoe UI", 10))
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure(
            "TLabelframe",
            background=panel_bg,
            foreground=accent,
            relief="flat",
            borderwidth=1,
        )
        style.configure("TLabelframe.Label", background=panel_bg, foreground=accent, font=("Segoe UI", 10, "bold"))
        style.configure(
            "TButton",
            background=accent,
            foreground="#ffffff",
            padding=(8, 4),
            relief="flat",
        )
        style.map("TButton", background=[("active", "#2563eb")])
        style.configure("TEntry", fieldbackground=entry_bg, foreground=fg, insertcolor=fg)
        style.configure("TCombobox", fieldbackground=entry_bg, foreground=fg, selectbackground=accent)
        style.configure(
            "Treeview",
            background=entry_bg,
            foreground=fg,
            fieldbackground=entry_bg,
            rowheight=24,
        )
        style.configure("Treeview.Heading", background=panel_bg, foreground=accent, font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", accent)])
        style.configure(
            "TNotebook",
            background=bg,
            tabmargins=[2, 4, 2, 0],
        )
        style.configure(
            "TNotebook.Tab",
            background=panel_bg,
            foreground=fg,
            padding=(12, 6),
            font=("Segoe UI", 10),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", accent)],
            foreground=[("selected", "#ffffff")],
        )

    def _build_ui(
        self,
        case_assignment: CaseAssignment,
        action_registration: ActionRegistration,
        evidence_custody: EvidenceCustody,
        crime_chronology: CrimeChronology,
    ) -> None:
        # ── Header bar ───────────────────────────────────────────────
        header = tk.Frame(self._root, bg="#0f1318", height=52)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔍  Criminal Investigation System",
            bg="#0f1318",
            fg="#e2e8f0",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left", padx=16, pady=12)

        tk.Label(
            header,
            text="Forensic Intelligence Platform  •  v3.0",
            bg="#0f1318",
            fg="#64748b",
            font=("Segoe UI", 9),
        ).pack(side="right", padx=16)

        # ── Notebook tabs ─────────────────────────────────────────────
        notebook = ttk.Notebook(self._root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tabs = [
            ("📋  Case Backlog", CaseBacklogView, case_assignment),
            ("📝  Audit Trail", AuditTrailView, action_registration),
            ("🔬  Evidence Custody", EvidenceCustodyView, evidence_custody),
            ("🕐  Crime Timeline", CrimeTimelineView, crime_chronology),
        ]
        for tab_title, ViewClass, use_case in tabs:
            frame = ViewClass(notebook, use_case)
            frame.pack(fill="both", expand=True)
            notebook.add(frame, text=tab_title)

        # ── Status bar ────────────────────────────────────────────────
        status = tk.Label(
            self._root,
            text="System ready",
            bg="#0f1318",
            fg="#64748b",
            font=("Segoe UI", 8),
            anchor="w",
            padx=10,
        )
        status.pack(fill="x", side="bottom", ipady=3)
