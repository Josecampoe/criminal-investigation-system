"""
CIMS - Reportes
reportes/generador.py — Generador de Informes ASCII

Genera reportes completos de la investigación
recorriendo las estructuras de datos (Lista Simple, Lista Doble).
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from modulos.gestor_evidencias  import GestorEvidencias
from modulos.gestor_timeline    import GestorTimeline
from modulos.gestores           import GestorCasos, GestorSospechosos
from modelos.enums              import EstadoSospechoso


REPORTES_DIR = Path(__file__).parent.parent / "reportes"
REPORTES_DIR.mkdir(exist_ok=True)


class GeneradorReportes:
    """Genera reportes completos recorriendo todas las estructuras."""

    def __init__(self,
                 ge: GestorEvidencias,
                 gt: GestorTimeline,
                 gc: GestorCasos,
                 gs: GestorSospechosos):
        self.ge = ge
        self.gt = gt
        self.gc = gc
        self.gs = gs

    def reporte_caso_completo(self, caso_id: str,
                               guardar: bool = True) -> str:
        """
        Genera el reporte completo del caso recorriendo:
          - Lista Simple: eslabones de custodia de cada evidencia
          - Lista Doble: eventos del timeline
          - Tabla Hash: datos del caso, sospechosos
        """
        caso = self.gc.obtener(caso_id)
        if not caso:
            return f"ERROR: Caso {caso_id} no encontrado"

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lineas = []
        W = 70

        def sep(c="═"): lineas.append(c * W)
        def titulo(t): lineas.append(f"  {t}")
        def vacio(): lineas.append("")
        def campo(k, v): lineas.append(f"  {k:<22}: {v}")

        # ─── Encabezado ─────────────────────────────────────────────
        sep()
        titulo("SISTEMA DE INVESTIGACIÓN CRIMINAL — CIMS v2.0")
        titulo("INFORME OFICIAL DE CASO")
        sep()
        campo("Generado el",      ts)
        campo("Caso No.",         caso.numero_caso)
        campo("Título",           caso.titulo)
        campo("Tipo",             caso.tipo.value)
        campo("Estado",           caso.estado.value)
        campo("Prioridad",        caso.prioridad.etiqueta())
        campo("Lugar del crimen", caso.lugar_crimen)
        campo("Fecha del crimen", caso.fecha_crimen[:16])
        campo("Fecha apertura",   caso.fecha_apertura[:16])
        campo("Investigador líder", caso.investigador_lider)
        vacio()
        titulo("DESCRIPCIÓN:")
        titulo(f"  {caso.descripcion}")
        sep("─")

        # ─── Víctimas ───────────────────────────────────────────────
        vacio()
        titulo(f"VÍCTIMAS ({len(caso.victimas)})")
        sep("─")
        if caso.victimas:
            for i, v in enumerate(caso.victimas, 1):
                titulo(f"  {i}. {v}")
        else:
            titulo("  Sin víctimas registradas")

        # ─── Sospechosos ────────────────────────────────────────────
        sospechosos = self.gs.listar(caso_id=caso_id)
        vacio()
        titulo(f"SOSPECHOSOS ({len(sospechosos)})")
        sep("─")
        for s in sospechosos:
            peligro = "⚠" * s.nivel_peligrosidad
            lineas.append(f"  [{s.id}] {s.nombre_completo}")
            lineas.append(f"       Estado: {s.estado.value}  |  "
                          f"Peligrosidad: {peligro}")
            if s.descripcion_fisica:
                lineas.append(f"       Física: {s.descripcion_fisica}")
            if s.antecedentes:
                lineas.append(f"       Antec.: {s.descripcion_antecedentes}")
            lineas.append(f"       Evidencias vinculadas: "
                          f"{len(s.evidencias_vinculadas)}")
            vacio()

        # ─── Evidencias + Cadena de Custodia (Lista Simple) ─────────
        evidencias = self.ge.listar(caso_id=caso_id)
        vacio()
        titulo(f"EVIDENCIAS ({len(evidencias)}) — Cadena de Custodia [Lista Simple]")
        sep("─")
        for ev in evidencias:
            cadena = self.ge.obtener_cadena(ev.id)
            integra = " ÍNTEGRA" if self.ge.verificar_integridad(ev.id) \
                      else " COMPROMETIDA"
            lineas.append(f"  [{ev.codigo}] {ev.descripcion}")
            lineas.append(f"    Tipo: {ev.tipo.value}  |  Estado: {ev.estado.value}"
                          f"  |  Cadena: {integra}")
            lineas.append(f"    Lugar hallazgo: {ev.lugar_hallazgo}")
            lineas.append(f"    Custodio actual: {ev.responsable_actual}"
                          f" @ {ev.ubicacion_actual}")
            if ev.resultado_analisis:
                lineas.append(f"    Análisis: {ev.resultado_analisis[:60]}")
            # Recorrer la Lista Simple de custodia
            if cadena and not cadena.esta_vacia():
                lineas.append(f"    Eslabones de custodia ({cadena.longitud()}):")
                for i, eslabon in enumerate(cadena):    # itera la Lista Simple
                    lineas.append(f"      [{i+1}] {eslabon.accion} — "
                                  f"{eslabon.responsable} @ "
                                  f"{eslabon.timestamp[:16]}")
            vacio()

        # ─── Timeline (Lista Doblemente Enlazada) ───────────────────
        eventos = self.gt.obtener_timeline(caso_id)
        vacio()
        titulo(f"LÍNEA DE TIEMPO ({len(eventos)} eventos) "
               f"— [Lista Doblemente Enlazada]")
        sep("─")
        titulo("  Recorrido ADELANTE (cronológico ▶):")
        for i, ev in enumerate(eventos):         # recorre Lista Doble adelante
            verificado = "✓" if ev.verificado else "?"
            lineas.append(f"  [{i+1:02d}][{verificado}] {ev}")
            if ev.lugar:
                lineas.append(f"         {ev.lugar}")

        vacio()
        titulo("  Recorrido ATRÁS (más reciente ◀):")
        for i, ev in enumerate(
                self.gt.obtener_timeline_inverso(caso_id)):   # Lista Doble inverso
            lineas.append(f"  [{i+1:02d}] {ev}")

        dur = self.gt.calcular_duracion(caso_id)
        if dur:
            vacio()
            campo("Inicio investigación", dur[0][:16])
            campo("Último evento",        dur[1][:16])
            campo("Duración total",       dur[2])

        # ─── Estadísticas ────────────────────────────────────────────
        vacio()
        titulo("ESTADÍSTICAS DE LA INVESTIGACIÓN")
        sep("─")
        stats_ev = self.ge.estadisticas()
        campo("Total evidencias",     stats_ev["total"])
        campo("Sospechosos",          len(sospechosos))
        campo("Eventos timeline",     len(eventos))
        campo("Tareas historial",     stats_ev["acciones_historial"])

        tipos_ev = stats_ev.get("por_tipo", {})
        if tipos_ev:
            titulo("  Evidencias por tipo:")
            for tipo, cnt in tipos_ev.items():
                lineas.append(f"    • {tipo}: {cnt}")

        tipos_tm = self.gt.resumen_tipos(caso_id)
        if tipos_tm:
            titulo("  Eventos por tipo:")
            for tipo, cnt in tipos_tm.items():
                lineas.append(f"    • {tipo}: {cnt}")

        # ─── Cierre ─────────────────────────────────────────────────
        vacio()
        sep()
        titulo("FIN DEL INFORME — CIMS v2.0")
        titulo(f"Generado: {ts}")
        sep()

        reporte = "\n".join(lineas)

        if guardar:
            nombre = f"reporte_{caso.numero_caso.replace('-', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta = REPORTES_DIR / nombre
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(reporte)
            print(f"\n   Reporte guardado: {ruta}")

        return reporte
