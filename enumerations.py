"""
Módulo de enumeraciones del Sistema de Investigación Criminal.

Define los tipos enumerados que representan las prioridades de los casos
criminales y los tipos de acciones que puede realizar un investigador.
Estos enums garantizan que solo se usen valores válidos y predefinidos
en todo el sistema, evitando errores por cadenas mal escritas.
"""

from enum import Enum


class CasePriority(Enum):
    """
    Enumeración que representa los niveles de prioridad de un caso criminal.

    Los valores numéricos indican la urgencia relativa, donde un número mayor
    implica mayor prioridad de atención. Se usan para clasificar y filtrar
    los casos en la cola de espera.

    Valores:
        LOW (1): Casos menores que no requieren atención inmediata.
        MEDIUM (2): Casos de gravedad moderada con tiempo razonable de respuesta.
        HIGH (3): Casos graves que requieren atención prioritaria.
        CRITICAL (4): Casos de máxima urgencia que requieren respuesta inmediata.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ActionType(Enum):
    """
    Enumeración que representa los tipos de acciones que un investigador
    puede realizar dentro del sistema de investigación criminal.

    Cada valor describe una operación específica que queda registrada
    en la pila de acciones para poder deshacerla si es necesario.

    Valores:
        ADD_SUSPECT: Agregar un sospechoso a un caso.
        REMOVE_SUSPECT: Eliminar un sospechoso de un caso.
        ADD_EVIDENCE: Registrar una nueva evidencia en un caso.
        LINK_EVIDENCE: Vincular una evidencia existente con un sospechoso o caso.
        OPEN_CASE: Abrir un nuevo caso de investigación.
        CLOSE_CASE: Cerrar un caso de investigación.
    """

    ADD_SUSPECT = "ADD_SUSPECT"
    REMOVE_SUSPECT = "REMOVE_SUSPECT"
    ADD_EVIDENCE = "ADD_EVIDENCE"
    LINK_EVIDENCE = "LINK_EVIDENCE"
    OPEN_CASE = "OPEN_CASE"
    CLOSE_CASE = "CLOSE_CASE"
