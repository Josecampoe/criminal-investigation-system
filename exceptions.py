"""
Módulo de excepciones personalizadas del Sistema de Investigación Criminal.

Define las excepciones específicas que se lanzan cuando ocurren errores
controlados en las operaciones de la Pila de Acciones y la Cola de Casos.
Cada excepción hereda de Exception y proporciona un mensaje descriptivo
que facilita la depuración y el manejo de errores en el sistema.
"""


class EmptyStackError(Exception):
    """
    Excepción lanzada cuando se intenta realizar una operación de extracción
    o consulta sobre una pila de acciones que se encuentra vacía.

    Se utiliza en los métodos pop_action() y peek_action() de ActionStack
    para señalar que no existen acciones disponibles para procesar.
    """

    def __init__(self, message: str = "La pila de acciones está vacía. No hay acciones para deshacer.") -> None:
        """
        Inicializa la excepción con un mensaje descriptivo.

        Parámetros:
            message: Mensaje descriptivo del error ocurrido. Si no se proporciona,
                     se usa un mensaje por defecto que indica que la pila está vacía.
        """
        super().__init__(message)


class EmptyQueueError(Exception):
    """
    Excepción lanzada cuando se intenta obtener o consultar un caso
    de una cola de casos que se encuentra vacía.

    Se utiliza en los métodos dequeue_case() y peek_next_case() de CaseQueue
    para señalar que no existen casos pendientes de asignación.
    """

    def __init__(self, message: str = "La cola de casos está vacía. No hay casos pendientes.") -> None:
        """
        Inicializa la excepción con un mensaje descriptivo.

        Parámetros:
            message: Mensaje descriptivo del error ocurrido. Si no se proporciona,
                     se usa un mensaje por defecto que indica que la cola está vacía.
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
