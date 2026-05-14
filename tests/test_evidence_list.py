import unittest
import os
import sys

# Añadir el directorio padre al path para importar el paquete principal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FinalCriminalSystem.models import Evidence, EvidenceType
from FinalCriminalSystem.linked_lists import RegistroForense
from FinalCriminalSystem.exceptions import EvidenceNotFoundError

class TestRegistroForense(unittest.TestCase):
    def setUp(self):
        self.registro = RegistroForense()
        self.ev1 = Evidence("E1", EvidenceType.WEAPON, "Pistola", "2024-01-01", "Smith")
        self.ev2 = Evidence("E2", EvidenceType.DNA_SAMPLE, "Sangre", "2024-01-02", "Miller")

    def test_registro_y_conteo(self):
        self.registro.registrar_evidencia(self.ev1)
        self.registro.registrar_evidencia(self.ev2)
        self.assertEqual(len(self.registro), 2)

    def test_consulta_por_id(self):
        self.registro.registrar_evidencia(self.ev1)
        encontrada = self.registro.consultar_evidencia("E1")
        self.assertEqual(encontrada.description, "Pistola")
        
        with self.assertRaises(EvidenceNotFoundError):
            self.registro.consultar_evidencia("INEXISTENTE")

    def test_anulacion_registro(self):
        self.registro.registrar_evidencia(self.ev1)
        self.registro.registrar_evidencia(self.ev2)
        self.registro.anular_registro_evidencia("E1")
        self.assertEqual(len(self.registro), 1)
        self.assertEqual(self.registro.obtener_todas_las_evidencias()[0].evidence_id, "E2")

    def test_persistencia_json(self):
        filename = "test_evidencias_refactor.json"
        self.registro.registrar_evidencia(self.ev1)
        self.registro.save_to_json(filename)
        
        nuevo_registro = RegistroForense()
        nuevo_registro.load_from_json(filename)
        self.assertEqual(len(nuevo_registro), 1)
        self.assertEqual(nuevo_registro.obtener_todas_las_evidencias()[0].evidence_id, "E1")
        
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
