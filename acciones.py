from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo
import webbrowser


ZONA_HORARIA = ZoneInfo("America/El_Salvador")
YOUTUBE_URL = "https://www.youtube.com/"
BUSQUEDA_URL = "https://www.google.com/search?q={}"
NOTICIAS_RSS = "https://news.google.com/rss?hl=es-419&gl=SV&ceid=SV:es-419"


def ahora():
    return datetime.now(ZONA_HORARIA)


def ejecutar(accion, resultado, conocimiento):
    if accion == "hora":
        return f"La hora actual es {ahora().strftime('%H:%M:%S')}."

    if accion == "fecha":
        dias = [
            "lunes", "martes", "miércoles", "jueves",
            "viernes", "sábado", "domingo"
        ]
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        fecha = ahora()
        return (
            f"Hoy es {dias[fecha.weekday()]} "
            f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}."
        )

    if accion == "reproducir_playlist":
        url = conocimiento.get("playlist_musica", "")
        if not url or "https://www.youtube.com/playlist?list=PLI1yT-YHTPFY" in url:
            return (
                "No has configurado la playlist todavía. "
                "Edita conocimiento/reglas.json y reemplaza la URL de ejemplo."
            )
        webbrowser.open_new_tab(url)
        return "Abriendo tu playlist de música en el navegador."

    if accion == "youtube":
        webbrowser.open_new_tab(YOUTUBE_URL)
        return "Abriendo YouTube."

    if accion == "buscar":
        grupos = resultado.get("grupos", ())
        consulta = grupos[0].strip() if grupos and grupos[0] else ""
        if not consulta:
            return "No encontré qué quieres buscar."
        webbrowser.open_new_tab(BUSQUEDA_URL.format(quote_plus(consulta)))
        return f"Buscando en internet: {consulta}"

    if accion == "noticias":
        return obtener_noticias()

    if accion == "ayuda":
        return (
            "Puedo ayudarte con: hora, fecha, YouTube, tu playlist, "
            "noticias y búsquedas en internet."
        )

    return f"La acción '{accion}' todavía no está implementada."


def obtener_noticias(limite=7):
    try:
        solicitud = Request(
            NOTICIAS_RSS,
            headers={"User-Agent": "NIVY/1.0"}
        )

        with urlopen(solicitud, timeout=10) as respuesta:
            xml = respuesta.read()

        raiz = ET.fromstring(xml)
        noticias = []

        for item in raiz.findall(".//item")[:limite]:
            titulo = item.findtext("title", default="Sin título").strip()
            enlace = item.findtext("link", default="").strip()
            noticias.append((titulo, enlace))

        if not noticias:
            return "No se pudieron encontrar noticias en este momento."

        salida = ["Noticias recientes:"]
        for indice, (titulo, enlace) in enumerate(noticias, start=1):
            salida.append(f"{indice}. {titulo}")
            if enlace:
                salida.append(f"   {enlace}")

        return "\n".join(salida)

    except Exception as error:
        return f"No pude consultar las noticias ahora. Detalle: {error}"
