import json
import os
from typing import List, Optional, Iterator, Set
from .models import Evidence, CrimeEvent, EvidenceType
from .nodes import EslabonEvidencia, HitoCronologico
from .exceptions import EvidenceNotFoundError, EventNotFoundError, EmptyListError


class RegistroForense:
    """
    Sistema de gestión de evidencias (Registro Secuencial).
    Optimizado para auditoría y persistencia de la cadena de custodia.
    """
    def __init__(self):
        """
        Inicializa un registro forense vacío.
        """
        self.__primer_eslabon: Optional[EslabonEvidencia] = None
        self.__conteo_evidencias: int = 0

    def esta_vacio(self) -> bool:
        """Determina si el registro carece de evidencias."""
        return self.__primer_eslabon is None

    def registrar_evidencia(self, evidencia: Evidence) -> None:
        """
        Anexa una nueva evidencia al final del registro oficial.

        :param evidencia: Objeto Evidence validado.
        """
        if not isinstance(evidencia, Evidence):
            raise TypeError("Error de integridad: Se requiere un objeto Evidence.")

        nuevo_eslabon = EslabonEvidencia(evidencia)
        if self.esta_vacio():
            self.__primer_eslabon = nuevo_eslabon
        else:
            actual = self.__primer_eslabon
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_eslabon
        self.__conteo_evidencias += 1

    def priorizar_evidencia(self, evidencia: Evidence) -> None:
        """
        Inserta una evidencia crítica al inicio del registro para atención inmediata.

        :param evidencia: Objeto Evidence validado.
        """
        if not isinstance(evidencia, Evidence):
            raise TypeError("Error de integridad: Se requiere un objeto Evidence.")

        nuevo_eslabon = EslabonEvidencia(evidencia)
        nuevo_eslabon.siguiente = self.__primer_eslabon
        self.__primer_eslabon = nuevo_eslabon
        self.__conteo_evidencias += 1

    def anular_registro_evidencia(self, id_evidencia: str) -> None:
        """
        Elimina una evidencia del registro oficial por su identificador único.

        :param id_evidencia: ID alfanumérico.
        :raises EvidenceNotFoundError: Si el ID no existe.
        """
        if self.esta_vacio():
            raise EvidenceNotFoundError("Operación fallida: El registro está vacío.")

        if self.__primer_eslabon.datos.evidence_id == id_evidencia:
            self.__primer_eslabon = self.__primer_eslabon.siguiente
            self.__conteo_evidencias -= 1
            return

        actual = self.__primer_eslabon
        while actual.siguiente is not None:
            if actual.siguiente.datos.evidence_id == id_evidencia:
                actual.siguiente = actual.siguiente.siguiente
                self.__conteo_evidencias -= 1
                return
            actual = actual.siguiente

        raise EvidenceNotFoundError(f"Violación de integridad: ID {id_evidencia} no hallado.")

    def consultar_evidencia(self, id_evidencia: str) -> Evidence:
        """Busca una evidencia específica en el archivo oficial."""
        for evidencia in self:
            if evidencia.evidence_id == id_evidencia:
                return evidencia
        raise EvidenceNotFoundError(f"ID {id_evidencia} no registrado en el sistema.")

    def filtrar_por_agente(self, nombre_agente: str) -> List[Evidence]:
        """
        Filtra evidencias por el agente responsable de la recolección.
        """
        return [ev for ev in self if ev.collected_by.lower() == nombre_agente.lower()]

    def obtener_todas_las_evidencias(self) -> List[Evidence]:
        """Retorna el inventario completo de evidencias."""
        return list(self)

    def filtrar_por_tipo(self, tipo: EvidenceType) -> List[Evidence]:
        """Retorna evidencias filtradas por su categoría forense."""
        return [ev for ev in self if ev.evidence_type == tipo]

    def save_to_json(self, filename: str) -> None:
        """Persiste el registro forense en un archivo JSON."""
        data = [ev.to_dictionary() for ev in self]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_from_json(self, filename: str) -> None:
        """Carga datos históricos al registro forense."""
        if not os.path.exists(filename):
            return
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                self.registrar_evidencia(Evidence.from_dictionary(item))

    def __len__(self) -> int:
        return self.__conteo_evidencias

    def __iter__(self) -> Iterator[Evidence]:
        """Habilita el recorrido oficial del registro."""
        actual = self.__primer_eslabon
        while actual is not None:
            yield actual.datos
            actual = actual.siguiente

    def __str__(self) -> str:
        if self.esta_vacio():
            return "Estado: Registro forense vacío."
        return f"Inventario Forense: {self.__conteo_evidencias} piezas bajo custodia."


