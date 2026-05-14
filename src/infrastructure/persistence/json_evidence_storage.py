"""
Infrastructure adapter: JsonEvidenceRegisterStorage.

Provides save/load persistence for the LinkedListEvidenceRegister
by serialising to a JSON file. Persistence logic is isolated from the
data structure to respect the Single Responsibility Principle.
"""

import json
import os
from typing import TYPE_CHECKING

from src.domain.entities.forensic_evidence import ForensicEvidence

if TYPE_CHECKING:
    from src.infrastructure.persistence.linked_list_evidence_register import (
        LinkedListEvidenceRegister,
    )


class JsonEvidenceRegisterStorage:
    """
    Handles JSON-based persistence for a forensic evidence register.

    Reads and writes evidence data from/to the filesystem, keeping
    I/O concerns separate from the domain and data-structure layers.
    """

    def __init__(self, filepath: str) -> None:
        self.__filepath = filepath

    def save(self, register: "LinkedListEvidenceRegister") -> None:
        """Persist the current evidence register to a JSON file."""
        os.makedirs(os.path.dirname(self.__filepath), exist_ok=True)
        data = [evidence.to_dict() for evidence in register]
        with open(self.__filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load(self, register: "LinkedListEvidenceRegister") -> None:
        """
        Load previously persisted evidence into a register.
        Skips silently if the file does not yet exist.
        """
        if not os.path.exists(self.__filepath):
            return
        with open(self.__filepath, "r", encoding="utf-8") as file:
            for record in json.load(file):
                register.append_evidence(ForensicEvidence.from_dict(record))
