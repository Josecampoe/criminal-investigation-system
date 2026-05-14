"""
Módulo 2 de 8 - Sistema de Investigación Criminal.
Pila de Acciones y Cola de Casos.

Este archivo actúa como punto de entrada del módulo, re-exportando todas las
clases públicas para que puedan importarse directamente desde aquí.
Cualquier módulo externo del sistema puede hacer:

    from stack_and_queue import ActionStack, CaseQueue, InvestigatorAction, ...

sin necesidad de conocer la estructura interna de archivos del módulo.
"""

from exceptions import EmptyStackError, EmptyQueueError, InvalidPriorityError
from enumerations import CasePriority, ActionType
from models import InvestigatorAction, CriminalCase
from action_stack import ActionStack
from case_queue import CaseQueue

__all__ = [
    "EmptyStackError",
    "EmptyQueueError",
    "InvalidPriorityError",
    "CasePriority",
    "ActionType",
    "InvestigatorAction",
    "CriminalCase",
    "ActionStack",
    "CaseQueue",
]
