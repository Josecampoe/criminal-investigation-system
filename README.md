# 🔍 Criminal Investigation System

> **Academic Project — Data Structures & Software Design**
> Universidad Cooperativa de Colombia · May 2025

---

## 📋 Project Context

The **Criminal Investigation System** is a desktop monolithic application that simulates the core workflows of a criminal investigations unit. It was built as a practical exercise to apply **advanced data structures** (LIFO Stack, FIFO Queue, Singly-Linked List, Doubly-Linked List) within a real-world business domain, while following professional software engineering principles.

The system allows investigators to:
- Register and assign criminal cases following a strict priority-respecting queue.
- Record every investigative action with full **undo capability** via an audit trail.
- Manage forensic evidence through a **chain-of-custody** linked register.
- Reconstruct and navigate a **bidirectional chronological timeline** of crime events.

---

## 🏗️ Architecture — Clean Architecture (Layered Monolith)

The project is organized into four strict layers. Each layer communicates **only downward** — the domain knows nothing about infrastructure or UI.

```
criminal-investigation-system/
│
├── main.py                          ← Composition Root (Dependency Injection)
│
└── src/
    ├── domain/                      ← Layer 1: Pure Business Rules
    │   ├── entities/                  Pure domain objects (dataclasses)
    │   │   ├── action_type.py
    │   │   ├── case_priority.py
    │   │   ├── crime_event.py
    │   │   ├── criminal_case.py
    │   │   ├── evidence_type.py
    │   │   ├── forensic_evidence.py
    │   │   └── investigator_action.py
    │   ├── exceptions/              Domain-specific errors
    │   │   └── investigation_errors.py
    │   └── ports/                   Abstract contracts (typing.Protocol)
    │       ├── audit_trail_port.py
    │       ├── case_backlog_port.py
    │       ├── crime_timeline_port.py
    │       └── evidence_register_port.py
    │
    ├── application/                 ← Layer 2: Use Cases / Business Orchestration
    │   └── use_cases/
    │       ├── action_registration.py
    │       ├── case_assignment.py
    │       ├── crime_chronology.py
    │       └── evidence_custody.py
    │
    ├── infrastructure/              ← Layer 3: Concrete Data Structures
    │   └── persistence/
    │       ├── doubly_linked_crime_timeline.py   (Doubly-Linked List)
    │       ├── in_memory_audit_trail.py          (LIFO Stack → list)
    │       ├── in_memory_case_backlog.py         (FIFO Queue → deque O(1))
    │       ├── json_evidence_storage.py          (JSON persistence)
    │       └── linked_list_evidence_register.py  (Singly-Linked List)
    │
    └── presentation/               ← Layer 4: Tkinter Desktop UI
        ├── main_window.py             Root window + Notebook tabs + Dark theme
        └── views/
            ├── audit_trail_view.py
            ├── case_backlog_view.py
            ├── crime_timeline_view.py
            └── evidence_custody_view.py
```

### Layer Communication

```
Presentation  →  Application (Use Cases)  →  Domain Ports  ←  Infrastructure
    (UI)              (Orchestration)          (Contracts)      (Data Structures)
```

> The **Dependency Inversion Principle** is enforced via `typing.Protocol`.
> Use cases depend on **interfaces**, never on concrete adapters.

---

## ⚙️ Data Structures Used

| Structure | Implementation | Location | Business Purpose |
|:---|:---|:---|:---|
| **LIFO Stack** | `list` (append/pop O(1)) | `InMemoryAuditTrail` | Investigator action undo trail |
| **FIFO Queue** | `collections.deque` (O(1)) | `InMemoryCaseBacklog` | Criminal case pending backlog |
| **Singly-Linked List** | Custom `_EvidenceNode` | `LinkedListEvidenceRegister` | Forensic chain-of-custody |
| **Doubly-Linked List** | Custom `_TimelineNode` | `DoublyLinkedCrimeTimeline` | Bidirectional crime chronology |

---

## 🚀 How to Run

### Prerequisites
- Python **3.10+**
- Tkinter (bundled with standard Python on Windows/macOS)
- No external dependencies required

### Launch
```bash
# From the project root directory
python main.py
```

---

## 🖥️ Application Modules

| Tab | Use Case | Description |
|:---|:---|:---|
| 📋 **Case Backlog** | `CaseAssignment` | Register cases, assign next case to an investigator, filter by priority |
| 📝 **Audit Trail** | `ActionRegistration` | Record investigative actions, undo the last action, search by investigator |
| 🔬 **Evidence Custody** | `EvidenceCustody` | Register standard/critical evidence, invalidate entries, filter by type |
| 🕐 **Crime Timeline** | `CrimeChronology` | Add events, navigate forward/backward, filter by location, view suspects |

---

## 🛠️ Technology Stack

| Layer | Technology |
|:---|:---|
| Language | Python 3.10+ |
| Desktop UI | Tkinter (ttk, themed widgets) |
| Data Structures | Custom implementations (no external libs) |
| Persistence | In-memory + JSON files |
| Design Patterns | Clean Architecture, SOLID, DRY, Ubiquitous Language |

---

## 📐 Design Principles Applied

- **Single Responsibility (SRP):** Each class has exactly one reason to change.
- **Open/Closed (OCP):** New storage adapters can be added without touching use cases.
- **Dependency Inversion (DIP):** Use cases depend on `Protocol` interfaces, not implementations.
- **DRY:** Shared validation helpers extracted to private methods.
- **Ubiquitous Language:** No pattern names mixed with business names (`CaseAssignment` not `CaseQueueManager`).

---

## 📅 Delivery

**Due date:** May 15, 2025
**Course:** Data Structures — Universidad Cooperativa de Colombia
