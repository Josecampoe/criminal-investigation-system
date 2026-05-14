"""
Módulo del Historial de Acciones del Sistema de Investigación Criminal.

Registra cronológicamente cada acción realizada por los investigadores,
permitiendo deshacer operaciones en orden inverso: la última acción
registrada es la primera en poder revertirse.

Este registro es fundamental para el sistema de "deshacer", garantizando
trazabilidad y control sobre cada intervención en los casos activos.
"""

from typing import List

from enumerations import ActionType
from exceptions import NoActionsToUndoError
from models import InvestigatorAction


class InvestigatorActionLog:
    """
    Registra las acciones realizadas por los investigadores y permite
    revertirlas en orden inverso (la más reciente se deshace primero).

    Permite agregar acciones, deshacerlas, consultar la más reciente
    y obtener el historial completo o filtrado por investigador.

    La estructura interna de almacenamiento es privada y no debe accederse
    directamente desde fuera de la clase. Toda interacción se realiza
    exclusivamente a través de los métodos públicos.
    """

    def __init__(self) -> None:
        """
        Inicializa el historial de acciones vacío.
        Las acciones se almacenan en orden cronológico; la última posición
        corresponde a la acción más reciente.
        """
        self.__logged_actions: List[InvestigatorAction] = []

    @property
    def size(self) -> int:
        """
        Propiedad que retorna el número actual de acciones registradas.

        Retorna:
            Número entero con la cantidad de acciones en el historial.
        """
        return len(self.__logged_actions)

    def register_action(self, action: InvestigatorAction) -> None:
        """
        Registra una nueva acción en el historial. La acción queda como
        la más reciente y será la primera en deshacerse si se llama a
        undo_last_action().

        Parámetros:
            action: Instancia de InvestigatorAction que representa la acción a registrar.

        Lanza:
            TypeError: Si la acción proporcionada es None o no es una instancia válida
                       de InvestigatorAction.
        """
        if action is None:
            raise TypeError("La acción no puede ser None. Se requiere una instancia válida de InvestigatorAction.")
        if not isinstance(action, InvestigatorAction):
            raise TypeError(
                f"El parámetro debe ser una instancia de InvestigatorAction, se recibió: {type(action).__name__}."
            )
        self.__logged_actions.append(action)

    def undo_last_action(self) -> InvestigatorAction:
        """
        Revierte la acción más reciente del historial, eliminándola del registro.
        Simula el "deshacer" de la última operación realizada por el investigador.

        Retorna:
            La instancia de InvestigatorAction que fue revertida.

        Lanza:
            NoActionsToUndoError: Si el historial está vacío y no hay acciones para deshacer.
        """
        if self.has_no_recorded_actions():
            raise NoActionsToUndoError()
        return self.__logged_actions.pop()

    def review_latest_action(self) -> InvestigatorAction:
        """
        Retorna la acción más reciente del historial sin eliminarla. Permite
        consultar cuál fue la última operación registrada sin modificar el estado.

        Retorna:
            La instancia de InvestigatorAction más reciente en el historial.

        Lanza:
            NoActionsToUndoError: Si el historial está vacío y no hay acciones para consultar.
        """
        if self.has_no_recorded_actions():
            raise NoActionsToUndoError()
        return self.__logged_actions[-1]

    def has_no_recorded_actions(self) -> bool:
        """
        Verifica si el historial de acciones está vacío. Se usa internamente
        antes de operaciones de extracción y también puede usarse externamente
        para verificar el estado antes de operar.

        Retorna:
            True si no hay acciones registradas, False en caso contrario.
        """
        return len(self.__logged_actions) == 0

    def get_full_history(self) -> List[InvestigatorAction]:
        """
        Retorna una copia de todas las acciones registradas, ordenadas de la
        más reciente a la más antigua. Se retorna una copia para proteger
        la integridad del registro interno.

        Retorna:
            Lista de InvestigatorAction ordenada de más reciente a más antigua.
            Lista vacía si no hay acciones registradas.
        """
        return list(reversed(self.__logged_actions))

    def search_by_investigator(self, investigator_name: str) -> List[InvestigatorAction]:
        """
        Busca y retorna todas las acciones realizadas por un investigador específico,
        ordenadas de la más reciente a la más antigua.

        Parámetros:
            investigator_name: Nombre completo del investigador a buscar.

        Retorna:
            Lista de InvestigatorAction realizadas por el investigador indicado.
            Lista vacía si no se encuentran acciones de ese investigador.

        Lanza:
            ValueError: Si el nombre del investigador está vacío o es None.
        """
        if not investigator_name or not investigator_name.strip():
            raise ValueError("El nombre del investigador no puede estar vacío para realizar la búsqueda.")
        actions_by_investigator = [
            action for action in self.__logged_actions
            if action.investigator_name == investigator_name
        ]
        return list(reversed(actions_by_investigator))

    def count_by_action_type(self, action_type: ActionType) -> int:
        """
        Cuenta cuántas acciones de un tipo específico existen en el historial.

        Parámetros:
            action_type: Tipo de acción a contar, debe ser una instancia de ActionType.

        Retorna:
            Número entero con la cantidad de acciones del tipo especificado.

        Lanza:
            TypeError: Si action_type no es una instancia válida de ActionType.
        """
        if not isinstance(action_type, ActionType):
            raise TypeError(
                f"El parámetro debe ser una instancia de ActionType, se recibió: {type(action_type).__name__}."
            )
        return sum(1 for action in self.__logged_actions if action.action_type == action_type)

    def clear_history(self) -> None:
        """
        Elimina todas las acciones del historial, dejándolo vacío.
        Esta operación es irreversible: una vez limpiado el historial,
        no se pueden recuperar las acciones eliminadas.
        """
        self.__logged_actions.clear()

    def __len__(self) -> int:
        """
        Retorna el número de acciones registradas en el historial.
        Permite usar len(action_log) de forma natural.

        Retorna:
            Número entero con la cantidad de acciones.
        """
        return len(self.__logged_actions)

    def __str__(self) -> str:
        """
        Retorna un resumen legible del estado actual del historial, indicando
        cuántas acciones contiene y cuál es la más reciente.

        Retorna:
            Cadena con el número de acciones y la acción más reciente si existe.
        """
        if self.has_no_recorded_actions():
            return "Historial de acciones vacío. No hay acciones registradas."
        latest = self.__logged_actions[-1]
        return (
            f"Historial de acciones: {len(self.__logged_actions)} acción(es) registrada(s). "
            f"Acción más reciente: [{latest.action_type.value}] por {latest.investigator_name}."
        )
