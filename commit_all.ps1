#!/usr/bin/env pwsh
# commit_all.ps1 - Criminal Investigation System
# Multi-author commit script (Conventional Commits)
# Run from: c:\Users\dino2\OneDrive\Escritorio\estructurafinal

Set-Location "c:\Users\dino2\OneDrive\Escritorio\estructurafinal"

$A1_NAME  = "StehvenObandoUcc"
$A1_EMAIL = "stehven.obando@campusucc.edu.co"

$A2_NAME  = "F3L1P3GoD"
$A2_EMAIL = "felipe.gamboa0102@gmail.com"

$A3_NAME  = "maajjjoo"
$A3_EMAIL = "majose2006@gmail.com"

function Commit-File($AuthorName, $AuthorEmail, $FilePath, $Message) {
    git config user.name  $AuthorName
    git config user.email $AuthorEmail
    git add $FilePath
    git commit -m $Message
    Write-Host "[OK] [$AuthorName] $Message" -ForegroundColor Green
}

Write-Host "=== Criminal Investigation System - Multi-Author Commits ===" -ForegroundColor Cyan

# --- Domain Entities ---
Write-Host "`n-- Domain Entities --" -ForegroundColor Yellow

Commit-File $A1_NAME $A1_EMAIL "src/domain/entities/case_priority.py" `
    "feat: add CasePriority enum for criminal case urgency levels"

Commit-File $A2_NAME $A2_EMAIL "src/domain/entities/action_type.py" `
    "feat: add ActionType enum for investigator operation categories"

Commit-File $A3_NAME $A3_EMAIL "src/domain/entities/evidence_type.py" `
    "feat: add EvidenceType enum for forensic evidence classification"

Commit-File $A1_NAME $A1_EMAIL "src/domain/entities/criminal_case.py" `
    "feat: add CriminalCase entity with assignment behaviour and invariant validation"

Commit-File $A2_NAME $A2_EMAIL "src/domain/entities/investigator_action.py" `
    "feat: add immutable InvestigatorAction entity for audit trail records"

Commit-File $A3_NAME $A3_EMAIL "src/domain/entities/forensic_evidence.py" `
    "feat: add immutable ForensicEvidence entity with serialisation support"

Commit-File $A1_NAME $A1_EMAIL "src/domain/entities/crime_event.py" `
    "feat: add CrimeEvent entity for chronological crime timeline nodes"

# --- Domain Exceptions ---
Write-Host "`n-- Domain Exceptions --" -ForegroundColor Yellow

Commit-File $A2_NAME $A2_EMAIL "src/domain/exceptions/investigation_errors.py" `
    "feat: add domain exception hierarchy with shared InvestigationError base"

# --- Domain Ports ---
Write-Host "`n-- Domain Ports (Interfaces) --" -ForegroundColor Yellow

Commit-File $A3_NAME $A3_EMAIL "src/domain/ports/case_backlog_port.py" `
    "feat: define CaseBacklogPort protocol for pending case storage abstraction"

Commit-File $A1_NAME $A1_EMAIL "src/domain/ports/audit_trail_port.py" `
    "feat: define AuditTrailPort protocol for investigator action storage"

Commit-File $A2_NAME $A2_EMAIL "src/domain/ports/evidence_register_port.py" `
    "feat: define EvidenceRegisterPort protocol for chain-of-custody abstraction"

Commit-File $A3_NAME $A3_EMAIL "src/domain/ports/crime_timeline_port.py" `
    "feat: define CrimeTimelinePort protocol for bidirectional timeline navigation"

# --- Application Use Cases ---
Write-Host "`n-- Application Use Cases --" -ForegroundColor Yellow

Commit-File $A1_NAME $A1_EMAIL "src/application/use_cases/case_assignment.py" `
    "feat: implement CaseAssignment use case for case registration and assignment"

Commit-File $A2_NAME $A2_EMAIL "src/application/use_cases/action_registration.py" `
    "feat: implement ActionRegistration use case for audit trail and undo workflow"

Commit-File $A3_NAME $A3_EMAIL "src/application/use_cases/evidence_custody.py" `
    "feat: implement EvidenceCustody use case for chain-of-custody management"

Commit-File $A1_NAME $A1_EMAIL "src/application/use_cases/crime_chronology.py" `
    "feat: implement CrimeChronology use case for timeline navigation and queries"

