"""
Domain enumeration for forensic evidence categories.

Each value represents a legally recognized category of physical
or digital evidence that can be collected and registered during
a criminal investigation.
"""

from enum import Enum


class EvidenceType(Enum):
    """
    Represents the legally recognized classification of forensic evidence.

    Values:
        FINGERPRINT:       Fingerprint collected at a scene.
        WEAPON:            Weapon or instrument related to the crime.
        WITNESS_TESTIMONY: Testimonial account from a witness.
        RECORDING:         Audio or video recording from surveillance.
        DOCUMENT:          Paper or digital document relevant to the case.
        DNA_SAMPLE:        Biological DNA sample.
        PHOTOGRAPH:        Crime scene or suspect photograph.
    """

    FINGERPRINT = "Fingerprint"
    WEAPON = "Weapon"
    WITNESS_TESTIMONY = "Witness Testimony"
    RECORDING = "Recording"
    DOCUMENT = "Document"
    DNA_SAMPLE = "DNA Sample"
    PHOTOGRAPH = "Photograph"
