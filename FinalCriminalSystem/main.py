import os
import sys

# Asegurar que el paquete sea importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FinalCriminalSystem.models import Evidence, CrimeEvent, EvidenceType
from FinalCriminalSystem.linked_lists import RegistroForense, CronologiaCriminal
from FinalCriminalSystem.exceptions import EvidenceNotFoundError, EventNotFoundError, EmptyListError

DATA_DIR = "data"
EVIDENCES_FILE = os.path.join(DATA_DIR, "evidences.json")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    print("\n" + "="*50)
    print("      SISTEMA DE INVESTIGACIÓN CRIMINAL v2.0")
    print("="*50)
    print("1. Gestionar Registro Forense (Evidencias)")
    print("2. Gestionar Cronología Criminal (Sucesos)")
    print("3. Guardar y Salir")
    print("="*50)
    return input("Seleccione una opción: ")

def gestionar_evidencias(registro: RegistroForense):
    while True:
        clear_screen()
        print("\n--- REGISTRO FORENSE ---")
        print(f"Estado actual: {registro}")
        print("1. Registrar Nueva Evidencia")
        print("2. Registrar Evidencia Crítica (Prioritaria)")
        print("3. Consultar por ID")
        print("4. Filtrar por Agente")
        print("5. Anular Registro de Evidencia")
        print("6. Listar Inventario Completo")
        print("7. Volver al Menú Principal")
        
        op = input("\nSeleccione: ")
        
        if op == "1" or op == "2":
            try:
                eid = input("ID: ")
                print("Tipos: " + ", ".join([t.name for t in EvidenceType]))
                tipo_str = input("Tipo: ").upper()
                tipo = EvidenceType[tipo_str]
                desc = input("Descripción: ")
                fecha = input("Fecha (YYYY-MM-DD): ")
                agente = input("Agente: ")
                nueva_ev = Evidence(eid, tipo, desc, fecha, agente)
                if op == "1":
                    registro.registrar_evidencia(nueva_ev)
                else:
                    registro.priorizar_evidencia(nueva_ev)
                print("\n[✔] Evidencia registrada en el sistema.")
            except (KeyError, ValueError) as e:
                print(f"\n[✘] Error en datos ingresados: {e}")
            input("\nPresione Enter para continuar...")
            
        elif op == "3":
            eid = input("ID a consultar: ")
            try:
                ev = registro.consultar_evidencia(eid)
                print(f"\n[i] Datos de la Evidencia: {ev}")
            except EvidenceNotFoundError as e:
                print(f"\n[!] {e}")
            input("\nPresione Enter para continuar...")
            
        elif op == "4":
            agente = input("Nombre del agente: ")
            res = registro.filtrar_por_agente(agente)
            if res:
                print(f"\nEvidencias recolectadas por {agente}:")
                for e in res: print(f"  - {e}")
            else:
                print("\n[!] No se hallaron registros para este agente.")
            input("\nPresione Enter para continuar...")
            
        elif op == "5":
            eid = input("ID de evidencia a anular: ")
            try:
                registro.anular_registro_evidencia(eid)
                print("\n[✔] Registro de evidencia anulado.")
            except EvidenceNotFoundError as e:
                print(f"\n[!] {e}")
            input("\nPresione Enter para continuar...")
            
        elif op == "6":
            print("\nINVENTARIO FORENSE COMPLETO:")
            for e in registro: print(f"  • {e}")
            input("\nPresione Enter para continuar...")
            
        elif op == "7":
            break

def gestionar_cronologia(cronologia: CronologiaCriminal):
    while True:
        clear_screen()
        print("\n--- CRONOLOGÍA CRIMINAL ---")
        try:
            actual = cronologia.obtener_suceso_actual()
            print(f"Suceso bajo análisis: {actual}")
        except EmptyListError:
            print("Estado: Línea de tiempo vacía.")
            
        print("\n1. Registrar Suceso (Nuevo Hito)")
        print("2. Insertar Suceso Fundacional (Origen)")
        print("3. Avanzar en Línea de Tiempo (Futuro)")
        print("4. Retroceder en Línea de Tiempo (Pasado)")
        print("5. Localizar por Ubicación")
        print("6. Ver Sospechosos Consolidados")
        print("7. Listado Cronológico Completo")
        print("8. Volver al Menú Principal")
        
        op = input("\nSeleccione: ")
        
        if op == "1" or op == "2":
            vid = input("ID Suceso: ")
            titulo = input("Título: ")
            desc = input("Descripción: ")
            hora = input("Fecha/Hora: ")
            loc = input("Ubicación: ")
            sos = input("Sospechosos (separados por coma): ").split(",")
            sos = [s.strip() for s in sos]
            nuevo_suceso = CrimeEvent(vid, titulo, desc, hora, loc, sos)
            if op == "1":
                cronologia.registrar_suceso(nuevo_suceso)
            else:
                cronologia.insertar_suceso_fundacional(nuevo_suceso)
            print("\n[✔] Hito cronológico registrado.")
            input("\nPresione Enter para continuar...")
            
        elif op == "3":
            res = cronologia.avanzar_en_linea_de_tiempo()
            if not res: print("\n[!] Límite superior de la cronología alcanzado.")
            input("\nPresione Enter para continuar...")
            
        elif op == "4":
            res = cronologia.retroceder_en_linea_de_tiempo()
            if not res: print("\n[!] Se ha llegado al origen de los hechos.")
            input("\nPresione Enter para continuar...")
            
        elif op == "5":
            loc = input("Ubicación a rastrear: ")
            res = cronologia.filtrar_por_ubicacion(loc)
            if res:
                for e in res: print(f"  - {e}")
            else:
                print("\n[!] No hay sucesos registrados en esa ubicación.")
            input("\nPresione Enter para continuar...")
            
        elif op == "6":
            sos = cronologia.obtener_sospechosos_consolidados()
            print(f"\nLista de Sospechosos Únicos: {', '.join(sos) if sos else 'Ninguno'}")
            input("\nPresione Enter para continuar...")
            
        elif op == "7":
            print("\nRECONSTRUCCIÓN DE HECHOS (ORDEN CRONOLÓGICO):")
            for e in cronologia: print(f"  >> {e}")
            input("\nPresione Enter para continuar...")
            
        elif op == "8":
            break

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    registro = RegistroForense()
    cronologia = CronologiaCriminal()
    
    # Cargar historial
    registro.load_from_json(EVIDENCES_FILE)
    cronologia.load_from_json(EVENTS_FILE)
    
    while True:
        clear_screen()
        op = menu_principal()
        
        if op == "1":
            gestionar_evidencias(registro)
        elif op == "2":
            gestionar_cronologia(cronologia)
        elif op == "3":
            print("\nSincronizando archivos de investigación...")
            registro.save_to_json(EVIDENCES_FILE)
            cronologia.save_to_json(EVENTS_FILE)
            print("Cierre de sesión exitoso.")
            break

if __name__ == "__main__":
    main()
