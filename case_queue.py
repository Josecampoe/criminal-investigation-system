"""
Módulo de la Lista de Casos Pendientes del Sistema de Investigación Criminal.

Gestiona los casos criminales que esperan ser asignados a un investigador,
respetando estrictamente el orden de llegada: el primer caso registrado
es el primero en ser asignado a un investigador disponible.

Esta lista garantiza equidad en la atención de casos y sirve como punto
de despacho centralizado para el equipo de investigación.
"""

from typing import List

from enumerations import CasePriority
from exceptions import NoPendingCasesError, InvalidPriorityError
from models import CriminalCase


class PendingCaseList:
    """
    Gestiona los casos criminales en espera de ser asignados a un investigador.

    Los casos se atienden en el orden en que fueron registrados: el primer caso
    en llegar es el primero en ser asignado. Esto garantiza equidad en la
    distribución de trabajo entre el equipo de investigación.

    La estructura interna de almacenamiento es privada y no debe accederse
    directamente desde fuera de la clase. Toda interacción se realiza
    exclusivamente a través de los métodos públicos.
    """

    def __init__(self) -> None:
        """
        Inicializa la lista de casos pendientes vacía.
        Los casos se almacenan en orden de llegada; el primer elemento (índice 0)
        es el caso más antiguo y el siguiente en ser asignado.
        """
        self.__waiting_cases: List[CriminalCase] = []

    @property
    def size(self) -> int:
        """
        Propiedad que retorna el número actual de casos en espera de asignación.

        Retorna:
            Número entero con la cantidad de casos pendientes.
        """
        return len(self.__waiting_cases)

    def add_case_to_waiting_list(self, criminal_case: CriminalCase) -> None:
        """
        Agrega un caso criminal al final de la lista de espera. El caso ingresado
        aguardará su turno respetando el orden de llegada de los demás casos.

        Parámetros:
            criminal_case: Instancia de CriminalCase que representa el caso a registrar.

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
        self.__waiting_cases.append(criminal_case)

    def assign_next_case(self) -> CriminalCase:
        """
        Retira y retorna el caso más antiguo de la lista de espera para asignarlo
        a un investigador disponible. El caso sale de la lista y pasa a ser trabajado.

        Retorna:
            La instancia de CriminalCase que llevaba más tiempo en espera.

        Lanza:
            NoPendingCasesError: Si la lista de espera está vacía y no hay casos pendientes.
        """
        if self.has_no_pending_cases():
            raise NoPendingCasesError()
        return self.__waiting_cases.pop(0)

    def review_next_pending_case(self) -> CriminalCase:
        """
        Retorna el caso más antiguo de la lista sin retirarlo. Permite consultar
        cuál será el próximo caso en ser asignado sin modificar el estado de la lista.

        Retorna:
            La instancia de CriminalCase que lleva más tiempo en espera.

        Lanza:
            NoPendingCasesError: Si la lista de espera está vacía y no hay casos para consultar.
        """
        if self.has_no_pending_cases():
            raise NoPendingCasesError()
        return self.__waiting_cases[0]

    def has_no_pending_cases(self) -> bool:
        """
        Verifica si la lista de casos pendientes está vacía. Se usa internamente
        antes de operaciones de extracción y también puede usarse externamente
        para verificar el estado antes de operar.

        Retorna:
            True si no hay casos en espera, False en caso contrario.
        """
        return len(self.__waiting_cases) == 0

    def get_pending_cases(self) -> List[CriminalCase]:
        """
        Retorna una copia de todos los casos en espera, en orden de llegada
        (del más antiguo al más reciente). Se retorna una copia para proteger
        la integridad del registro interno.

        Retorna:
            Lista de CriminalCase en el orden en que fueron registrados.
            Lista vacía si no hay casos pendientes.
        """
        return list(self.__waiting_cases)

    def get_cases_by_priority(self, priority: CasePriority) -> List[CriminalCase]:
        """
        Filtra y retorna los casos que coincidan con el nivel de urgencia especificado,
        manteniendo el orden de llegada original. Útil para identificar rápidamente
        los casos más urgentes dentro de la lista de espera.

        Parámetros:
            priority: Nivel de urgencia por el cual filtrar los casos.
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
        return [case for case in self.__waiting_cases if case.case_priority == priority]

    def count_by_priority(self, priority: CasePriority) -> int:
        """
        Cuenta cuántos casos pendientes tienen el nivel de urgencia especificado.
        Útil para obtener estadísticas rápidas sin necesidad de crear una lista filtrada.

        Parámetros:
            priority: Nivel de urgencia a contar. Debe ser una instancia de CasePriority.

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
        return sum(1 for case in self.__waiting_cases if case.case_priority == priority)

    def clear_pending_cases(self) -> None:
        """
        Elimina todos los casos de la lista de espera, dejándola vacía.
        Esta operación es irreversible: una vez vaciada la lista,
        no se pueden recuperar los casos eliminados.
        """
        self.__waiting_cases.clear()

    def __len__(self) -> int:
        """
        Retorna el número de casos pendientes en la lista de espera.
        Permite usar len(pending_case_list) de forma natural.

        Retorna:
            Número entero con la cantidad de casos en espera.
        """
        return len(self.__waiting_cases)

    def __str__(self) -> str:
        """
        Retorna un resumen legible del estado actual de la lista de espera,
        indicando cuántos casos están pendientes y cuál es el siguiente a atender.

        Retorna:
            Cadena con el número de casos pendientes y el próximo caso a asignar.
        """
        if self.has_no_pending_cases():
            return "Lista de casos pendientes vacía. No hay casos en espera de asignación."
        next_case = self.__waiting_cases[0]
        return (
            f"Lista de casos pendientes: {len(self.__waiting_cases)} caso(s) en espera. "
            f"Próximo caso a asignar: [{next_case.case_id}] {next_case.case_title} "
            f"(Urgencia: {next_case.case_priority.name})."
        )
