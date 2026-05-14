"""
Módulo de la Pila de Acciones del Sistema de Investigación Criminal.

Implementa la estructura de datos Pila (Stack - LIFO) para registrar
las acciones realizadas por los investigadores, permitiendo deshacerlas
en orden inverso (la última acción registrada es la primera en deshacerse).

La pila es fundamental para el sistema de "deshacer" (undo), ya que cada
acción que un investigador realiza se apila, y al deshacer se retira
desde la cima hacia abajo.
"""

from typing import List, Optional

from exceptions import EmptyStackError
from models import InvestigatorAction


class ActionStack:
    """
    Implementa una estructura de datos tipo Pila (Stack - LIFO) para registrar
    las acciones realizadas por los investigadores.

    Permite agregar acciones, deshacerlas en orden inverso (la última acción
    registrada es la primera en deshacerse), consultar la acción más reciente
    y obtener el historial completo.

    La estructura interna de almacenamiento es privada y no debe accederse
    directamente desde fuera de la clase. Toda interacción se realiza
    exclusivamente a través de los métodos públicos.
    """

    def __init__(self) -> None:
        """
        Inicializa la pila de acciones con un almacenamiento interno vacío.
        La lista interna almacena las acciones donde el último elemento
        representa la cima de la pila (la acción más reciente).
        """
        self.__action_storage: List[InvestigatorAction] = []

    @property
    def size(self) -> int:
        """
        Propiedad que retorna el número actual de acciones almacenadas en la pila.

        Retorna:
            Número entero con la cantidad de acciones en la pila.
        """
        return len(self.__action_storage)

    def push_action(self, action: InvestigatorAction) -> None:
        """
        Agrega una acción a la cima de la pila. La acción agregada se convierte
        en la más reciente y será la primera en ser deshecha si se llama a pop_action().

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
        self.__action_storage.append(action)

    def pop_action(self) -> InvestigatorAction:
        """
        Elimina y retorna la acción en la cima de la pila (la más reciente).
        Esta operación simula el "deshacer" de la última acción realizada
        por el investigador.

        Retorna:
            La instancia de InvestigatorAction que se encontraba en la cima.

        Lanza:
            EmptyStackError: Si la pila está vacía y no hay acciones para deshacer.
        """
        if self.is_empty():
            raise EmptyStackError()
        return self.__action_storage.pop()

    def peek_action(self) -> InvestigatorAction:
        """
        Retorna la acción en la cima de la pila sin eliminarla. Permite consultar
        cuál fue la última acción registrada sin modificar el estado de la pila.

        Retorna:
            La instancia de InvestigatorAction que se encuentra en la cima.

        Lanza:
            EmptyStackError: Si la pila está vacía y no hay acciones para consultar.
        """
        if self.is_empty():
            raise EmptyStackError()
        return self.__action_storage[-1]

    def is_empty(self) -> bool:
        """
        Verifica si la pila de acciones está vacía. Este método se usa internamente
        antes de operaciones de extracción y también puede usarse externamente
        para verificar el estado antes de operar.

        Retorna:
            True si la pila no contiene acciones, False en caso contrario.
        """
        return len(self.__action_storage) == 0

    def get_full_history(self) -> List[InvestigatorAction]:
        """
        Retorna una copia de todas las acciones almacenadas, ordenadas de la
        más reciente a la más antigua. Se retorna una copia para proteger
        la integridad de la estructura interna.

        Retorna:
            Lista de InvestigatorAction ordenada de más reciente a más antigua.
            Lista vacía si la pila no tiene acciones.
        """
        return list(reversed(self.__action_storage))

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
        matching_actions = [
            action for action in self.__action_storage
            if action.investigator_name == investigator_name
        ]
        return list(reversed(matching_actions))

    def count_by_action_type(self, action_type: "ActionType") -> int:
        """
        Cuenta cuántas acciones de un tipo específico existen en la pila.

        Parámetros:
            action_type: Tipo de acción a contar, debe ser una instancia de ActionType.

        Retorna:
            Número entero con la cantidad de acciones del tipo especificado.

        Lanza:
            TypeError: Si action_type no es una instancia válida de ActionType.
        """
        from enumerations import ActionType as ActionTypeEnum
        if not isinstance(action_type, ActionTypeEnum):
            raise TypeError(
                f"El parámetro debe ser una instancia de ActionType, se recibió: {type(action_type).__name__}."
            )
        return sum(1 for action in self.__action_storage if action.action_type == action_type)

    def clear_history(self) -> None:
        """
        Elimina todas las acciones almacenadas en la pila, dejándola vacía.
        Esta operación es irreversible: una vez limpiado el historial,
        no se pueden recuperar las acciones eliminadas.
        """
        self.__action_storage.clear()

    def __len__(self) -> int:
        """
        Retorna el número de acciones almacenadas en la pila.
        Permite usar len(action_stack) de forma natural.

        Retorna:
            Número entero con la cantidad de acciones.
        """
        return len(self.__action_storage)

    def __str__(self) -> str:
        """
        Retorna un resumen legible del estado actual de la pila, indicando
        cuántas acciones contiene y cuál es la más reciente.

        Retorna:
            Cadena con el número de acciones y la acción más reciente si existe.
        """
        if self.is_empty():
            return "Pila de acciones vacía. No hay acciones registradas."
        top_action = self.__action_storage[-1]
        return (
            f"Pila de acciones: {len(self.__action_storage)} acción(es) registrada(s). "
            f"Acción más reciente: [{top_action.action_type.value}] por {top_action.investigator_name}."
        )
