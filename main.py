from acciones import ejecutar
from explicacion import generar_explicacion
from interfaz import (
    mostrar_bienvenida,
    leer_comando,
    responder
)
from motor import MotorExperto
from reproductor import Reproductor


def main():

    motor = MotorExperto()

    reproductor = Reproductor(
        motor.conocimiento
    )

    mostrar_bienvenida()

    try:

        while True:

            entrada = leer_comando()

            if not entrada:

                responder(
                    "Escribe una instrucción."
                )

                continue

            if motor.normalizar(
                entrada
            ) in {
                "salir",
                "cerrar",
                "terminar"
            }:

                responder(
                    "Hasta luego."
                )

                break

            resultado = motor.evaluar(
                entrada
            )

            if resultado is None:

                responder(
                    "No entendí la solicitud. "
                    "Prueba con 'ayuda' para ver "
                    "los comandos disponibles."
                )

                continue

            regla = resultado["regla"]

            respuesta = ejecutar(
                regla["accion"],
                resultado,
                motor.conocimiento,
                reproductor
            )

            responder(
                respuesta
            )

            print(
                f"[EXPLICACIÓN] "
                f"{generar_explicacion(resultado)}"
            )

    finally:

        reproductor.cerrar()


if __name__ == "__main__":
    main()