class CronologiaCriminal:
    """
    Motor cronológico para la reconstrucción de hechos (Línea de Tiempo).
    Permite navegar por la secuencia de sucesos criminales.
    """
    def __init__(self):
        self.__suceso_inicial: Optional[HitoCronologico] = None
        self.__suceso_final: Optional[HitoCronologico] = None
        self.__foco_investigacion: Optional[HitoCronologico] = None
        self.__total_sucesos: int = 0

    def esta_vacia(self) -> bool:
        return self.__suceso_inicial is None

    def registrar_suceso(self, suceso: CrimeEvent) -> None:
        """Añade un hito a la línea de tiempo (orden cronológico de registro)."""
        if not isinstance(suceso, CrimeEvent):
            raise TypeError("Error: Objeto CrimeEvent inválido.")

        nuevo_hito = HitoCronologico(suceso)
        if self.esta_vacia():
            self.__suceso_inicial = self.__suceso_final = self.__foco_investigacion = nuevo_hito
        else:
            nuevo_hito.anterior = self.__suceso_final
            self.__suceso_final.posterior = nuevo_hito
            self.__suceso_final = nuevo_hito
        self.__total_sucesos += 1

    def insertar_suceso_fundacional(self, suceso: CrimeEvent) -> None:
        """Establece un nuevo punto de origen en la cronología."""
        if not isinstance(suceso, CrimeEvent):
            raise TypeError("Error: Objeto CrimeEvent inválido.")

        nuevo_hito = HitoCronologico(suceso)
        if self.esta_vacia():
            self.__suceso_inicial = self.__suceso_final = self.__foco_investigacion = nuevo_hito
        else:
            nuevo_hito.posterior = self.__suceso_inicial
            self.__suceso_inicial.anterior = nuevo_hito
            self.__suceso_inicial = nuevo_hito
        self.__total_sucesos += 1

    def eliminar_suceso(self, id_suceso: str) -> None:
        """Elimina un hito de la línea de tiempo."""
        actual = self.__suceso_inicial
        while actual is not None:
            if actual.suceso.event_id == id_suceso:
                if self.__total_sucesos == 1:
                    self.__suceso_inicial = self.__suceso_final = self.__foco_investigacion = None
                elif actual == self.__suceso_inicial:
                    self.__suceso_inicial = actual.posterior
                    self.__suceso_inicial.anterior = None
                    if self.__foco_investigacion == actual:
                        self.__foco_investigacion = self.__suceso_inicial
                elif actual == self.__suceso_final:
                    self.__suceso_final = actual.anterior
                    self.__suceso_final.posterior = None
                    if self.__foco_investigacion == actual:
                        self.__foco_investigacion = self.__suceso_final
                else:
                    actual.anterior.posterior = actual.posterior
                    actual.posterior.anterior = actual.anterior
                    if self.__foco_investigacion == actual:
                        self.__foco_investigacion = actual.posterior
                self.__total_sucesos -= 1
                return
            actual = actual.posterior
        raise EventNotFoundError(f"Hito temporal {id_suceso} no localizado.")

    def obtener_sospechosos_consolidados(self) -> Set[str]:
        """Extrae la lista única de sospechosos de toda la cronología."""
        sospechosos: Set[str] = set()
        for evento in self:
            for sospechoso in evento.involved_suspects:
                sospechosos.add(sospechoso)
        return sospechosos

    def filtrar_por_ubicacion(self, ubicacion: str) -> List[CrimeEvent]:
        """Localiza sucesos ocurridos en una zona geográfica."""
        return [e for e in self if ubicacion.lower() in e.event_location.lower()]

    def avanzar_en_linea_de_tiempo(self) -> Optional[CrimeEvent]:
        """Mueve el foco de la investigación hacia el futuro."""
        if self.esta_vacia(): raise EmptyListError("No hay sucesos registrados.")
        if self.__foco_investigacion.posterior:
            self.__foco_investigacion = self.__foco_investigacion.posterior
            return self.__foco_investigacion.suceso
        return None

    def retroceder_en_linea_de_tiempo(self) -> Optional[CrimeEvent]:
        """Mueve el foco de la investigación hacia el pasado."""
        if self.esta_vacia(): raise EmptyListError("No hay sucesos registrados.")
        if self.__foco_investigacion.anterior:
            self.__foco_investigacion = self.__foco_investigacion.anterior
            return self.__foco_investigacion.suceso
        return None

    def obtener_suceso_actual(self) -> CrimeEvent:
        if self.esta_vacia(): raise EmptyListError("Sin hitos cronológicos.")
        return self.__foco_investigacion.suceso

    def ir_al_origen(self) -> CrimeEvent:
        if self.esta_vacia(): raise EmptyListError("Línea de tiempo vacía.")
        self.__foco_investigacion = self.__suceso_inicial
        return self.__foco_investigacion.suceso

    def ir_al_final(self) -> CrimeEvent:
        if self.esta_vacia(): raise EmptyListError("Línea de tiempo vacía.")
        self.__foco_investigacion = self.__suceso_final
        return self.__foco_investigacion.suceso

    def save_to_json(self, filename: str) -> None:
        """Persiste la cronología en un archivo JSON."""
        data = [suceso.to_dictionary() for suceso in self]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_from_json(self, filename: str) -> None:
        """Carga datos históricos a la línea de tiempo."""
        if not os.path.exists(filename):
            return
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                self.registrar_suceso(CrimeEvent.from_dictionary(item))

    def __iter__(self) -> Iterator[CrimeEvent]:
        """Habilita el análisis secuencial de los hechos."""
        actual = self.__suceso_inicial
        while actual:
            yield actual.suceso
            actual = actual.posterior

    def __len__(self) -> int:
        return self.__total_sucesos

    def __str__(self) -> str:
        if self.esta_vacia(): return "Estado: Cronología sin sucesos."
        return (f"Línea de Tiempo: {self.__total_sucesos} hitos. "
                f"Punto de origen: '{self.__suceso_inicial.suceso.event_title}'.")
