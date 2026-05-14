"""
Módulo de excepciones personalizadas del Sistema de Investigación Criminal.

Define las excepciones específicas que se lanzan cuando ocurren errores
controlados en las operaciones del historial de acciones y la lista de
casos pendientes. Cada excepción hereda de Exception y proporciona un
mensaje descriptivo que facilita la depuración y el manejo de errores.
"""


class NoActionsToUndoError(Exception):
    """
    Excepción lanzada cuando se intenta deshacer o consultar una acción
    en un historial que se encuentra vacío.

    Se utiliza en los métodos undo_last_action() y review_latest_action()
    de InvestigatorActionLog para señalar que no existen acciones registradas.
    """

    def __init__(self, message: str = "El historial de acciones está vacío. No hay acciones para deshacer.") -> None:
        """
        Inicializa la excepción con un mensaje descriptivo.

        Parámetros:
            message: Mensaje descriptivo del error ocurrido. Si no se proporciona,
                     se usa un mensaje por defecto que indica que el historial está vacío.
        """
        super().__init__(message)


class NoPendingCasesError(Exception):
    """
    Excepción lanzada cuando se intenta asignar o consultar un caso
    en una lista de espera que se encuentra vacía.

    Se utiliza en los métodos assign_next_case() y review_next_pending_case()
    de PendingCaseList para señalar que no existen casos pendientes de asignación.
    """

    def __init__(self, message: str = "La lista de espera está vacía. No hay casos pendientes de asignación.") -> None:
        """
        Inicializa la excepción con un mensaje descriptivo.

        Parámetros:
            message: Mensaje descriptivo del error ocurrido. Si no se proporciona,
                     se usa un mensaje por defecto que indica que la lista está vacía.
        """
        super().__init__(message)


class InvalidPriorityError(Exception):
    """
    Excepción lanzada cuando se proporciona un valor de prioridad
    que no corresponde a ninguno de los niveles válidos definidos en CasePriority.

    Se utiliza en métodos que reciben un parámetro de prioridad para filtrar
    o clasificar casos criminales.
    """

    def __init__(self, message: str = "La prioridad proporcionada no es válida.") -> None:
        """
        Inicializa la excepción con un mensaje descriptivo.

        Parámetros:
            message: Mensaje descriptivo del error ocurrido. Si no se proporciona,
                     se usa un mensaje por defecto que indica que la prioridad es inválida.
        """
        super().__init__(message)
