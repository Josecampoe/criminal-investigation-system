"""
Módulo de modelos de datos del Sistema de Investigación Criminal.

Define las dataclasses que representan las entidades principales del sistema:
las acciones de los investigadores y los casos criminales. Cada modelo incluye
validación de datos en su inicialización para garantizar la integridad de la
información que circula por el sistema.
"""

from dataclasses import dataclass

from enumerations import ActionType, CasePriority


@dataclass
class InvestigatorAction:
    """
    Representa una acción individual realizada por un investigador dentro del sistema.

    Cada acción queda registrada con un identificador único, el tipo de acción,
    una descripción detallada, el nombre del investigador responsable y la marca
    de tiempo en que se realizó. Esta información permite reconstruir el historial
    de operaciones y deshacer acciones cuando sea necesario.

    Atributos:
        action_id: Identificador único de la acción (ejemplo: "ACT-001").
        action_type: Tipo de acción realizada, definido por el enum ActionType.
        description: Descripción detallada de lo que se realizó en esta acción.
        investigator_name: Nombre completo del investigador que ejecutó la acción.
        timestamp: Marca de tiempo en formato "YYYY-MM-DD HH:MM:SS".
    """

    action_id: str
    action_type: ActionType
    description: str
    investigator_name: str
    timestamp: str

    def __post_init__(self) -> None:
        """
        Valida que todos los atributos de la acción sean coherentes y no estén vacíos.

        Lanza:
            ValueError: Si algún atributo de texto está vacío o solo contiene espacios.
            TypeError: Si action_type no es una instancia válida de ActionType.
        """
        if not isinstance(self.action_type, ActionType):
            raise TypeError(
                f"El tipo de acción debe ser una instancia de ActionType, se recibió: {type(self.action_type).__name__}."
            )
        if not self.action_id or not self.action_id.strip():
            raise ValueError("El identificador de la acción (action_id) no puede estar vacío.")
        if not self.description or not self.description.strip():
            raise ValueError("La descripción de la acción no puede estar vacía.")
        if not self.investigator_name or not self.investigator_name.strip():
            raise ValueError("El nombre del investigador no puede estar vacío.")
        if not self.timestamp or not self.timestamp.strip():
            raise ValueError("La marca de tiempo (timestamp) no puede estar vacía.")

    def __str__(self) -> str:
        """
        Retorna una representación legible de la acción del investigador.

        Retorna:
            Cadena formateada con la información completa de la acción, incluyendo
            la marca de tiempo, el identificador, el tipo, el investigador y la descripción.
        """
        return (
            f"[{self.timestamp}] Acción #{self.action_id} | "
            f"Tipo: {self.action_type.value} | "
            f"Investigador: {self.investigator_name} | "
            f"Descripción: {self.description}"
        )


@dataclass
class CriminalCase:
    """
    Representa un caso criminal registrado en el sistema que espera ser asignado
    a un investigador para su resolución.

    Cada caso tiene un identificador único, un título descriptivo, un nivel de
    prioridad, el investigador asignado (cadena vacía si aún no se asigna) y la
    fecha de registro en el sistema.

    Atributos:
        case_id: Identificador único del caso (ejemplo: "CASO-2024-001").
        case_title: Título descriptivo del caso criminal.
        case_priority: Nivel de prioridad del caso, definido por el enum CasePriority.
        assigned_investigator: Nombre del investigador asignado (vacío si no se ha asignado).
        registration_date: Fecha de registro en formato "YYYY-MM-DD HH:MM:SS".
    """

    case_id: str
    case_title: str
    case_priority: CasePriority
    assigned_investigator: str
    registration_date: str

    def __post_init__(self) -> None:
        """
        Valida que todos los atributos del caso sean coherentes y no estén vacíos
        (excepto assigned_investigator que puede estar vacío si el caso no ha sido asignado).

        Lanza:
            ValueError: Si algún atributo obligatorio está vacío o solo contiene espacios.
            TypeError: Si case_priority no es una instancia válida de CasePriority.
        """
        if not isinstance(self.case_priority, CasePriority):
            raise TypeError(
                f"La prioridad del caso debe ser una instancia de CasePriority, se recibió: {type(self.case_priority).__name__}."
            )
        if not self.case_id or not self.case_id.strip():
            raise ValueError("El identificador del caso (case_id) no puede estar vacío.")
        if not self.case_title or not self.case_title.strip():
            raise ValueError("El título del caso (case_title) no puede estar vacío.")
        if not self.registration_date or not self.registration_date.strip():
            raise ValueError("La fecha de registro (registration_date) no puede estar vacía.")

    def __str__(self) -> str:
        """
        Retorna una representación legible del caso criminal.

        Retorna:
            Cadena formateada con la información completa del caso, mostrando
            "Sin asignar" cuando el caso no tiene investigador asignado.
        """
        investigator_display = self.assigned_investigator if self.assigned_investigator else "Sin asignar"
        return (
            f"Caso #{self.case_id} | "
            f"Título: {self.case_title} | "
            f"Prioridad: {self.case_priority.name} | "
            f"Investigador: {investigator_display} | "
            f"Fecha de registro: {self.registration_date}"
        )
