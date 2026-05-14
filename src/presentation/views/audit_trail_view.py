"""
Presentation layer: AuditTrailView (Tkinter tab).

Displays the investigator action audit trail. Users can record new
actions and revert (undo) the most recently recorded one.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from src.domain.entities.investigator_action import InvestigatorAction
from src.domain.entities.action_type import ActionType
from src.domain.exceptions.investigation_errors import (
    EmptyAuditTrailError,
    InvestigationError,
)
from src.application.use_cases.action_registration import ActionRegistration


class AuditTrailView(ttk.Frame):
    """Tkinter frame managing the investigator audit trail tab."""

    def __init__(self, parent: tk.Widget, use_case: ActionRegistration) -> None:
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

        # ── Record action panel ───────────────────────────────────────
        rec_frame = ttk.LabelFrame(self, text=" Record New Action ", padding=8)
        rec_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))
        rec_frame.columnconfigure(1, weight=1)

        fields = [
            ("Action ID:", "entry_action_id"),
            ("Investigator Name:", "entry_investigator"),
            ("Description:", "entry_description"),
        ]
        for idx, (label, attr) in enumerate(fields):
            ttk.Label(rec_frame, text=label).grid(row=idx, column=0, sticky="w", pady=2)
            widget = ttk.Entry(rec_frame)
            widget.grid(row=idx, column=1, sticky="ew", padx=(6, 0), pady=2)
            setattr(self, attr, widget)

        ttk.Label(rec_frame, text="Action Type:").grid(row=3, column=0, sticky="w", pady=2)
        self.combo_type = ttk.Combobox(
            rec_frame,
            values=[t.name for t in ActionType],
            state="readonly",
        )
        self.combo_type.set(ActionType.ADD_EVIDENCE.name)
        self.combo_type.grid(row=3, column=1, sticky="ew", padx=(6, 0), pady=2)

        btn_row = ttk.Frame(rec_frame)
        btn_row.grid(row=4, column=0, columnspan=2, pady=(8, 0))
        ttk.Button(btn_row, text="➕  Record Action", command=self._on_record).pack(
            side="left", padx=4
        )
        ttk.Button(btn_row, text="↩️  Undo Last Action", command=self._on_undo).pack(
            side="left", padx=4
        )

        # ── Search by investigator ────────────────────────────────────
        search_frame = ttk.LabelFrame(self, text=" Search by Investigator ", padding=8)
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=4)
        search_frame.columnconfigure(0, weight=1)

        inner = ttk.Frame(search_frame)
        inner.grid(row=0, column=0, sticky="ew")
        inner.columnconfigure(0, weight=1)

        self.entry_search = ttk.Entry(inner)
        self.entry_search.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(inner, text="🔍  Search", command=self._on_search).grid(row=0, column=1)
        ttk.Button(inner, text="🔄  Show All", command=self._refresh_list).grid(
            row=0, column=2, padx=(4, 0)
        )

        # ── History list ──────────────────────────────────────────────
        list_frame = ttk.LabelFrame(self, text=" Action History (most recent first) ", padding=8)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(4, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("id", "type", "investigator", "description", "timestamp")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        for col, heading, width in zip(
            columns,
            ("ID", "Type", "Investigator", "Description", "Timestamp"),
            (80, 120, 160, 280, 160),
        ):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, minwidth=50)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_record(self) -> None:
        try:
            action = InvestigatorAction(
                action_id=self.entry_action_id.get().strip(),
                action_type=ActionType[self.combo_type.get()],
                description=self.entry_description.get().strip(),
                investigator_name=self.entry_investigator.get().strip(),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            self._use_case.record_action(action)
            messagebox.showinfo("Success", f"Action '{action.action_id}' recorded.")
            self._clear_form()
            self._refresh_list()
        except (ValueError, TypeError, InvestigationError) as exc:
            messagebox.showerror("Validation Error", str(exc))

    def _on_undo(self) -> None:
        try:
            reverted = self._use_case.revert_last_action()
            messagebox.showinfo(
                "Undone",
                f"Action '{reverted.action_id}' has been reverted.",
            )
            self._refresh_list()
        except EmptyAuditTrailError:
            messagebox.showwarning("Empty Trail", "No actions to undo.")

    def _on_search(self) -> None:
        name = self.entry_search.get().strip()
        if not name:
            self._refresh_list()
            return
        try:
            actions = self._use_case.find_by_investigator(name)
            self._populate_tree(actions)
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _refresh_list(self) -> None:
        self._populate_tree(self._use_case.get_full_history())

    def _populate_tree(self, actions) -> None:
        self.tree.delete(*self.tree.get_children())
        for action in actions:
            self.tree.insert(
                "",
                "end",
                values=(
                    action.action_id,
                    action.action_type.value,
                    action.investigator_name,
                    action.description,
                    action.timestamp,
                ),
            )

    def _clear_form(self) -> None:
        for attr in ("entry_action_id", "entry_investigator", "entry_description"):
            getattr(self, attr).delete(0, tk.END)