# --- Infrastructure Adapters ---
Write-Host "`n-- Infrastructure Adapters (Data Structures) --" -ForegroundColor Yellow

Commit-File $A2_NAME $A2_EMAIL "src/infrastructure/persistence/in_memory_case_backlog.py" `
    "feat: implement InMemoryCaseBacklog using deque for O(1) FIFO operations"

Commit-File $A3_NAME $A3_EMAIL "src/infrastructure/persistence/in_memory_audit_trail.py" `
    "feat: implement InMemoryAuditTrail as LIFO stack for action undo support"

Commit-File $A1_NAME $A1_EMAIL "src/infrastructure/persistence/linked_list_evidence_register.py" `
    "feat: implement LinkedListEvidenceRegister as singly-linked chain-of-custody"

Commit-File $A2_NAME $A2_EMAIL "src/infrastructure/persistence/doubly_linked_crime_timeline.py" `
    "feat: implement DoublyLinkedCrimeTimeline for O(1) bidirectional navigation"

Commit-File $A3_NAME $A3_EMAIL "src/infrastructure/persistence/json_evidence_storage.py" `
    "feat: add JsonEvidenceRegisterStorage for file-based evidence persistence"

# --- Presentation Layer ---
Write-Host "`n-- Presentation Layer (Tkinter UI) --" -ForegroundColor Yellow

Commit-File $A1_NAME $A1_EMAIL "src/presentation/views/case_backlog_view.py" `
    "feat: add CaseBacklogView tkinter tab for case registration and assignment"

Commit-File $A2_NAME $A2_EMAIL "src/presentation/views/audit_trail_view.py" `
    "feat: add AuditTrailView tkinter tab for recording and reverting actions"

Commit-File $A3_NAME $A3_EMAIL "src/presentation/views/evidence_custody_view.py" `
    "feat: add EvidenceCustodyView tkinter tab for forensic evidence management"

Commit-File $A1_NAME $A1_EMAIL "src/presentation/views/crime_timeline_view.py" `
    "feat: add CrimeTimelineView tkinter tab for crime event navigation"

Commit-File $A2_NAME $A2_EMAIL "src/presentation/main_window.py" `
    "feat: add MainWindow root with dark theme and dependency-injected notebook tabs"

# --- Package __init__.py files ---
Write-Host "`n-- Package __init__.py files --" -ForegroundColor Yellow

$initFiles = @(
    "src/__init__.py",
    "src/domain/__init__.py",
    "src/domain/entities/__init__.py",
    "src/domain/exceptions/__init__.py",
    "src/domain/ports/__init__.py",
    "src/application/__init__.py",
    "src/application/use_cases/__init__.py",
    "src/infrastructure/__init__.py",
    "src/infrastructure/persistence/__init__.py",
    "src/presentation/__init__.py",
    "src/presentation/views/__init__.py"
)

$authors = @(
    @{ Name = $A3_NAME; Email = $A3_EMAIL },
    @{ Name = $A1_NAME; Email = $A1_EMAIL },
    @{ Name = $A2_NAME; Email = $A2_EMAIL }
)

for ($i = 0; $i -lt $initFiles.Count; $i++) {
    $auth = $authors[$i % 3]
    $pkg = ($initFiles[$i] -split "/")[0..($initFiles[$i].Split("/").Count - 2)] -join "/"
    Commit-File $auth.Name $auth.Email $initFiles[$i] `
        "chore: expose $pkg as importable Python package"
}

# --- Root files ---
Write-Host "`n-- Root Files --" -ForegroundColor Yellow

Commit-File $A3_NAME $A3_EMAIL "main.py" `
    "feat: add composition root wiring all layers and launching tkinter app"

Commit-File $A1_NAME $A1_EMAIL "README.md" `
    "docs: add professional README with architecture, data structures and run guide"

Commit-File $A2_NAME $A2_EMAIL "commit_all.ps1" `
    "chore: add multi-author commit automation script"

# --- Summary ---
Write-Host "`n=== All commits created. Git log: ===" -ForegroundColor Cyan
git log --oneline
