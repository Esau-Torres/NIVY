import json
import re
import unicodedata
from pathlib import Path


class MotorExperto:
    def __init__(self, archivo_reglas="conocimiento/reglas.json"):
        self.archivo_reglas = Path(archivo_reglas)
        self.conocimiento = self._cargar_conocimiento()
        self.reglas = sorted(
            self.conocimiento["reglas"],
            key=lambda regla: regla.get("prioridad", 0),
            reverse=True,
        )

    @staticmethod
    def normalizar(texto: str) -> str:
        texto = texto.strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            caracter for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )
        return texto

    def _cargar_conocimiento(self):
        with self.archivo_reglas.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def evaluar(self, entrada: str):
        texto = self.normalizar(entrada)

        for regla in self.reglas:
            for patron in regla.get("patrones", []):
                coincidencia = re.search(patron, texto, flags=re.IGNORECASE)
                if coincidencia:
                    return {
                        "regla": regla,
                        "entrada_original": entrada,
                        "texto_normalizado": texto,
                        "grupos": coincidencia.groups(),
                    }

        return None

    def explicar(self, resultado):
        if resultado is None:
            return "No se encontró ninguna regla compatible con la solicitud."
        regla = resultado["regla"]
        return (
            f"Regla aplicada: {regla['id']} - {regla['nombre']} | "
            f"Acción: {regla['accion']}"
        )
