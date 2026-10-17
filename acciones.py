import json
import re
from datetime import datetime
from urllib.parse import quote_plus, unquote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo
import webbrowser

ZONA_HORARIA = ZoneInfo("America/El_Salvador")
YOUTUBE_URL = "https://www.youtube.com/"
BUSQUEDA_URL = "https://www.google.com/search?q={}"
NOTICIAS_RSS = "https://news.google.com/rss?hl=es-419&gl=SV&ceid=SV:es-419"

# Variables globales para guardar las últimas noticias consultadas
ULTIMAS_NOTICIAS = []

def ahora():
    return datetime.now(ZONA_HORARIA)

def buscar_informacion(consulta):
    """Busca primero en Wikipedia (definiciones exactas) y luego en la web (DuckDuckGo)"""
    
    # Intento 1: API de búsqueda de Wikipedia (Tolera errores ortográficos y mayúsculas)
    try:
        url_busqueda = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(consulta)}&utf8=&format=json"
        solicitud_busqueda = Request(url_busqueda, headers={"User-Agent": "NIVY/1.0"})
        
        with urlopen(solicitud_busqueda, timeout=5) as respuesta:
            datos_busqueda = json.loads(respuesta.read())
            resultados = datos_busqueda.get("query", {}).get("search", [])
            
            if resultados:
                # Tomar el título exacto del primer resultado (Ej: corrige "sistema experto" a "Sistema experto")
                titulo_exacto = resultados[0]["title"]
                titulo_url = quote_plus(titulo_exacto.replace(" ", "_"))
                
                url_resumen = f"https://es.wikipedia.org/api/rest_v1/page/summary/{titulo_url}"
                solicitud_resumen = Request(url_resumen, headers={"User-Agent": "NIVY/1.0"})
                
                with urlopen(solicitud_resumen, timeout=5) as resp_resumen:
                    datos_resumen = json.loads(resp_resumen.read())
                    resumen = datos_resumen.get("extract")
                    enlace = datos_resumen.get("content_urls", {}).get("desktop", {}).get("page", "")
                    
                    if resumen and enlace:
                        consola = f"Resumen (Wikipedia): {resumen}\n-> [Ir a la fuente]({enlace})"
                        voz = f"Esto encontré sobre {consulta}: {resumen}"
                        return consola, voz
    except Exception:
        pass # Si falla Wikipedia, pasamos a DuckDuckGo web
    
    # Intento 2: Raspado web tolerante en DuckDuckGo (para búsquedas generales)
    try:
        url_ddg = f"https://html.duckduckgo.com/html/?q={quote_plus(consulta)}"
        solicitud_ddg = Request(url_ddg, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        
        with urlopen(solicitud_ddg, timeout=7) as respuesta:
            html = respuesta.read().decode('utf-8')
        
        # Regex más flexible: DuckDuckGo a veces usa <a> o <div> para los resultados
        snippet_match = re.search(r'class="result__snippet[^>]*>(.*?)(?:<\/a>|<\/div>)', html, re.IGNORECASE | re.DOTALL)
        link_match = re.search(r'<a class="result__url" href="([^"]+)"', html, re.IGNORECASE)
        
        if snippet_match and link_match:
            # Limpiar etiquetas HTML residuales (<b>, </b>, etc.)
            resumen_html = snippet_match.group(1)
            resumen = re.sub(r'<[^>]+>', '', resumen_html).strip()
            
            enlace = link_match.group(1)
            # Limpiar redirecciones internas de DuckDuckGo en el link
            if "uddg=" in enlace:
                enlace = unquote(enlace.split("uddg=")[1].split("&")[0])

            if resumen:
                consola = f"Resumen Web: {resumen}\n-> [Ir a la fuente]({enlace})"
                voz = f"Esto encontré en la web sobre {consulta}: {resumen}"
                return consola, voz
    except Exception:
        pass # Fallo en el raspado, pasamos a Google
    
    # Fallback 3: Si todo falla, abrimos el buscador de Google en el navegador
    enlace_google = BUSQUEDA_URL.format(quote_plus(consulta))
    consola = f"Te mostraré los resultados directamente en tu navegador:\n-> [Ir a resultados]({enlace_google})"
    voz = f"He abierto los resultados de {consulta} en tu navegador."
    webbrowser.open_new_tab(enlace_google)
    
    return consola, voz

def ejecutar(accion, resultado, conocimiento, reproductor=None):
    # NOTA: Ahora las funciones devuelven una Tupla -> (Texto_Consola, Texto_Voz)
    
    if accion == "hora":
        msj = f"La hora actual es {ahora().strftime('%H:%M:%S')}."
        return msj, msj

    if accion == "fecha":
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        fecha = ahora()
        msj = f"Hoy es {dias[fecha.weekday()]} {fecha.day} de {meses[fecha.month - 1]} de {fecha.year}."
        return msj, msj

    if accion == "reproducir_playlist":
        if reproductor is None: return "El reproductor no está disponible.", "El reproductor no está disponible."
        grupos = resultado.get("grupos", ())
        nombre_playlist = grupos[0].strip() if grupos and grupos[0] else ""
        if nombre_playlist.lower() in {"", "mi playlist", "mi musica", "musica", "playlist"}:
            nombre_playlist = None
        msj = reproductor.reproducir_playlist(nombre_playlist)
        return msj, msj

    if accion in ["siguiente_cancion", "cancion_anterior", "pausar_reproduccion", "reanudar_reproduccion", "estado_reproduccion"]:
        if reproductor is None: return "Sin reproductor.", "Sin reproductor."
        if accion == "siguiente_cancion": msj = reproductor.siguiente()
        elif accion == "cancion_anterior": msj = reproductor.anterior()
        elif accion == "pausar_reproduccion": msj = reproductor.pausar()
        elif accion == "reanudar_reproduccion": msj = reproductor.reanudar()
        elif accion == "estado_reproduccion": msj = reproductor.estado()
        return msj, msj

    if accion == "youtube":
        webbrowser.open_new_tab(YOUTUBE_URL)
        return "Abriendo YouTube.", "Abriendo YouTube."

    if accion == "buscar":
        grupos = resultado.get("grupos", ())
        consulta = grupos[0].strip() if grupos and grupos[0] else ""
        if not consulta:
            return "No especificaste la búsqueda.", "No especificaste qué quieres buscar."
        return buscar_informacion(consulta)

    if accion == "noticias":
        return obtener_noticias()

    if accion == "abrir_noticia":
        grupos = resultado.get("grupos", ())
        if grupos and grupos[0].isdigit():
            indice = int(grupos[0]) - 1 # Restamos 1 porque el usuario dice "1" pero en la lista es "0"
            if 0 <= indice < len(ULTIMAS_NOTICIAS):
                enlace = ULTIMAS_NOTICIAS[indice]
                webbrowser.open_new_tab(enlace)
                msj = f"Abriendo la noticia {indice + 1} en tu navegador."
                return msj, msj
            else:
                msj = "El número de noticia no es válido. Primero pídemelas de nuevo."
                return msj, msj
        return "Falta el número de la noticia.", "Falta el número de la noticia."

    if accion == "ayuda":
        msj = "Puedo darte hora, fecha, resumirte búsquedas de internet, abrir noticias por número, y gestionar tu música en YouTube."
        return msj, msj

    return f"La acción '{accion}' no está implementada.", "Acción no implementada."

def obtener_noticias(limite=5):
    global ULTIMAS_NOTICIAS
    try:
        solicitud = Request(NOTICIAS_RSS, headers={"User-Agent": "NIVY/1.0"})
        with urlopen(solicitud, timeout=10) as respuesta:
            xml = respuesta.read()
        raiz = ET.fromstring(xml)

        noticias = []
        for item in raiz.findall(".//item")[:limite]:
            titulo = item.findtext("title", default="Sin título").strip()
            enlace = item.findtext("link", default="").strip()
            noticias.append((titulo, enlace))

        if not noticias:
            return "No encontré noticias.", "No encontré noticias actuales."

        # Guardamos URLs en la memoria temporal para el comando "abrir noticia"
        ULTIMAS_NOTICIAS.clear()
        for _, enlace in noticias:
            ULTIMAS_NOTICIAS.append(enlace)

        # SEPARACIÓN: Texto para imprimir vs Texto para hablar
        principal_titulo, principal_enlace = noticias[0]
        
        consola = [
            f"🗞️ NOTICIA PRINCIPAL (Índice 1): {principal_titulo}",
            f"   -> [Ir a noticia]({principal_enlace})\n",
            "Otras recomendaciones:"
        ]
        
        voz = [f"La noticia principal es: {principal_titulo}."]
        
        for indice, (titulo, enlace) in enumerate(noticias[1:], start=2):
            consola.append(f"{indice}. {titulo}\n   -> [Ir a noticia]({enlace})")
            # NIVY solo leerá los títulos limpios
            voz.append(f"Noticia {indice}: {titulo}.")

        consola.append("\n💡 Di 'abre la noticia 2' para visualizarla en tu navegador.")
        
        return "\n".join(consola), " ".join(voz)

    except Exception as error:
        return f"Error al consultar noticias: {error}", "No pude consultar las noticias debido a un error de red."