"""
Presentation layer: EvidenceCustodyView (Tkinter tab).

Lets investigators register, search, filter and invalidate
forensic evidence items in the chain-of-custody register.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.domain.entities.forensic_evidence import ForensicEvidence
from src.domain.entities.evidence_type import EvidenceType
from src.domain.exceptions.investigation_errors import (
    EvidenceNotFoundError,
    InvestigationError,
)
from src.application.use_cases.evidence_custody import EvidenceCustody


class EvidenceCustodyView(ttk.Frame):
    """Tkinter frame managing the forensic evidence custody tab."""

    def __init__(self, parent: tk.Widget, use_case: EvidenceCustody) -> None:
        super().__init__(parent)
        self._use_case = use_case
        self._build_ui()
        self._refresh_list()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # ── Register evidence panel ───────────────────────────────────
        reg_frame = ttk.LabelFrame(self, text=" Register Evidence ", padding=8)
        reg_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))
        reg_frame.columnconfigure(1, weight=1)

        text_fields = [
            ("Evidence ID:", "entry_ev_id"),
            ("Description:", "entry_ev_desc"),
            ("Collection Date (YYYY-MM-DD):", "entry_ev_date"),
            ("Collected By:", "entry_ev_agent"),
        ]
        for idx, (label, attr) in enumerate(text_fields):
            ttk.Label(reg_frame, text=label).grid(row=idx, column=0, sticky="w", pady=2)
            widget = ttk.Entry(reg_frame)
            widget.grid(row=idx, column=1, sticky="ew", padx=(6, 0), pady=2)
            setattr(self, attr, widget)

        ttk.Label(reg_frame, text="Evidence Type:").grid(row=4, column=0, sticky="w", pady=2)
        self.combo_ev_type = ttk.Combobox(
            reg_frame,
            values=[t.name for t in EvidenceType],
            state="readonly",
        )
        self.combo_ev_type.set(EvidenceType.FINGERPRINT.name)
        self.combo_ev_type.grid(row=4, column=1, sticky="ew", padx=(6, 0), pady=2)

        btn_row = ttk.Frame(reg_frame)
        btn_row.grid(row=5, column=0, columnspan=2, pady=(8, 0))
        ttk.Button(btn_row, text="➕  Register Standard", command=self._on_register).pack(
            side="left", padx=4
        )
        ttk.Button(btn_row, text="🚨  Register Critical", command=self._on_register_critical).pack(
            side="left", padx=4
        )

        # ── Search / invalidate panel ─────────────────────────────────
        action_frame = ttk.LabelFrame(self, text=" Find / Invalidate Evidence ", padding=8)
        action_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=4)
        action_frame.columnconfigure(1, weight=1)

        ttk.Label(action_frame, text="Evidence ID:").grid(row=0, column=0, sticky="w")
        self.entry_search_id = ttk.Entry(action_frame)
        self.entry_search_id.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        btn_row2 = ttk.Frame(action_frame)
        btn_row2.grid(row=1, column=0, columnspan=2, pady=(6, 0))
        ttk.Button(btn_row2, text="🔍  Find by ID", command=self._on_find).pack(side="left", padx=4)
        ttk.Button(btn_row2, text="🗑️  Invalidate", command=self._on_invalidate).pack(
            side="left", padx=4
        )

        ttk.Label(action_frame, text="Filter by Type:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.combo_filter = ttk.Combobox(
            action_frame,
            values=["ALL"] + [t.name for t in EvidenceType],
            state="readonly",
        )
        self.combo_filter.set("ALL")
        self.combo_filter.grid(row=2, column=1, sticky="ew", padx=(6, 0), pady=(8, 0))
        ttk.Button(action_frame, text="🔍  Filter", command=self._on_filter_type).grid(
            row=3, column=0, columnspan=2, pady=(4, 0)
        )

        # ── Inventory list ────────────────────────────────────────────
        list_frame = ttk.LabelFrame(self, text=" Evidence Inventory ", padding=8)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(4, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("id", "type", "description", "date", "agent")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        for col, heading, width in zip(
            columns,
            ("ID", "Type", "Description", "Date", "Agent"),
            (100, 130, 270, 110, 130),
        ):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, minwidth=50)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        ttk.Button(self, text="🔄  Refresh", command=self._refresh_list).grid(
            row=3, column=0, pady=(0, 10)
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _build_evidence(self) -> ForensicEvidence:
        return ForensicEvidence(
            evidence_id=self.entry_ev_id.get().strip(),
            evidence_type=EvidenceType[self.combo_ev_type.get()],
            description=self.entry_ev_desc.get().strip(),
            collection_date=self.entry_ev_date.get().strip(),
            collected_by=self.entry_ev_agent.get().strip(),
        )

    def _on_register(self) -> None:
        try:
            ev = self._build_evidence()
            self._use_case.register_evidence(ev)
            messagebox.showinfo("Success", f"Evidence '{ev.evidence_id}' registered.")
            self._clear_form()
            self._refresh_list()
        except (ValueError, TypeError, InvestigationError) as exc:
            messagebox.showerror("Validation Error", str(exc))

    def _on_register_critical(self) -> None:
        try:
            ev = self._build_evidence()
            self._use_case.register_critical_evidence(ev)
            messagebox.showinfo("Success", f"Critical evidence '{ev.evidence_id}' prioritised.")
            self._clear_form()
            self._refresh_list()
        except (ValueError, TypeError, InvestigationError) as exc:
            messagebox.showerror("Validation Error", str(exc))

    def _on_find(self) -> None:
        ev_id = self.entry_search_id.get().strip()
        try:
            ev = self._use_case.find_evidence(ev_id)
            messagebox.showinfo("Found", str(ev))
        except EvidenceNotFoundError as exc:
            messagebox.showwarning("Not Found", str(exc))

    def _on_invalidate(self) -> None:
        ev_id = self.entry_search_id.get().strip()
        if not messagebox.askyesno("Confirm", f"Invalidate evidence '{ev_id}'?"):
            return
        try:
            self._use_case.invalidate_evidence(ev_id)
            messagebox.showinfo("Removed", f"Evidence '{ev_id}' invalidated.")
            self._refresh_list()
        except EvidenceNotFoundError as exc:
            messagebox.showwarning("Not Found", str(exc))

    def _on_filter_type(self) -> None:
        selected = self.combo_filter.get()
        if selected == "ALL":
            items = self._use_case.get_full_inventory()
        else:
            items = self._use_case.get_evidence_by_type(EvidenceType[selected])
        self._populate_tree(items)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _refresh_list(self) -> None:
        self._populate_tree(self._use_case.get_full_inventory())

    def _populate_tree(self, items) -> None:
        self.tree.delete(*self.tree.get_children())
        for ev in items:
            self.tree.insert(
                "",
                "end",
                values=(
                    ev.evidence_id,
                    ev.evidence_type.value,
                    ev.description,
                    ev.collection_date,
                    ev.collected_by,
                ),
            )

    def _clear_form(self) -> None:
        for attr in ("entry_ev_id", "entry_ev_desc", "entry_ev_date", "entry_ev_agent"):
            getattr(self, attr).delete(0, tk.END)
