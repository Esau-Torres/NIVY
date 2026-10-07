import unittest
from motor import MotorExperto


class TestReglas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.motor = MotorExperto()

    def test_hora(self):
        resultado = self.motor.evaluar("¿Qué hora es?")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["regla"]["id"], "R001")

    def test_fecha(self):
        resultado = self.motor.evaluar("dime la fecha")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["regla"]["id"], "R002")

    def test_playlist(self):
        resultado = self.motor.evaluar("pon mi playlist")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["regla"]["id"], "R003")

    def test_busqueda(self):
        resultado = self.motor.evaluar("busca en internet Python")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["regla"]["id"], "R006")
        self.assertEqual(resultado["grupos"][0], "python")

    def test_desconocido(self):
        resultado = self.motor.evaluar("haz algo completamente diferente")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
