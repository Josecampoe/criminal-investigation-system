import unittest
import os
import sys

# Añadir el directorio padre al path para importar el paquete principal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FinalCriminalSystem.models import CrimeEvent
from FinalCriminalSystem.linked_lists import CronologiaCriminal
from FinalCriminalSystem.exceptions import EmptyListError

class TestCronologiaCriminal(unittest.TestCase):
    def setUp(self):
        self.cronologia = CronologiaCriminal()
        self.suceso1 = CrimeEvent("V1", "Robo", "Banco", "10:00", "Centro", ["John"])
        self.suceso2 = CrimeEvent("V2", "Huida", "Escape", "10:30", "Norte", ["John"])

    def test_registro_y_navegacion(self):
        self.cronologia.registrar_suceso(self.suceso1)
        self.cronologia.registrar_suceso(self.suceso2)
        self.assertEqual(self.cronologia.obtener_suceso_actual().event_id, "V1")
        
        proximo = self.cronologia.avanzar_en_linea_de_tiempo()
        self.assertEqual(proximo.event_id, "V2")
        self.assertEqual(self.cronologia.obtener_suceso_actual().event_id, "V2")
        
        anterior = self.cronologia.retroceder_en_linea_de_tiempo()
        self.assertEqual(anterior.event_id, "V1")

    def test_sospechosos_consolidados(self):
        self.cronologia.registrar_suceso(self.suceso1)
        self.cronologia.registrar_suceso(self.suceso2)
        self.cronologia.registrar_suceso(CrimeEvent("V3", "Ocultamiento", "Cueva", "12:00", "Bosque", ["Jane", "John"]))
        
        sospechosos = self.cronologia.obtener_sospechosos_consolidados()
        self.assertEqual(len(sospechosos), 2)
        self.assertIn("John", sospechosos)
        self.assertIn("Jane", sospechosos)

    def test_persistencia_json(self):
        filename = "test_cronologia_refactor.json"
        self.cronologia.registrar_suceso(self.suceso1)
        self.cronologia.save_to_json(filename)
        
        nueva_cronologia = CronologiaCriminal()
        nueva_cronologia.load_from_json(filename)
        self.assertEqual(len(nueva_cronologia), 1)
        self.assertEqual(nueva_cronologia.obtener_suceso_actual().event_id, "V1")
        
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
