from acciones import ejecutar
from explicacion import generar_explicacion
from interfaz import mostrar_bienvenida, leer_comando, responder
from motor import MotorExperto


def main():
    motor = MotorExperto()
    mostrar_bienvenida()

    while True:
        entrada = leer_comando()

        if not entrada:
            responder("Escribe una instrucción.")
            continue

        if motor.normalizar(entrada) in {"salir", "cerrar", "terminar"}:
            responder("Hasta luego.")
            break

        resultado = motor.evaluar(entrada)

        if resultado is None:
            responder(
                "No entendí la solicitud. Prueba con 'ayuda' para ver "
                "los comandos disponibles."
            )
            continue

        regla = resultado["regla"]
        respuesta = ejecutar(
            regla["accion"],
            resultado,
            motor.conocimiento
        )

        responder(respuesta)

        # Modo de trazabilidad del sistema experto.
        print(f"[EXPLICACIÓN] {generar_explicacion(resultado)}")


if __name__ == "__main__":
    main()
