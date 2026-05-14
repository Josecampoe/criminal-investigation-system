from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Dict, Any


class EvidenceType(Enum):
    """
    Define el catálogo exhaustivo de tipos de evidencias permitidos.
    Cada tipo representa una categoría forense con validez legal.
    """
    FINGERPRINT = "Huella Dactilar"
    WEAPON = "Arma"
    WITNESS_TESTIMONY = "Testimonio de Testigo"
    RECORDING = "Grabación"
    DOCUMENT = "Documento"
    DNA_SAMPLE = "Muestra de ADN"
    PHOTOGRAPH = "Fotografía"


@dataclass(frozen=True)
class Evidence:
    """
    Representa una unidad de evidencia forense inmutable.
    La inmutabilidad garantiza la integridad de la cadena de custodia.
    """
    evidence_id: str
    evidence_type: EvidenceType
    description: str
    collection_date: str
    collected_by: str

    def to_dictionary(self) -> Dict[str, Any]:
        """
        Convierte la evidencia en un diccionario para serialización.
        Maneja el Enum de tipo de evidencia para compatibilidad con JSON.

        :return: Diccionario con los datos de la evidencia.
        """
        data = asdict(self)
        data['evidence_type'] = self.evidence_type.name
        return data

    @classmethod
    def from_dictionary(cls, data: Dict[str, Any]) -> 'Evidence':
        """
        Reconstruye un objeto Evidence desde un diccionario.

        :param data: Diccionario con datos de la evidencia.
        :return: Instancia de Evidence.
        """
        data_copy = data.copy()
        data_copy['evidence_type'] = EvidenceType[data['evidence_type']]
        return cls(**data_copy)

    def __str__(self) -> str:
        """
        Representación técnica detallada.
        """
        return (f"EVIDENCIA [{self.evidence_id}] | TIPO: {self.evidence_type.value} | "
                f"FECHA: {self.collection_date} | AGENTE: {self.collected_by}")


@dataclass
class CrimeEvent:
    """
    Representa un hito cronológico dentro de la investigación.
    Almacena detalles geoespaciales y actores involucrados.
    """
    event_id: str
    event_title: str
    event_description: str
    event_date: str
    event_location: str
    involved_suspects: List[str]

    def to_dictionary(self) -> Dict[str, Any]:
        """
        Convierte el evento en un diccionario para serialización.

        :return: Diccionario con los datos del evento.
        """
        return asdict(self)

    @classmethod
    def from_dictionary(cls, data: Dict[str, Any]) -> 'CrimeEvent':
        """
        Reconstruye un objeto CrimeEvent desde un diccionario.

        :param data: Diccionario con datos del evento.
        :return: Instancia de CrimeEvent.
        """
        return cls(**data)

    def __str__(self) -> str:
        """
        Representación textual del suceso cronológico.
        """
        suspects_count = len(self.involved_suspects)
        return (f"EVENTO [{self.event_id}] | {self.event_date} | {self.event_title} | "
                f"UBICACIÓN: {self.event_location} | SOSPECHOSOS: {suspects_count}")
