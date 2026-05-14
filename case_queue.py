"""
Módulo de la Cola de Casos del Sistema de Investigación Criminal.

Implementa la estructura de datos Cola (Queue - FIFO) para gestionar
los casos criminales que esperan ser asignados a un investigador,
respetando el orden de llegada.

La cola garantiza que los casos se atiendan de forma justa: el primer
caso registrado es el primero en ser asignado a un investigador disponible.
"""

from typing import List

from enumerations import CasePriority
from exceptions import EmptyQueueError, InvalidPriorityError
from models import CriminalCase


class CaseQueue:
    """
    Implementa una estructura de datos tipo Cola (Queue - FIFO) para gestionar
    los casos criminales que esperan ser asignados a un investigador.

    Los casos se atienden en el orden en que fueron registrados: el primer caso
    en llegar es el primero en ser asignado. Esto garantiza equidad en la
    atención de los casos.

    La estructura interna de almacenamiento es privada y no debe accederse
    directamente desde fuera de la clase. Toda interacción se realiza
    exclusivamente a través de los métodos públicos.
    """

    def __init__(self) -> None:
        """
        Inicializa la cola de casos con un almacenamiento interno vacío.
        La lista interna almacena los casos donde el primer elemento (índice 0)
        representa el frente de la cola (el caso más antiguo en espera).
        """
        self.__case_storage: List[CriminalCase] = []

    @property
    def size(self) -> int:
        """
        Propiedad que retorna el número actual de casos en espera dentro de la cola.

        Retorna:
            Número entero con la cantidad de casos pendientes de asignación.
        """
        return len(self.__case_storage)

    def enqueue_case(self, criminal_case: CriminalCase) -> None:
        """
        Agrega un caso criminal al final de la cola de espera. El caso agregado
        será el último en ser atendido, respetando el orden FIFO.

        Parámetros:
            criminal_case: Instancia de CriminalCase que representa el caso a encolar.

        Lanza:
            TypeError: Si el caso proporcionado es None o no es una instancia válida
                       de CriminalCase.
        """
        if criminal_case is None:
            raise TypeError("El caso no puede ser None. Se requiere una instancia válida de CriminalCase.")
        if not isinstance(criminal_case, CriminalCase):
            raise TypeError(
                f"El parámetro debe ser una instancia de CriminalCase, se recibió: {type(criminal_case).__name__}."
            )
        self.__case_storage.append(criminal_case)

    def dequeue_case(self) -> CriminalCase:
        """
        Elimina y retorna el caso al frente de la cola (el primero en haber llegado).
        Esta operación simula la asignación de un caso a un investigador: el caso
        sale de la cola de espera para ser trabajado.

        Retorna:
            La instancia de CriminalCase que se encontraba al frente de la cola.

        Lanza:
            EmptyQueueError: Si la cola está vacía y no hay casos pendientes.
        """
        if self.is_empty():
            raise EmptyQueueError()
        return self.__case_storage.pop(0)

    def peek_next_case(self) -> CriminalCase:
        """
        Retorna el caso al frente de la cola sin eliminarlo. Permite consultar
        cuál es el siguiente caso que será asignado sin modificar el estado de la cola.

        Retorna:
            La instancia de CriminalCase que se encuentra al frente de la cola.

        Lanza:
            EmptyQueueError: Si la cola está vacía y no hay casos para consultar.
        """
        if self.is_empty():
            raise EmptyQueueError()
        return self.__case_storage[0]

    def is_empty(self) -> bool:
        """
        Verifica si la cola de casos está vacía. Este método se usa internamente
        antes de operaciones de extracción y también puede usarse externamente
        para verificar el estado antes de operar.

        Retorna:
            True si la cola no contiene casos pendientes, False en caso contrario.
        """
        return len(self.__case_storage) == 0

    def get_pending_cases(self) -> List[CriminalCase]:
        """
        Retorna una copia de todos los casos pendientes en orden de llegada
        (del más antiguo al más reciente). Se retorna una copia para proteger
        la integridad de la estructura interna.

        Retorna:
            Lista de CriminalCase en el orden en que fueron registrados.
            Lista vacía si no hay casos pendientes.
        """
        return list(self.__case_storage)

    def get_cases_by_priority(self, priority: CasePriority) -> List[CriminalCase]:
        """
        Filtra y retorna una lista de casos que coincidan con la prioridad especificada,
        manteniendo el orden de llegada original. Útil para identificar rápidamente
        los casos más urgentes dentro de la cola.

        Parámetros:
            priority: Nivel de prioridad por el cual filtrar los casos.
                      Debe ser una instancia válida del enum CasePriority.

        Retorna:
            Lista de CriminalCase cuya prioridad coincide con la proporcionada.
            Lista vacía si no hay casos con esa prioridad.

        Lanza:
            InvalidPriorityError: Si la prioridad proporcionada no es una instancia
                                  válida de CasePriority.
        """
        if not isinstance(priority, CasePriority):
            raise InvalidPriorityError(
                f"La prioridad '{priority}' no es válida. Use un valor del enum CasePriority "
                f"(LOW, MEDIUM, HIGH, CRITICAL)."
            )
        return [case for case in self.__case_storage if case.case_priority == priority]

    def count_by_priority(self, priority: CasePriority) -> int:
        """
        Cuenta cuántos casos pendientes tienen la prioridad especificada.
        Útil para obtener estadísticas rápidas sin necesidad de crear una lista filtrada.

        Parámetros:
            priority: Nivel de prioridad a contar. Debe ser una instancia de CasePriority.

        Retorna:
            Número entero con la cantidad de casos que tienen la prioridad indicada.

        Lanza:
            InvalidPriorityError: Si la prioridad proporcionada no es una instancia
                                  válida de CasePriority.
        """
        if not isinstance(priority, CasePriority):
            raise InvalidPriorityError(
                f"La prioridad '{priority}' no es válida. Use un valor del enum CasePriority "
                f"(LOW, MEDIUM, HIGH, CRITICAL)."
            )
        return sum(1 for case in self.__case_storage if case.case_priority == priority)

    def clear_queue(self) -> None:
        """
        Elimina todos los casos pendientes de la cola, dejándola vacía.
        Esta operación es irreversible: una vez vaciada la cola,
        no se pueden recuperar los casos eliminados.
        """
        self.__case_storage.clear()

    def __len__(self) -> int:
        """
        Retorna el número de casos pendientes en la cola.
        Permite usar len(case_queue) de forma natural.

        Retorna:
            Número entero con la cantidad de casos en espera.
        """
        return len(self.__case_storage)

    def __str__(self) -> str:
        """
        Retorna un resumen legible del estado actual de la cola, indicando
        cuántos casos están pendientes y cuál es el siguiente a ser atendido.

        Retorna:
            Cadena con el número de casos pendientes y el siguiente caso a atender.
        """
        if self.is_empty():
            return "Cola de casos vacía. No hay casos pendientes de asignación."
        next_case = self.__case_storage[0]
        return (
            f"Cola de casos: {len(self.__case_storage)} caso(s) pendiente(s). "
            f"Siguiente caso: [{next_case.case_id}] {next_case.case_title} "
            f"(Prioridad: {next_case.case_priority.name})."
        )
