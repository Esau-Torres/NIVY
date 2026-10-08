from acciones import ejecutar
from explicacion import generar_explicacion
from interfaz import (
    mostrar_bienvenida,
    leer_comando,
    responder
)
from motor import MotorExperto
from reproductor import Reproductor
from voz import GestorVoz


def main():
    motor = MotorExperto()
    reproductor = Reproductor(motor.conocimiento)
    
    # Inicializar el gestor de voz
    voz = GestorVoz()

    mostrar_bienvenida()

    try:
        while True:
            # Seleccionar método de entrada de forma automática o manual
            tipo_entrada = input("\n¿Entrada por [v]oz o [t]exto? (o 'salir'): ").strip().lower()
            
            if tipo_entrada in {"salir", "cerrar", "terminar", "s"}:
                mensaje = "Hasta luego."
                responder(mensaje)
                voz.hablar(mensaje)
                break

            if tipo_entrada == "v":
                entrada = voz.escuchar(duracion=6) # 6 segundos para hablar cómodamente
            else:
                entrada = leer_comando()

            if not entrada:
                responder("No capturé ninguna voz o texto. Inténtalo de nuevo.")
                continue

            if motor.normalizar(entrada) in {"salir", "cerrar", "terminar"}:
                mensaje = "Hasta luego."
                responder(mensaje)
                voz.hablar(mensaje)
                break

            resultado = motor.evaluar(entrada)

            if resultado is None:
                mensaje_error = "No entendí la solicitud. Prueba con 'ayuda'."
                responder(mensaje_error)
                voz.hablar(mensaje_error)
                continue

            regla = resultado["regla"]
            accion_nombre = regla["accion"]

            # ---------------------------------------------------------
            # ORDEN: PRIMERO HABLAR / DESCRIBIR, LUEGO EJECUTAR ACCIÓN
            # ---------------------------------------------------------
            
            # 1. Definir el mensaje de respuesta basado en la regla
            respuesta_texto = regla.get("respuesta", f"Ejecutando {regla['nombre']}.")
            
            # Si la regla requiere datos dinámicos (como hora o fecha), los calculamos antes
            if accion_nombre in ["hora", "fecha", "noticias", "ayuda"]:
                respuesta_texto = ejecutar(accion_nombre, resultado, motor.conocimiento, reproductor)
            elif accion_nombre == "youtube":
                respuesta_texto = "Abriendo YouTube con tu perfil de Brave."
            elif accion_nombre == "reproducir_playlist":
                grupos = resultado.get("grupos", ())
                nombre_pl = grupos[0].strip() if grupos and grupos[0] else "tu playlist"
                respuesta_texto = f"Preparando la playlist {nombre_pl}."

            # 2. NIVY habla y muestra el texto PRIMERO
            responder(respuesta_texto)
            voz.hablar(respuesta_texto)

            # 3. LUEGO se ejecuta la acción pesada (Selenium / Navegador / Reproductor)
            if accion_nombre in ["reproducir_playlist", "siguiente_cancion", "cancion_anterior", "estado_reproduccion", "youtube", "buscar"]:
                resultado_accion = ejecutar(accion_nombre, resultado, motor.conocimiento, reproductor)
                if accion_nombre in ["reproducir_playlist", "siguiente_cancion", "cancion_anterior"]:
                    print(f"NIVY > {resultado_accion}")

            print(
                f"[EXPLICACIÓN] "
                f"{generar_explicacion(resultado)}"
            )

    finally:
        reproductor.cerrar()


if __name__ == "__main__":
    main()