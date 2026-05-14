class EvidenceNotFoundError(Exception):
    """
    Excepción lanzada cuando no se encuentra una evidencia específica en el sistema.
    Se utiliza principalmente al buscar por el identificador único de la evidencia.
    """
    pass


class EventNotFoundError(Exception):
    """
    Excepción lanzada cuando un evento criminal no existe en la cronología.
    Se utiliza al intentar realizar operaciones sobre un ID de evento inexistente.
    """
    pass


class EmptyListError(Exception):
    """
    Excepción lanzada cuando se intenta realizar una operación de navegación o acceso
    en una lista que no contiene elementos.
    """
    pass
