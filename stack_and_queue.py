"""
Módulo 2 de 8 - Sistema de Investigación Criminal.
Historial de Acciones y Lista de Casos Pendientes.

Este archivo actúa como punto de entrada del módulo, re-exportando todas las
clases públicas para que puedan importarse directamente desde aquí.
Cualquier módulo externo del sistema puede hacer:

    from stack_and_queue import InvestigatorActionLog, PendingCaseList, InvestigatorAction, ...

sin necesidad de conocer la estructura interna de archivos del módulo.
"""

from exceptions import NoActionsToUndoError, NoPendingCasesError, InvalidPriorityError
from enumerations import CasePriority, ActionType
from models import InvestigatorAction, CriminalCase
from action_stack import InvestigatorActionLog
from case_queue import PendingCaseList

__all__ = [
    "NoActionsToUndoError",
    "NoPendingCasesError",
    "InvalidPriorityError",
    "CasePriority",
    "ActionType",
    "InvestigatorAction",
    "CriminalCase",
    "InvestigatorActionLog",
    "PendingCaseList",
]


if __name__ == "__main__":

    print("=" * 80)
    print("  SISTEMA DE INVESTIGACIÓN CRIMINAL")
    print("  Módulo 2: Historial de Acciones y Lista de Casos Pendientes")
    print("=" * 80)

    # =========================================================================
    # SECCIÓN 1: Demostración del Historial de Acciones (InvestigatorActionLog)
    # Se simula una jornada de trabajo completa de un equipo de investigación.
    # Primero se registran las acciones cronológicamente, luego se demuestra
    # cómo deshacer las más recientes, consultar la última, buscar por
    # investigador y contar por tipo de acción.
    # =========================================================================

    print("\n" + "-" * 80)
    print("  SECCIÓN 1: HISTORIAL DE ACCIONES - Simulación de jornada de trabajo")
    print("-" * 80)

    # Creación del historial de acciones para el equipo de investigación
    action_log = InvestigatorActionLog()

    # Se verifica que el historial inicia vacío
    print(f"\n>>> Historial recién creado - ¿Sin acciones?: {action_log.has_no_recorded_actions()}")
    print(f">>> Tamaño inicial: {len(action_log)}")

    # Registro de 6 acciones de diferentes tipos simulando un caso real de robo
    actions_to_register = [
        InvestigatorAction(
            action_id="ACT-001",
            action_type=ActionType.OPEN_CASE,
            description="Apertura del caso de robo en joyería del centro comercial Plaza Norte",
            investigator_name="Detective María González",
            timestamp="2024-03-15 08:30:00"
        ),
        InvestigatorAction(
            action_id="ACT-002",
            action_type=ActionType.ADD_SUSPECT,
            description="Se agrega a Carlos Mendoza como sospechoso principal por coincidencia con descripción de testigos",
            investigator_name="Detective María González",
            timestamp="2024-03-15 09:15:00"
        ),
        InvestigatorAction(
            action_id="ACT-003",
            action_type=ActionType.ADD_EVIDENCE,
            description="Se registra grabación de cámara de seguridad del estacionamiento como evidencia clave",
            investigator_name="Detective María González",
            timestamp="2024-03-15 10:00:00"
        ),
        InvestigatorAction(
            action_id="ACT-004",
            action_type=ActionType.ADD_EVIDENCE,
            description="Se registran huellas dactilares encontradas en la vitrina rota como evidencia forense",
            investigator_name="Perito Forense Juan Ramírez",
            timestamp="2024-03-15 11:30:00"
        ),
        InvestigatorAction(
            action_id="ACT-005",
            action_type=ActionType.LINK_EVIDENCE,
            description="Se vinculan las huellas dactilares con el sospechoso Carlos Mendoza mediante base de datos AFIS",
            investigator_name="Perito Forense Juan Ramírez",
            timestamp="2024-03-15 14:00:00"
        ),
        InvestigatorAction(
            action_id="ACT-006",
            action_type=ActionType.ADD_SUSPECT,
            description="Se agrega a Roberto Díaz como segundo sospechoso por aparecer en video de seguridad",
            investigator_name="Detective María González",
            timestamp="2024-03-15 15:45:00"
        ),
    ]

    # Se registran todas las acciones en el historial una por una
    print("\n>>> Registrando acciones del equipo de investigación...")
    for action in actions_to_register:
        action_log.register_action(action)
        print(f"  + Registrada: {action.action_type.value} por {action.investigator_name}")

    # Se verifica que el historial ya no está vacío y el tamaño es coherente
    print(f"\n>>> ¿Sin acciones después de registrar?: {action_log.has_no_recorded_actions()}")
    print(f">>> Tamaño actual: {len(action_log)}")
    print(f">>> Estado completo: {action_log}")

    # Mostrar el historial completo (de más reciente a más antigua)
    print("\n>>> Historial completo de acciones (más reciente primero):")
    full_history = action_log.get_full_history()
    for index, historical_action in enumerate(full_history, start=1):
        print(f"  {index}. {historical_action}")

    # Buscar acciones por investigador específico
    print("\n>>> Buscando acciones del Perito Forense Juan Ramírez:")
    forensic_actions = action_log.search_by_investigator("Perito Forense Juan Ramírez")
    for index, forensic_action in enumerate(forensic_actions, start=1):
        print(f"  {index}. {forensic_action}")

    # Contar acciones por tipo
    print("\n>>> Conteo de acciones por tipo:")
    print(f"  - ADD_EVIDENCE: {action_log.count_by_action_type(ActionType.ADD_EVIDENCE)}")
    print(f"  - ADD_SUSPECT: {action_log.count_by_action_type(ActionType.ADD_SUSPECT)}")
    print(f"  - LINK_EVIDENCE: {action_log.count_by_action_type(ActionType.LINK_EVIDENCE)}")
    print(f"  - OPEN_CASE: {action_log.count_by_action_type(ActionType.OPEN_CASE)}")

    # Consultar la acción más reciente sin eliminarla
    latest_action = action_log.review_latest_action()
    print(f"\n>>> Acción más reciente (sin eliminar): {latest_action}")
    print(f">>> Tamaño después de la consulta (no debe cambiar): {len(action_log)}")

    # Deshacer las últimas 2 acciones y mostrar el resultado
    print("\n>>> Deshaciendo las últimas 2 acciones...")
    for undo_number in range(1, 3):
        undone_action = action_log.undo_last_action()
        print(f"  - Deshecha #{undo_number}: {undone_action}")

    # Verificar coherencia: el tamaño debe haber disminuido en 2
    print(f"\n>>> Tamaño después de deshacer 2 acciones: {len(action_log)}")
    print(f">>> Estado actualizado: {action_log}")

    # La nueva acción más reciente debe ser ACT-004
    new_latest = action_log.review_latest_action()
    print(f">>> Nueva acción más reciente: {new_latest}")

    # =========================================================================
    # SECCIÓN 2: Demostración de la Lista de Casos Pendientes (PendingCaseList)
    # Se simula la recepción de casos criminales y su asignación a investigadores
    # respetando el orden de llegada. Se demuestra el registro, la asignación,
    # la consulta del próximo caso, el filtrado por prioridad y el conteo.
    # =========================================================================

    print("\n" + "-" * 80)
    print("  SECCIÓN 2: LISTA DE CASOS PENDIENTES - Simulación de recepción y asignación")
    print("-" * 80)

    # Creación de la lista de casos pendientes
    pending_case_list = PendingCaseList()

    # Se verifica que la lista inicia vacía
    print(f"\n>>> Lista recién creada - ¿Sin casos pendientes?: {pending_case_list.has_no_pending_cases()}")
    print(f">>> Tamaño inicial: {len(pending_case_list)}")

    # Registro de 5 casos con diferentes prioridades simulando una semana de trabajo
    cases_to_register = [
        CriminalCase(
            case_id="CASO-2024-001",
            case_title="Robo a mano armada en sucursal bancaria Av. Reforma",
            case_priority=CasePriority.HIGH,
            assigned_investigator="",
            registration_date="2024-03-10 07:00:00"
        ),
        CriminalCase(
            case_id="CASO-2024-002",
            case_title="Fraude electrónico mediante phishing a clientes corporativos",
            case_priority=CasePriority.MEDIUM,
            assigned_investigator="",
            registration_date="2024-03-11 09:30:00"
        ),
        CriminalCase(
            case_id="CASO-2024-003",
            case_title="Secuestro exprés reportado en zona residencial Las Lomas",
            case_priority=CasePriority.CRITICAL,
            assigned_investigator="",
            registration_date="2024-03-12 06:15:00"
        ),
        CriminalCase(
            case_id="CASO-2024-004",
            case_title="Vandalismo en propiedad pública del parque central",
            case_priority=CasePriority.LOW,
            assigned_investigator="",
            registration_date="2024-03-12 11:00:00"
        ),
        CriminalCase(
            case_id="CASO-2024-005",
            case_title="Homicidio doloso en estacionamiento del centro comercial",
            case_priority=CasePriority.CRITICAL,
            assigned_investigator="",
            registration_date="2024-03-13 03:45:00"
        ),
    ]

    # Se agregan todos los casos a la lista de espera uno por uno
    print("\n>>> Registrando casos criminales en la lista de espera...")
    for case in cases_to_register:
        pending_case_list.add_case_to_waiting_list(case)
        print(f"  + Registrado: [{case.case_id}] {case.case_title} (Prioridad: {case.case_priority.name})")

    # Se verifica que la lista ya no está vacía y el tamaño es coherente
    print(f"\n>>> ¿Sin casos pendientes después de registrar?: {pending_case_list.has_no_pending_cases()}")
    print(f">>> Tamaño actual: {len(pending_case_list)}")
    print(f">>> Estado completo: {pending_case_list}")

    # Mostrar todos los casos pendientes en orden de llegada
    print("\n>>> Casos pendientes en orden de llegada:")
    pending_cases = pending_case_list.get_pending_cases()
    for index, pending_case in enumerate(pending_cases, start=1):
        print(f"  {index}. {pending_case}")

    # Consultar el siguiente caso sin retirarlo de la lista
    next_case = pending_case_list.review_next_pending_case()
    print(f"\n>>> Próximo caso a asignar (sin retirarlo): {next_case}")
    print(f">>> Tamaño después de la consulta (no debe cambiar): {len(pending_case_list)}")

    # Filtrar casos por prioridad CRITICAL
    print("\n>>> Filtrando casos con prioridad CRITICAL:")
    critical_cases = pending_case_list.get_cases_by_priority(CasePriority.CRITICAL)
    for index, critical_case in enumerate(critical_cases, start=1):
        print(f"  {index}. {critical_case}")

    # Asignar los primeros 2 casos y mostrar quién fue asignado
    print("\n>>> Asignando los primeros 2 casos a investigadores disponibles...")
    investigators_available = ["Detective María González", "Detective Carlos Herrera"]

    for investigator_index in range(2):
        assigned_case = pending_case_list.assign_next_case()
        assigned_case.assigned_investigator = investigators_available[investigator_index]
        print(f"  - Caso [{assigned_case.case_id}] asignado a: {assigned_case.assigned_investigator}")
        print(f"    Título: {assigned_case.case_title}")

    # Verificar coherencia: el tamaño debe haber disminuido en 2
    print(f"\n>>> Tamaño después de asignar 2 casos: {len(pending_case_list)}")
    print(f">>> Estado actualizado: {pending_case_list}")

    # El nuevo próximo caso debe ser CASO-2024-003
    new_next = pending_case_list.review_next_pending_case()
    print(f">>> Nuevo próximo caso en espera: {new_next}")

    # Verificar que los casos CRITICAL restantes se actualizaron correctamente
    print("\n>>> Casos CRITICAL restantes después de las asignaciones:")
    remaining_critical = pending_case_list.get_cases_by_priority(CasePriority.CRITICAL)
    for index, remaining_case in enumerate(remaining_critical, start=1):
        print(f"  {index}. {remaining_case}")

    # =========================================================================
    # SECCIÓN 3: Demostración del manejo de errores
    # Se provocan intencionalmente errores para verificar que las excepciones
    # personalizadas funcionan correctamente y que el sistema responde de forma
    # predecible ante entradas inválidas o estados vacíos.
    # =========================================================================

    print("\n" + "-" * 80)
    print("  SECCIÓN 3: MANEJO DE ERRORES - Verificación de excepciones")
    print("-" * 80)

    # Intentar deshacer una acción en un historial vacío (debe lanzar NoActionsToUndoError)
    print("\n>>> Intentando undo_last_action() en un historial vacío...")
    empty_log = InvestigatorActionLog()
    try:
        empty_log.undo_last_action()
    except NoActionsToUndoError as error:
        print(f"  + NoActionsToUndoError capturado: {error}")

    # Intentar consultar la última acción en un historial vacío (debe lanzar NoActionsToUndoError)
    print("\n>>> Intentando review_latest_action() en un historial vacío...")
    try:
        empty_log.review_latest_action()
    except NoActionsToUndoError as error:
        print(f"  + NoActionsToUndoError capturado: {error}")

    # Intentar asignar un caso de una lista vacía (debe lanzar NoPendingCasesError)
    print("\n>>> Intentando assign_next_case() en una lista vacía...")
    empty_list = PendingCaseList()
    try:
        empty_list.assign_next_case()
    except NoPendingCasesError as error:
        print(f"  + NoPendingCasesError capturado: {error}")

    # Intentar consultar el próximo caso en una lista vacía (debe lanzar NoPendingCasesError)
    print("\n>>> Intentando review_next_pending_case() en una lista vacía...")
    try:
        empty_list.review_next_pending_case()
    except NoPendingCasesError as error:
        print(f"  + NoPendingCasesError capturado: {error}")

    # Intentar filtrar con una prioridad inválida (debe lanzar InvalidPriorityError)
    print("\n>>> Intentando get_cases_by_priority() con prioridad inválida...")
    try:
        pending_case_list.get_cases_by_priority("URGENTE")  # type: ignore
    except InvalidPriorityError as error:
        print(f"  + InvalidPriorityError capturado: {error}")

    # Intentar agregar None como acción (debe lanzar TypeError)
    print("\n>>> Intentando register_action(None)...")
    try:
        action_log.register_action(None)  # type: ignore
    except TypeError as error:
        print(f"  + TypeError capturado: {error}")

    # Intentar agregar None como caso (debe lanzar TypeError)
    print("\n>>> Intentando add_case_to_waiting_list(None)...")
    try:
        pending_case_list.add_case_to_waiting_list(None)  # type: ignore
    except TypeError as error:
        print(f"  + TypeError capturado: {error}")

    # Intentar crear una acción con descripción vacía (debe lanzar ValueError)
    print("\n>>> Intentando crear InvestigatorAction con descripción vacía...")
    try:
        InvestigatorAction(
            action_id="ACT-999",
            action_type=ActionType.ADD_SUSPECT,
            description="",
            investigator_name="Detective Prueba",
            timestamp="2024-01-01 00:00:00"
        )
    except ValueError as error:
        print(f"  + ValueError capturado: {error}")

    # Intentar crear un caso con prioridad inválida (debe lanzar TypeError)
    print("\n>>> Intentando crear CriminalCase con prioridad inválida...")
    try:
        CriminalCase(
            case_id="CASO-999",
            case_title="Caso de prueba",
            case_priority="ALTA",  # type: ignore
            assigned_investigator="",
            registration_date="2024-01-01 00:00:00"
        )
    except TypeError as error:
        print(f"  + TypeError capturado: {error}")

    # Limpiar el historial y verificar que queda vacío
    print("\n>>> Limpiando historial de acciones con clear_history()...")
    print(f"  Antes: {len(action_log)} acciones")
    action_log.clear_history()
    print(f"  Después: {len(action_log)} acciones — ¿Sin acciones?: {action_log.has_no_recorded_actions()}")

    # Limpiar la lista de casos y verificar que queda vacía
    print("\n>>> Limpiando lista de casos pendientes con clear_pending_cases()...")
    print(f"  Antes: {len(pending_case_list)} casos")
    pending_case_list.clear_pending_cases()
    print(f"  Después: {len(pending_case_list)} casos — ¿Sin pendientes?: {pending_case_list.has_no_pending_cases()}")

    print("\n" + "=" * 80)
    print("  Demostración completada exitosamente.")
    print("  Módulo listo para ser importado por el sistema principal.")
    print("=" * 80)
