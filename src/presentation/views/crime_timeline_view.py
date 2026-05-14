"""
Presentation layer: CrimeTimelineView (Tkinter tab).

Allows investigators to add crime events to the timeline, navigate
forward/backward in chronological order, and filter by location or
view the consolidated suspect list.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.domain.entities.crime_event import CrimeEvent
from src.domain.exceptions.investigation_errors import (
    EmptyTimelineError,
    EventNotFoundError,
    InvestigationError,
)
from src.application.use_cases.crime_chronology import CrimeChronology


class CrimeTimelineView(ttk.Frame):
    """Tkinter frame managing the crime event timeline tab."""

    def __init__(self, parent: tk.Widget, use_case: CrimeChronology) -> None:
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

        # ── Add event panel ───────────────────────────────────────────
        add_frame = ttk.LabelFrame(self, text=" Add Crime Event ", padding=8)
        add_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))
        add_frame.columnconfigure(1, weight=1)

        text_fields = [
            ("Event ID:", "entry_ev_id"),
            ("Title:", "entry_ev_title"),
            ("Description:", "entry_ev_desc"),
            ("Date/Time (YYYY-MM-DD HH:MM:SS):", "entry_ev_date"),
            ("Location:", "entry_ev_loc"),
            ("Suspects (comma-separated):", "entry_ev_suspects"),
        ]
        for idx, (label, attr) in enumerate(text_fields):
            ttk.Label(add_frame, text=label).grid(row=idx, column=0, sticky="w", pady=2)
            widget = ttk.Entry(add_frame)
            widget.grid(row=idx, column=1, sticky="ew", padx=(6, 0), pady=2)
            setattr(self, attr, widget)

        btn_row = ttk.Frame(add_frame)
        btn_row.grid(row=6, column=0, columnspan=2, pady=(8, 0))
        ttk.Button(btn_row, text="➕  Add to End", command=self._on_add_end).pack(
            side="left", padx=4
        )
        ttk.Button(btn_row, text="🔰  Set as Origin", command=self._on_add_origin).pack(
            side="left", padx=4
        )

        # ── Navigation panel ──────────────────────────────────────────
        nav_frame = ttk.LabelFrame(self, text=" Timeline Navigation ", padding=8)
        nav_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=4)

        nav_inner = ttk.Frame(nav_frame)
        nav_inner.pack(fill="x")

        ttk.Button(nav_inner, text="⏮  Origin", command=self._on_go_origin).pack(side="left", padx=4)
        ttk.Button(nav_inner, text="◀  Back", command=self._on_rewind).pack(side="left", padx=4)
        ttk.Button(nav_inner, text="▶  Forward", command=self._on_advance).pack(side="left", padx=4)
        ttk.Button(nav_inner, text="⏭  Latest", command=self._on_go_latest).pack(side="left", padx=4)

        self.lbl_focus = ttk.Label(
            nav_frame,
            text="Current event: —",
            foreground="#005fa3",
            font=("Segoe UI", 9, "italic"),
        )
        self.lbl_focus.pack(fill="x", pady=(6, 0))

        filter_inner = ttk.Frame(nav_frame)
        filter_inner.pack(fill="x", pady=(8, 0))
        ttk.Label(filter_inner, text="Filter by location:").pack(side="left")
        self.entry_loc_filter = ttk.Entry(filter_inner)
        self.entry_loc_filter.pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(filter_inner, text="🔍  Search", command=self._on_filter_loc).pack(side="left")
        ttk.Button(filter_inner, text="👥  All Suspects", command=self._on_suspects).pack(
            side="left", padx=(4, 0)
        )

        # ── Timeline list ─────────────────────────────────────────────
        list_frame = ttk.LabelFrame(self, text=" Crime Events (Chronological) ", padding=8)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(4, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("id", "title", "date", "location", "suspects")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        for col, heading, width in zip(
            columns,
            ("ID", "Title", "Date", "Location", "Suspects"),
            (90, 200, 160, 160, 150),
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

    def _build_event(self) -> CrimeEvent:
        suspects_raw = self.entry_ev_suspects.get().strip()
        suspects = [s.strip() for s in suspects_raw.split(",") if s.strip()]
        return CrimeEvent(
            event_id=self.entry_ev_id.get().strip(),
            event_title=self.entry_ev_title.get().strip(),
            event_description=self.entry_ev_desc.get().strip(),
            event_date=self.entry_ev_date.get().strip(),
            event_location=self.entry_ev_loc.get().strip(),
            involved_suspects=suspects,
        )

    def _on_add_end(self) -> None:
        try:
            event = self._build_event()
            self._use_case.add_event(event)
            messagebox.showinfo("Added", f"Event '{event.event_id}' added to timeline.")
            self._clear_form()
            self._refresh_list()
        except (ValueError, TypeError, InvestigationError) as exc:
            messagebox.showerror("Validation Error", str(exc))

    def _on_add_origin(self) -> None:
        try:
            event = self._build_event()
            self._use_case.insert_founding_event(event)
            messagebox.showinfo("Added", f"Event '{event.event_id}' set as timeline origin.")
            self._clear_form()
            self._refresh_list()
        except (ValueError, TypeError, InvestigationError) as exc:
            messagebox.showerror("Validation Error", str(exc))

    def _on_advance(self) -> None:
        try:
            event = self._use_case.advance_focus()
            if event:
                self._update_focus_label(event)
            else:
                messagebox.showinfo("End of Timeline", "Already at the latest event.")
        except EmptyTimelineError:
            messagebox.showwarning("Empty Timeline", "No events have been recorded.")

    def _on_rewind(self) -> None:
        try:
            event = self._use_case.rewind_focus()
            if event:
                self._update_focus_label(event)
            else:
                messagebox.showinfo("Start of Timeline", "Already at the origin event.")
        except EmptyTimelineError:
            messagebox.showwarning("Empty Timeline", "No events have been recorded.")

    def _on_go_origin(self) -> None:
        try:
            event = self._use_case.go_to_origin()
            self._update_focus_label(event)
        except EmptyTimelineError:
            messagebox.showwarning("Empty Timeline", "No events have been recorded.")

    def _on_go_latest(self) -> None:
        try:
            event = self._use_case.go_to_latest()
            self._update_focus_label(event)
        except EmptyTimelineError:
            messagebox.showwarning("Empty Timeline", "No events have been recorded.")

    def _on_filter_loc(self) -> None:
        location = self.entry_loc_filter.get().strip()
        events = self._use_case.search_by_location(location) if location else self._use_case.get_full_timeline()
        self._populate_tree(events)

    def _on_suspects(self) -> None:
        suspects = self._use_case.get_all_suspects()
        if suspects:
            messagebox.showinfo(
                "Consolidated Suspects",
                "Suspects across all events:\n\n" + "\n".join(sorted(suspects)),
            )
        else:
            messagebox.showinfo("Consolidated Suspects", "No suspects recorded yet.")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _update_focus_label(self, event: CrimeEvent) -> None:
        self.lbl_focus.config(
            text=f"Current event: [{event.event_id}] {event.event_title}  |  {event.event_date}"
        )

    def _refresh_list(self) -> None:
        self._populate_tree(self._use_case.get_full_timeline())
        if not self._use_case.is_timeline_empty():
            try:
                self._update_focus_label(self._use_case.get_current_event())
            except EmptyTimelineError:
                pass

    def _populate_tree(self, events) -> None:
        self.tree.delete(*self.tree.get_children())
        for ev in events:
            self.tree.insert(
                "",
                "end",
                values=(
                    ev.event_id,
                    ev.event_title,
                    ev.event_date,
                    ev.event_location,
                    ", ".join(ev.involved_suspects),
                ),
            )

    def _clear_form(self) -> None:
        for attr in (
            "entry_ev_id", "entry_ev_title", "entry_ev_desc",
            "entry_ev_date", "entry_ev_loc", "entry_ev_suspects",
        ):
            getattr(self, attr).delete(0, tk.END)
