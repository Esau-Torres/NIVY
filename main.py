from acciones import ejecutar, obtener_saludo_inicial
from explicacion import generar_explicacion
from interfaz import (
    leer_comando,
    responder
)
from motor import MotorExperto
from reproductor import Reproductor
from voz import GestorVoz
from whatsapp import GestorWhatsApp

def main():
    motor = MotorExperto()
    reproductor = Reproductor(motor.conocimiento)
    voz = GestorVoz()
    whatsapp = GestorWhatsApp()

    # 1. Preguntar el método de ENTRADA (Micrófono o Teclado)
    modo_actual = None
    while modo_actual not in ["v", "t"]:
        modo_actual = input("\n[INICIO] ¿El método de entrada será por [v]oz o [t]exto?: ").strip().lower()

    # 2. Generar el saludo dinámico
    saludo_consola, saludo_voz = obtener_saludo_inicial()
    
    # NIVY saluda siempre por pantalla y por VOZ
    responder(saludo_consola)
    voz.hablar(saludo_voz)

    try:
        while True:
            # Capturar comando según el modo elegido
            if modo_actual == "v":
                entrada = voz.escuchar(duracion=6)
            else:
                entrada = leer_comando()

            if not entrada:
                if modo_actual == "t":
                    responder("No capturé nada. Inténtalo de nuevo.")
                continue

            if motor.normalizar(entrada) in {"salir", "cerrar", "terminar", "s"}:
                mensaje = "Hasta luego. ¡Que tengas un excelente día!"
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

            # ---------------------------------------------------------
            # CAMBIO DE MODO DINÁMICO
            # ---------------------------------------------------------
            if accion_nombre == "modo_texto":
                modo_actual = "t"
                msj = regla.get("respuesta", "Cambiando a entrada por texto.")
                responder(msj)
                voz.hablar(msj)
                continue
            
            elif accion_nombre == "modo_voz":
                modo_actual = "v"
                msj = regla.get("respuesta", "Cambiando a entrada por voz.")
                responder(msj)
                voz.hablar(msj)
                continue

            # ---------------------------------------------------------
            # CONFIGURAR RESPUESTA
            # ---------------------------------------------------------
            respuesta_consola = regla.get("respuesta", f"Ejecutando {regla['nombre']}.")
            respuesta_voz = respuesta_consola

            # PROCESAR ACCIONES (Retornan Tupla: Texto_Consola, Texto_Voz)
            if accion_nombre in [
                "hora", "fecha", "noticias", "ayuda", "buscar", 
                "abrir_noticia", "enviar_whatsapp", "leer_whatsapp"
            ]:
                # Pasamos 'reproductor' y 'whatsapp' a la función ejecutar
                resultado_ejecucion = ejecutar(accion_nombre, resultado, motor.conocimiento, reproductor, whatsapp)
                
                # Verificamos si la función nos devolvió una tupla con dos respuestas (Consola, Voz)
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

            # ---------------------------------------------------------
            # NIVY RESPONDE
            # ---------------------------------------------------------
            # Imprime en consola (puede contener texto, menús y URLs formateadas)
            responder(respuesta_consola)
            
            # Habla (solo si el método de entrada actual es voz)
            if modo_actual == "v":
                voz.hablar(respuesta_voz)

            # EJECUCIÓN PESADA DEL NAVEGADOR PARA REPRODUCTOR
            if accion_nombre in [
                "reproducir_playlist", "siguiente_cancion", "cancion_anterior", 
                "estado_reproduccion", "pausar_reproduccion", "reanudar_reproduccion"
            ]:
                resultado_accion = ejecutar(accion_nombre, resultado, motor.conocimiento, reproductor, whatsapp)
                # Si la acción devuelve una tupla, ignoramos imprimirla de nuevo
                if not isinstance(resultado_accion, tuple) and accion_nombre not in ["estado_reproduccion"]:
                    print(f"NIVY > {resultado_accion}")

            print(f"[EXPLICACIÓN] {generar_explicacion(resultado)}")

    finally:
        reproductor.cerrar()
        whatsapp.cerrar()

if __name__ == "__main__":
    main()