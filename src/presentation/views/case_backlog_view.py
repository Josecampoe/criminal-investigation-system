"""
Presentation layer: CaseBacklogView (Tkinter tab).

Displays the pending criminal case backlog. Users can register new cases,
assign the next case to an investigator, and filter by priority.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.domain.entities.criminal_case import CriminalCase
from src.domain.entities.case_priority import CasePriority
from src.domain.exceptions.investigation_errors import (
    NoPendingCasesError,
    InvalidPriorityError,
    InvestigationError,
)
from src.application.use_cases.case_assignment import CaseAssignment


class CaseBacklogView(ttk.Frame):
    """Tkinter frame managing the criminal case backlog tab."""

    def __init__(self, parent: tk.Widget, use_case: CaseAssignment) -> None:
        super().__init__(parent)
        self._use_case = use_case
        self._build_ui()
        self._refresh_list()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        # ── Register case panel ──────────────────────────────────────
        reg_frame = ttk.LabelFrame(self, text=" Register New Case ", padding=8)
        reg_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 4))
        reg_frame.columnconfigure(1, weight=1)

        fields = [
            ("Case ID:", "entry_case_id"),
            ("Title:", "entry_title"),
            ("Registration Date (YYYY-MM-DD HH:MM:SS):", "entry_date"),
        ]
        for row_idx, (label, attr) in enumerate(fields):
            ttk.Label(reg_frame, text=label).grid(row=row_idx, column=0, sticky="w", pady=2)
            widget = ttk.Entry(reg_frame)
            widget.grid(row=row_idx, column=1, sticky="ew", padx=(6, 0), pady=2)
            setattr(self, attr, widget)

        ttk.Label(reg_frame, text="Priority:").grid(row=3, column=0, sticky="w", pady=2)
        self.combo_priority = ttk.Combobox(
            reg_frame,
            values=[p.name for p in CasePriority],
            state="readonly",
        )
        self.combo_priority.set(CasePriority.MEDIUM.name)
        self.combo_priority.grid(row=3, column=1, sticky="ew", padx=(6, 0), pady=2)

        ttk.Button(reg_frame, text="➕  Register Case", command=self._on_register).grid(
            row=4, column=0, columnspan=2, pady=(8, 0)
        )

        # ── Assign next case panel ────────────────────────────────────
        assign_frame = ttk.LabelFrame(self, text=" Assign Next Case ", padding=8)
        assign_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)
        assign_frame.columnconfigure(1, weight=1)

        ttk.Label(assign_frame, text="Investigator Name:").grid(row=0, column=0, sticky="w")
        self.entry_investigator = ttk.Entry(assign_frame)
        self.entry_investigator.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        ttk.Button(assign_frame, text="✅  Assign Next", command=self._on_assign).grid(
            row=1, column=0, columnspan=2, pady=(8, 0)
        )

        # ── Filter panel ──────────────────────────────────────────────
        filter_frame = ttk.LabelFrame(self, text=" Filter by Priority ", padding=8)
        filter_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=4)
        filter_frame.columnconfigure(1, weight=1)

        self.combo_filter = ttk.Combobox(
            filter_frame,
            values=["ALL"] + [p.name for p in CasePriority],
            state="readonly",
        )
        self.combo_filter.set("ALL")
        self.combo_filter.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(filter_frame, text="🔍  Filter", command=self._on_filter).grid(
            row=0, column=1
        )

        # ── Pending cases list ────────────────────────────────────────
        list_frame = ttk.LabelFrame(self, text=" Pending Cases ", padding=8)
        list_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=(4, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("id", "title", "priority", "date")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        for col, heading, width in zip(
            columns,
            ("Case ID", "Title", "Priority", "Registered"),
            (120, 300, 90, 160),
        ):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, minwidth=60)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        ttk.Button(self, text="🔄  Refresh", command=self._refresh_list).grid(
            row=4, column=0, columnspan=2, pady=(0, 10)
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_register(self) -> None:
        try:
            case = CriminalCase(
                case_id=self.entry_case_id.get().strip(),
                case_title=self.entry_title.get().strip(),
                case_priority=CasePriority[self.combo_priority.get()],
                assigned_investigator="",
                registration_date=self.entry_date.get().strip(),
            )
            self._use_case.register_case(case)
            messagebox.showinfo("Success", f"Case '{case.case_id}' registered.")
            self._clear_form()
            self._refresh_list()
        except (ValueError, TypeError, InvestigationError) as exc:
            messagebox.showerror("Validation Error", str(exc))

    def _on_assign(self) -> None:
        investigator = self.entry_investigator.get().strip()
        try:
            assigned = self._use_case.assign_next_to(investigator)
            messagebox.showinfo(
                "Assigned",
                f"Case '{assigned.case_id}' assigned to {investigator}.",
            )
            self._refresh_list()
        except NoPendingCasesError:
            messagebox.showwarning("Empty Backlog", "No pending cases to assign.")
        except (ValueError, InvestigationError) as exc:
            messagebox.showerror("Error", str(exc))

    def _on_filter(self) -> None:
        selected = self.combo_filter.get()
        if selected == "ALL":
            cases = self._use_case.get_all_pending()
        else:
            cases = self._use_case.filter_by_priority(CasePriority[selected])
        self._populate_tree(cases)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _refresh_list(self) -> None:
        self._populate_tree(self._use_case.get_all_pending())

    def _populate_tree(self, cases) -> None:
        self.tree.delete(*self.tree.get_children())
        for case in cases:
            self.tree.insert(
                "",
                "end",
                values=(case.case_id, case.case_title, case.case_priority.name, case.registration_date),
            )

    def _clear_form(self) -> None:
        for attr in ("entry_case_id", "entry_title", "entry_date"):
            getattr(self, attr).delete(0, tk.END)
