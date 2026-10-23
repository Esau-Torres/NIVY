import unittest
import sys
import os

# Asegura que el script de pruebas pueda encontrar el módulo 'motor' en el directorio principal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor import MotorExperto

class TestSistemaExpertoNIVY(unittest.TestCase):

    def setUp(self):
        # setUp se ejecuta antes de cada test.
        # Instanciamos el motor para tenerlo listo para todas las pruebas.
        self.motor = MotorExperto()

    def test_consulta_hora(self):
        """Verifica que el sistema entienda cuando se le pregunta la hora"""
        entrada_usuario = "¿Qué hora es?"
        
        # El motor evalúa la frase
        resultado = self.motor.evaluar(entrada_usuario)
        
        # Verificamos que encontró una regla (no es None)
        self.assertIsNotNone(resultado, "El motor no reconoció la frase para consultar la hora.")
        
        # Verificamos que la regla activada sea la de la hora (R001) y ejecute 'hora'
        regla = resultado["regla"]
        self.assertEqual(regla["accion"], "hora")
        self.assertEqual(regla["id"], "R001")

    def test_reproduccion_musica_y_extraccion(self):
        """Verifica que active la música y extraiga el nombre de la playlist"""
        # Se ajusta la frase para que la captura exacta coincida con la aserción 'metal'
        entrada_usuario = "Nivy, reproduce metal"
        
        resultado = self.motor.evaluar(entrada_usuario)
        self.assertIsNotNone(resultado)
        
        regla = resultado["regla"]
        
        # Debe activar la regla R008 (Seleccionar playlist dinámica)
        self.assertEqual(regla["accion"], "reproducir_playlist")
        self.assertEqual(regla["id"], "R008")
        
        # Verificamos que extrajo correctamente la palabra "metal" de la expresión regular
        grupos = resultado["grupos"]
        self.assertTrue(len(grupos) > 0)
        self.assertEqual(grupos[0].strip().lower(), "metal")

    def test_envio_whatsapp_complejo(self):
        """Verifica la extracción de múltiples datos (contacto y mensaje) para WhatsApp"""
        # Se ajusta la frase para que coincida exactamente con el patrón "\bmandale un mensaje a (.+) que diga (.+)"
        entrada_usuario = "mandale un mensaje a Carlos que diga hola como estas"
        
        resultado = self.motor.evaluar(entrada_usuario)
        self.assertIsNotNone(resultado)
        
        regla = resultado["regla"]
        self.assertEqual(regla["accion"], "enviar_whatsapp")
        self.assertEqual(regla["id"], "R018")
        
        # Verifica que Regex separó correctamente el remitente y el mensaje
        grupos = resultado["grupos"]
        self.assertEqual(len(grupos), 2, "La regla de WhatsApp debe extraer exactamente 2 grupos.")
        self.assertEqual(grupos[0].strip().lower(), "carlos")
        self.assertEqual(grupos[1].strip().lower(), "hola como estas")

    def test_comando_desconocido(self):
        """Verifica el comportamiento cuando se ingresa algo sin sentido"""
        entrada_usuario = "quiero que cocines una pizza"
        
        resultado = self.motor.evaluar(entrada_usuario)
        
        # Como no hay reglas para cocinar, el resultado debe ser None
        self.assertIsNone(resultado)

    def test_normalizacion_texto(self):
        """Verifica que el motor quite acentos y pase a minúsculas antes de evaluar"""
        entrada = "¿QUÉ HÓRÁ ÈS?"
        
        # Usamos el método estático de normalización
        texto_limpio = self.motor.normalizar(entrada)
        
        # Debería ignorar la puntuación inicial/final (en tu código quitas acentos y mayúsculas)
        self.assertTrue("que hora es" in texto_limpio)

if __name__ == "__main__":
    unittest.main()