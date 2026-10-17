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
    voz = GestorVoz()

    mostrar_bienvenida()

    modo_actual = None
    while modo_actual not in ["v", "t"]:
        modo_actual = input("\n[INICIO] ¿El modo activo será por [v]oz o [t]exto?: ").strip().lower()

    try:
        while True:
            if modo_actual == "v":
                entrada = voz.escuchar(duracion=6)
            else:
                entrada = leer_comando()

            if not entrada:
                if modo_actual == "t":
                    responder("No capturé nada. Inténtalo de nuevo.")
                continue

            if motor.normalizar(entrada) in {"salir", "cerrar", "terminar", "s"}:
                mensaje = "Hasta luego."
                responder(mensaje)
                voz.hablar(mensaje)
                break

            resultado = motor.evaluar(entrada)

            if resultado is None:
                mensaje_error = "No entendí la solicitud. Prueba pedirme 'ayuda'."
                responder(mensaje_error)
                voz.hablar(mensaje_error)
                continue

            regla = resultado["regla"]
            accion_nombre = regla["accion"]

            # INTERCEPTAR CAMBIOS DE MODO DINÁMICOS
            if accion_nombre == "modo_texto":
                modo_actual = "t"
                msj = regla.get("respuesta", "Cambiando a texto.")
                responder(msj)
                voz.hablar(msj)
                continue
            
            elif accion_nombre == "modo_voz":
                modo_actual = "v"
                msj = regla.get("respuesta", "Cambiando a voz.")
                responder(msj)
                voz.hablar(msj)
                continue

            # CONFIGURAR RESPUESTA PREDETERMINADA
            respuesta_consola = regla.get("respuesta", f"Ejecutando {regla['nombre']}.")
            respuesta_voz = respuesta_consola

            # PROCESAR ACCIONES DINÁMICAS (esperan recibir una Tupla: Consola, Voz)
            if accion_nombre in ["hora", "fecha", "noticias", "ayuda", "buscar", "abrir_noticia"]:
                resultado_ejecucion = ejecutar(accion_nombre, resultado, motor.conocimiento, reproductor)
                if isinstance(resultado_ejecucion, tuple):
                    respuesta_consola, respuesta_voz = resultado_ejecucion
                else:
                    respuesta_consola = respuesta_voz = resultado_ejecucion
            
            elif accion_nombre == "youtube":
                respuesta_consola = respuesta_voz = "Abriendo YouTube con tu perfil de Brave."
            elif accion_nombre == "reproducir_playlist":
                grupos = resultado.get("grupos", ())
                nombre_pl = grupos[0].strip() if grupos and grupos[0] else "tu playlist"
                respuesta_consola = respuesta_voz = f"Preparando la playlist {nombre_pl}."
            elif accion_nombre == "pausar_reproduccion":
                respuesta_consola = respuesta_voz = "Pausando la reproducción."
            elif accion_nombre == "reanudar_reproduccion":
                respuesta_consola = respuesta_voz = "Reanudando la reproducción."

            # NIVY RESPONDE (Muestra texto con URLs, pero habla texto limpio)
            responder(respuesta_consola)
            voz.hablar(respuesta_voz)

            # EJECUCIÓN PESADA DEL NAVEGADOR
            if accion_nombre in [
                "reproducir_playlist", "siguiente_cancion", "cancion_anterior", 
                "estado_reproduccion", "pausar_reproduccion", "reanudar_reproduccion"
            ]:
                resultado_accion = ejecutar(accion_nombre, resultado, motor.conocimiento, reproductor)
                # Si la acción devuelve respuesta de confirmación de tuplas, ignorar
                if not isinstance(resultado_accion, tuple) and accion_nombre not in ["estado_reproduccion"]:
                    print(f"NIVY > {resultado_accion}")

            print(f"[EXPLICACIÓN] {generar_explicacion(resultado)}")

    finally:
        reproductor.cerrar()

if __name__ == "__main__":
    main()