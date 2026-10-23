import unittest
from motor import MotorExperto

class TestSistemaExpertoNIVY(unittest.TestCase):

    def setUp(self):
        self.motor = MotorExperto()

    def test_computadora_lenta(self):
        # 1. El hecho es la entrada de texto del usuario
        entrada_usuario = "Nivy, mi computadora esta lenta"
        
        # 2. El motor evalúa la frase
        resultado = self.motor.evaluar(entrada_usuario)
        self.assertIsNotNone(resultado, "No se reconoció la frase.")
        
        # 3. Verificamos que el diagnóstico sea el correcto
        respuesta_esperada = "El diagnóstico indica una posible falta de memoria RAM."
        respuesta_obtenida = resultado["regla"]["respuesta"]
        
        self.assertIn("falta de memoria RAM", respuesta_obtenida)
        self.assertEqual(resultado["regla"]["accion"], "diagnosticar_ram")

if __name__ == "__main__":
    unittest.main()