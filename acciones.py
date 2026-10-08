from datetime import datetime
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

import webbrowser


ZONA_HORARIA = ZoneInfo("America/El_Salvador")

YOUTUBE_URL = "https://www.youtube.com/"

BUSQUEDA_URL = "https://www.google.com/search?q={}"

NOTICIAS_RSS = (
    "https://news.google.com/rss?"
    "hl=es-419&gl=SV&ceid=SV:es-419"
)


def ahora():
    return datetime.now(ZONA_HORARIA)


def ejecutar(
    accion,
    resultado,
    conocimiento,
    reproductor=None
):

    # ---------------------------------------------------------
    # HORA
    # ---------------------------------------------------------

    if accion == "hora":

        return (
            f"La hora actual es "
            f"{ahora().strftime('%H:%M:%S')}."
        )

    # ---------------------------------------------------------
    # FECHA
    # ---------------------------------------------------------

    if accion == "fecha":

        dias = [
            "lunes",
            "martes",
            "miércoles",
            "jueves",
            "viernes",
            "sábado",
            "domingo"
        ]

        meses = [
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre"
        ]

        fecha = ahora()

        return (
            f"Hoy es {dias[fecha.weekday()]} "
            f"{fecha.day} de "
            f"{meses[fecha.month - 1]} "
            f"de {fecha.year}."
        )

    # ---------------------------------------------------------
    # REPRODUCIR PLAYLIST
    # ---------------------------------------------------------

    if accion == "reproducir_playlist":

        if reproductor is None:
            return "El reproductor no está disponible."

        grupos = resultado.get(
            "grupos",
            ()
        )

        nombre_playlist = ""

        if grupos and grupos[0]:
            nombre_playlist = grupos[0].strip()

        # Frases que significan playlist por defecto
        valores_genericos = {
            "",
            "mi playlist",
            "mi musica",
            "musica",
            "playlist"
        }

        if nombre_playlist.lower() in valores_genericos:
            nombre_playlist = None

        return reproductor.reproducir_playlist(
            nombre_playlist
        )

    # ---------------------------------------------------------
    # SIGUIENTE
    # ---------------------------------------------------------

    if accion == "siguiente_cancion":

        if reproductor is None:
            return "El reproductor no está disponible."

        return reproductor.siguiente()

    # ---------------------------------------------------------
    # ANTERIOR
    # ---------------------------------------------------------

    if accion == "cancion_anterior":

        if reproductor is None:
            return "El reproductor no está disponible."

        return reproductor.anterior()

    # ---------------------------------------------------------
    # ESTADO DE REPRODUCCIÓN
    # ---------------------------------------------------------

    if accion == "estado_reproduccion":

        if reproductor is None:
            return "El reproductor no está disponible."

        return reproductor.estado()

    # ---------------------------------------------------------
    # YOUTUBE
    # ---------------------------------------------------------

    if accion == "youtube":

        webbrowser.open_new_tab(
            YOUTUBE_URL
        )

        return "Abriendo YouTube."

    # ---------------------------------------------------------
    # BÚSQUEDA
    # ---------------------------------------------------------

    if accion == "buscar":

        grupos = resultado.get(
            "grupos",
            ()
        )

        consulta = (
            grupos[0].strip()
            if grupos and grupos[0]
            else ""
        )

        if not consulta:
            return "No encontré qué quieres buscar."

        webbrowser.open_new_tab(
            BUSQUEDA_URL.format(
                quote_plus(consulta)
            )
        )

        return (
            f"Buscando en internet: "
            f"{consulta}"
        )

    # ---------------------------------------------------------
    # NOTICIAS
    # ---------------------------------------------------------

    if accion == "noticias":

        return obtener_noticias()

    # ---------------------------------------------------------
    # AYUDA
    # ---------------------------------------------------------

    if accion == "ayuda":

        return (
            "Puedo ayudarte con: "
            "hora, fecha, YouTube, playlists, "
            "siguiente canción, canción anterior, "
            "estado de reproducción, noticias "
            "y búsquedas en internet."
        )

    return (
        f"La acción '{accion}' "
        f"todavía no está implementada."
    )


def obtener_noticias(limite=7):

    try:

        solicitud = Request(
            NOTICIAS_RSS,
            headers={
                "User-Agent": "NIVY/1.0"
            }
        )

        with urlopen(
            solicitud,
            timeout=10
        ) as respuesta:

            xml = respuesta.read()

        raiz = ET.fromstring(xml)

        noticias = []

        for item in raiz.findall(
            ".//item"
        )[:limite]:

            titulo = item.findtext(
                "title",
                default="Sin título"
            ).strip()

            enlace = item.findtext(
                "link",
                default=""
            ).strip()

            noticias.append(
                (
                    titulo,
                    enlace
                )
            )

        if not noticias:

            return (
                "No se pudieron encontrar "
                "noticias en este momento."
            )

        salida = [
            "Noticias recientes:"
        ]

        for indice, (
            titulo,
            enlace
        ) in enumerate(
            noticias,
            start=1
        ):

            salida.append(
                f"{indice}. {titulo}"
            )

            if enlace:

                salida.append(
                    f"   {enlace}"
                )

        return "\n".join(
            salida
        )

    except Exception as error:

        return (
            "No pude consultar las noticias "
            f"ahora. Detalle: {error}"
        )