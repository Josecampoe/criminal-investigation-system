"""
Archivo principal de demostración del Módulo 2 - Sistema de Investigación Criminal.

Ejecuta una simulación completa que demuestra el funcionamiento de la Pila de
Acciones (ActionStack) y la Cola de Casos (CaseQueue), incluyendo el manejo
de errores con excepciones personalizadas.

Este archivo importa todo desde stack_and_queue.py, demostrando que el módulo
puede ser consumido sin problemas por otros componentes del sistema.
"""

from stack_and_queue import (
    ActionStack,
    CaseQueue,
    InvestigatorAction,
    CriminalCase,
    CasePriority,
    ActionType,
    EmptyStackError,
    EmptyQueueError,
    InvalidPriorityError,
)


if __name__ == "__main__":

    print("=" * 80)
    print("  SISTEMA DE INVESTIGACIÓN CRIMINAL")
    print("  Módulo 2: Pila de Acciones y Cola de Casos")
    print("=" * 80)

    # =========================================================================
    # SECCIÓN 1: Demostración de la Pila de Acciones (ActionStack)
    # Se simula una jornada de trabajo completa de un equipo de investigación.
    # Primero se registran las acciones cronológicamente, luego se demuestra
    # cómo deshacer las más recientes, consultar la cima, buscar por
    # investigador y contar por tipo de acción.
    # =========================================================================

    print("\n" + "-" * 80)
    print("  SECCIÓN 1: PILA DE ACCIONES - Simulación de jornada de trabajo")
    print("-" * 80)

    # Creación de la pila de acciones para el equipo de investigación
    action_stack = ActionStack()

    # Se verifica que la pila inicia vacía (coherencia: is_empty y size deben coincidir)
    print(f"\n>>> Pila recién creada - ¿Está vacía?: {action_stack.is_empty()}")
    print(f">>> Tamaño inicial: {action_stack.size}")

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

    # Se registran todas las acciones en la pila una por una
    print("\n>>> Registrando acciones del equipo de investigación...")
    for action in actions_to_register:
        action_stack.push_action(action)
        print(f"  + Registrada: {action.action_type.value} por {action.investigator_name}")

    # Se verifica que la pila ya no está vacía y el tamaño es coherente
    print(f"\n>>> ¿Pila vacía después de registrar?: {action_stack.is_empty()}")
    print(f">>> Tamaño actual (size): {action_stack.size}")
    print(f">>> Tamaño actual (len): {len(action_stack)}")
    print(f">>> Estado completo: {action_stack}")

    # Mostrar el historial completo (de más reciente a más antigua)
    print("\n>>> Historial completo de acciones (más reciente primero):")
    full_history = action_stack.get_full_history()
    for index, historical_action in enumerate(full_history, start=1):
        print(f"  {index}. {historical_action}")

    # Buscar acciones por investigador específico
    print("\n>>> Buscando acciones del Perito Forense Juan Ramírez:")
    forensic_actions = action_stack.search_by_investigator("Perito Forense Juan Ramírez")
    for index, forensic_action in enumerate(forensic_actions, start=1):
        print(f"  {index}. {forensic_action}")

    # Contar acciones por tipo
    print("\n>>> Conteo de acciones por tipo:")
    print(f"  - ADD_EVIDENCE: {action_stack.count_by_action_type(ActionType.ADD_EVIDENCE)}")
    print(f"  - ADD_SUSPECT: {action_stack.count_by_action_type(ActionType.ADD_SUSPECT)}")
    print(f"  - LINK_EVIDENCE: {action_stack.count_by_action_type(ActionType.LINK_EVIDENCE)}")
    print(f"  - OPEN_CASE: {action_stack.count_by_action_type(ActionType.OPEN_CASE)}")

    # Consultar la acción en la cima sin eliminarla (peek)
    top_action = action_stack.peek_action()
    print(f"\n>>> Acción en la cima (peek, sin eliminar): {top_action}")
    print(f">>> Tamaño después del peek (no debe cambiar): {len(action_stack)}")

    # Deshacer las últimas 2 acciones (pop) y mostrar el resultado
    print("\n>>> Deshaciendo las últimas 2 acciones (pop)...")
    for undo_number in range(1, 3):
        undone_action = action_stack.pop_action()
        print(f"  - Deshecha #{undo_number}: {undone_action}")

    # Verificar coherencia: el tamaño debe haber disminuido en 2
    print(f"\n>>> Tamaño después de deshacer 2 acciones: {len(action_stack)}")
    print(f">>> Estado actualizado: {action_stack}")

    # La nueva cima debe ser la acción ACT-004 (la que estaba debajo de las 2 eliminadas)
    new_top = action_stack.peek_action()
    print(f">>> Nueva cima de la pila: {new_top}")

    # =========================================================================
    # SECCIÓN 2: Demostración de la Cola de Casos (CaseQueue)
    # Se simula la recepción de casos criminales y su asignación a investigadores
    # respetando el orden de llegada. Se demuestra el encolado, desencolado,
    # consulta del frente, filtrado por prioridad y conteo.
    # =========================================================================

    print("\n" + "-" * 80)
    print("  SECCIÓN 2: COLA DE CASOS - Simulación de recepción y asignación")
    print("-" * 80)

    # Creación de la cola de casos
    case_queue = CaseQueue()

    # Se verifica que la cola inicia vacía (coherencia: is_empty y size deben coincidir)
    print(f"\n>>> Cola recién creada - ¿Está vacía?: {case_queue.is_empty()}")
    print(f">>> Tamaño inicial: {case_queue.size}")

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

    # Se agregan todos los casos a la cola uno por uno
    print("\n>>> Registrando casos criminales en la cola de espera...")
    for case in cases_to_register:
        case_queue.enqueue_case(case)
        print(f"  + Registrado: [{case.case_id}] {case.case_title} (Prioridad: {case.case_priority.name})")

    # Se verifica que la cola ya no está vacía y el tamaño es coherente
    print(f"\n>>> ¿Cola vacía después de registrar?: {case_queue.is_empty()}")
    print(f">>> Tamaño actual (size): {case_queue.size}")
    print(f">>> Tamaño actual (len): {len(case_queue)}")
    print(f">>> Estado completo: {case_queue}")

    # Mostrar todos los casos pendientes en orden de llegada
    print("\n>>> Casos pendientes en orden de llegada (FIFO):")
    pending_cases = case_queue.get_pending_cases()
    for index, pending_case in enumerate(pending_cases, start=1):
        print(f"  {index}. {pending_case}")

    # Consultar el siguiente caso sin eliminarlo (peek)
    next_case = case_queue.peek_next_case()
    print(f"\n>>> Siguiente caso a atender (peek, sin eliminar): {next_case}")
    print(f">>> Tamaño después del peek (no debe cambiar): {len(case_queue)}")

    # Conteo de casos por prioridad
    print("\n>>> Conteo de casos por prioridad:")
    print(f"  - CRITICAL: {case_queue.count_by_priority(CasePriority.CRITICAL)}")
    print(f"  - HIGH: {case_queue.count_by_priority(CasePriority.HIGH)}")
    print(f"  - MEDIUM: {case_queue.count_by_priority(CasePriority.MEDIUM)}")
    print(f"  - LOW: {case_queue.count_by_priority(CasePriority.LOW)}")

    # Filtrar casos por prioridad CRITICAL
    print("\n>>> Filtrando casos con prioridad CRITICAL:")
    critical_cases = case_queue.get_cases_by_priority(CasePriority.CRITICAL)
    for index, critical_case in enumerate(critical_cases, start=1):
        print(f"  {index}. {critical_case}")

    # Asignar los primeros 2 casos (dequeue) y mostrar quién fue asignado
    print("\n>>> Asignando los primeros 2 casos a investigadores (dequeue)...")
    investigators_available = ["Detective María González", "Detective Carlos Herrera"]

    for investigator_index in range(2):
        assigned_case = case_queue.dequeue_case()
        assigned_case.assigned_investigator = investigators_available[investigator_index]
        print(f"  - Caso [{assigned_case.case_id}] asignado a: {assigned_case.assigned_investigator}")
        print(f"    Título: {assigned_case.case_title}")

    # Verificar coherencia: el tamaño debe haber disminuido en 2
    print(f"\n>>> Tamaño después de asignar 2 casos: {len(case_queue)}")
    print(f">>> Estado actualizado: {case_queue}")

    # El nuevo frente debe ser CASO-2024-003 (el que estaba detrás de los 2 asignados)
    new_front = case_queue.peek_next_case()
    print(f">>> Nuevo frente de la cola: {new_front}")

    # Verificar que los casos CRITICAL restantes se actualizaron correctamente
    print("\n>>> Casos CRITICAL restantes después de las asignaciones:")
    remaining_critical = case_queue.get_cases_by_priority(CasePriority.CRITICAL)
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

    # --- Errores de pila vacía ---

    # Intentar deshacer una acción en una pila vacía (debe lanzar EmptyStackError)
    print("\n>>> Intentando pop_action() en una pila vacía...")
    empty_stack = ActionStack()
    try:
        empty_stack.pop_action()
    except EmptyStackError as error:
        print(f"  ✓ EmptyStackError capturado: {error}")

    # Intentar consultar la cima de una pila vacía (debe lanzar EmptyStackError)
    print("\n>>> Intentando peek_action() en una pila vacía...")
    try:
        empty_stack.peek_action()
    except EmptyStackError as error:
        print(f"  ✓ EmptyStackError capturado: {error}")

    # --- Errores de cola vacía ---

    # Intentar obtener un caso de una cola vacía (debe lanzar EmptyQueueError)
    print("\n>>> Intentando dequeue_case() en una cola vacía...")
    empty_queue = CaseQueue()
    try:
        empty_queue.dequeue_case()
    except EmptyQueueError as error:
        print(f"  ✓ EmptyQueueError capturado: {error}")

    # Intentar consultar el siguiente caso en una cola vacía (debe lanzar EmptyQueueError)
    print("\n>>> Intentando peek_next_case() en una cola vacía...")
    try:
        empty_queue.peek_next_case()
    except EmptyQueueError as error:
        print(f"  ✓ EmptyQueueError capturado: {error}")

    # --- Errores de tipo inválido ---

    # Intentar filtrar con una prioridad inválida (debe lanzar InvalidPriorityError)
    print("\n>>> Intentando get_cases_by_priority() con prioridad inválida...")
    try:
        case_queue.get_cases_by_priority("URGENTE")  # type: ignore
    except InvalidPriorityError as error:
        print(f"  ✓ InvalidPriorityError capturado: {error}")

    # Intentar contar con una prioridad inválida (debe lanzar InvalidPriorityError)
    print("\n>>> Intentando count_by_priority() con prioridad inválida...")
    try:
        case_queue.count_by_priority(99)  # type: ignore
    except InvalidPriorityError as error:
        print(f"  ✓ InvalidPriorityError capturado: {error}")

    # --- Errores de parámetros None ---

    # Intentar agregar None como acción (debe lanzar TypeError)
    print("\n>>> Intentando push_action(None)...")
    try:
        action_stack.push_action(None)  # type: ignore
    except TypeError as error:
        print(f"  ✓ TypeError capturado: {error}")

    # Intentar agregar None como caso (debe lanzar TypeError)
    print("\n>>> Intentando enqueue_case(None)...")
    try:
        case_queue.enqueue_case(None)  # type: ignore
    except TypeError as error:
        print(f"  ✓ TypeError capturado: {error}")

    # --- Errores de validación en modelos ---

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
        print(f"  ✓ ValueError capturado: {error}")

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
        print(f"  ✓ TypeError capturado: {error}")

    # --- Demostración de clear (limpieza) ---

    # Limpiar la pila y verificar que queda vacía
    print("\n>>> Limpiando historial de la pila con clear_history()...")
    print(f"  Antes: {len(action_stack)} acciones")
    action_stack.clear_history()
    print(f"  Después: {len(action_stack)} acciones")
    print(f"  ¿Vacía?: {action_stack.is_empty()}")

    # Limpiar la cola y verificar que queda vacía
    print("\n>>> Limpiando cola con clear_queue()...")
    print(f"  Antes: {len(case_queue)} casos")
    case_queue.clear_queue()
    print(f"  Después: {len(case_queue)} casos")
    print(f"  ¿Vacía?: {case_queue.is_empty()}")

    print("\n" + "=" * 80)
    print("  Demostración completada exitosamente.")
    print("  Módulo listo para ser importado por el sistema principal.")
    print("=" * 80)
