from pathlib import Path
import json
import os
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Reproductor:
    """
    Gestiona las playlists y el estado de reproducción de NIVY.

    Utiliza una única pestaña de Chrome para reproducir
    y cambiar entre canciones.
    """

    def __init__(
        self,
        conocimiento,
        archivo_estado="conocimiento/estado_reproduccion.json"
    ):
        self.conocimiento = conocimiento

        self.youtube = conocimiento.get(
            "youtube",
            {}
        )

        self.playlists = self.youtube.get(
            "playlists",
            {}
        )

        reproduccion = self.youtube.get(
            "reproduccion",
            {}
        )

        self.repetir_playlist = reproduccion.get(
            "repetir_playlist",
            True
        )

        self.archivo_estado = Path(
            archivo_estado
        )

        self.playlist_actual = None
        self.indice_actual = 0
        self.canciones = []

        # Navegador controlado por NIVY
        self.driver = None

        self._cargar_estado()

    # =========================================================
    # NORMALIZACIÓN
    # =========================================================

    @staticmethod
    def normalizar(texto):

        return (
            texto
            .strip()
            .lower()
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
        )

    # =========================================================
    # NAVEGADOR
    # =========================================================

    def _iniciar_navegador(self):
        if self.driver is not None:
            return

        opciones = Options()
        # Nos conectamos a la instancia de Brave que ya abrimos con --remote-debugging-port=9222
        opciones.debugger_address = "127.0.0.1:9222"
        
        # Indicamos la ruta de Brave por si acaso
        opciones.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

        # Inicializamos el driver conectado a esa sesión existente
        self.driver = webdriver.Chrome(options=opciones)        
        self.driver.maximize_window()
        
    # =========================================================
    # ESTADO
    # =========================================================

    def _cargar_estado(self):

        if not self.archivo_estado.exists():
            return

        try:

            with self.archivo_estado.open(
                "r",
                encoding="utf-8"
            ) as archivo:

                estado = json.load(
                    archivo
                )

            self.playlist_actual = estado.get(
                "playlist_actual"
            )

            self.indice_actual = estado.get(
                "indice_actual",
                0
            )

        except (
            json.JSONDecodeError,
            OSError
        ):

            self.playlist_actual = None
            self.indice_actual = 0

    def _guardar_estado(self):

        self.archivo_estado.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        estado = {
            "playlist_actual": self.playlist_actual,
            "indice_actual": self.indice_actual
        }

        with self.archivo_estado.open(
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                estado,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    # =========================================================
    # PLAYLISTS
    # =========================================================

    def listar_playlists(self):

        return list(
            self.playlists.keys()
        )

    def buscar_playlist(self, nombre=None):

        if not self.playlists:
            return None

        # Si no especificamos playlist,
        # usamos la primera.
        if not nombre:
            return next(
                iter(self.playlists)
            )

        nombre_normalizado = self.normalizar(
            nombre
        )

        # Buscar por clave
        for clave in self.playlists:

            if (
                self.normalizar(clave)
                == nombre_normalizado
            ):
                return clave

        # Buscar por nombre visible
        for clave, datos in self.playlists.items():

            nombre_visible = datos.get(
                "nombre",
                clave
            )

            if (
                self.normalizar(nombre_visible)
                == nombre_normalizado
            ):
                return clave

        # Buscar coincidencia parcial
        for clave, datos in self.playlists.items():

            nombre_visible = datos.get(
                "nombre",
                clave
            )

            if (
                nombre_normalizado
                in self.normalizar(clave)
                or
                nombre_normalizado
                in self.normalizar(nombre_visible)
            ):
                return clave

        return None

    # =========================================================
    # OBTENER CANCIONES DE YOUTUBE
    # =========================================================

    def cargar_canciones(
        self,
        clave_playlist
    ):

        if clave_playlist not in self.playlists:
            return []

        playlist = self.playlists[
            clave_playlist
        ]

        url = playlist.get(
            "url"
        )

        if not url:
            return []

        opciones = {
            "extract_flat": True,
            "quiet": True,
            "skip_download": True,
            "ignoreerrors": True
        }

        try:

            with yt_dlp.YoutubeDL(
                opciones
            ) as ydl:

                informacion = ydl.extract_info(
                    url,
                    download=False
                )

            entradas = informacion.get(
                "entries",
                []
            )

            canciones = []

            for entrada in entradas:

                if not entrada:
                    continue

                video_id = entrada.get(
                    "id"
                )

                if not video_id:
                    continue

                titulo = entrada.get(
                    "title",
                    "Canción sin título"
                )

                url_video = (
                    "https://www.youtube.com/watch?v="
                    + video_id
                )

                canciones.append(
                    {
                        "titulo": titulo,
                        "url": url_video,
                        "id": video_id
                    }
                )

            return canciones

        except Exception as error:

            print(
                f"[REPRODUCTOR] "
                f"Error al cargar playlist: {error}"
            )

            return []

    # =========================================================
    # REPRODUCIR PLAYLIST
    # =========================================================

    def reproducir_playlist(
        self,
        nombre=None
    ):

        clave = self.buscar_playlist(
            nombre
        )

        if not clave:

            disponibles = ", ".join(
                self.playlists.keys()
            )

            return (
                "No encontré esa playlist. "
                f"Playlists disponibles: "
                f"{disponibles}"
            )

        canciones = self.cargar_canciones(
            clave
        )

        if not canciones:

            return (
                f"No pude obtener las canciones "
                f"de la playlist '{clave}'."
            )

        self.playlist_actual = clave

        self.canciones = canciones

        self.indice_actual = 0

        self._guardar_estado()

        return self._abrir_cancion()

    # =========================================================
    # ABRIR / CAMBIAR CANCIÓN
    # =========================================================

    def _abrir_cancion(self):

        if not self.canciones:
            return "No hay canciones disponibles."

        if (
            self.indice_actual < 0
            or
            self.indice_actual
            >= len(self.canciones)
        ):
            return (
                "La posición de la canción "
                "no es válida."
            )

        cancion = self.canciones[
            self.indice_actual
        ]

        self._iniciar_navegador()

        # Navegar en la MISMA pestaña
        self.driver.get(
            cancion["url"]
        )

        self._guardar_estado()

        playlist = self.playlists[
            self.playlist_actual
        ]

        nombre_playlist = playlist.get(
            "nombre",
            self.playlist_actual
        )

        return (
            f"Reproduciendo: "
            f"{cancion['titulo']} "
            f"({self.indice_actual + 1}/"
            f"{len(self.canciones)}) "
            f"de '{nombre_playlist}'."
        )

    # =========================================================
    # SIGUIENTE
    # =========================================================

    def siguiente(self):

        if not self.playlist_actual:

            return (
                "No hay ninguna playlist "
                "seleccionada. Primero dime "
                "qué playlist quieres reproducir."
            )

        if not self.canciones:

            self.canciones = (
                self.cargar_canciones(
                    self.playlist_actual
                )
            )

        if not self.canciones:

            return (
                "No hay canciones disponibles."
            )

        siguiente_indice = (
            self.indice_actual + 1
        )

        if (
            siguiente_indice
            >= len(self.canciones)
        ):

            if self.repetir_playlist:

                siguiente_indice = 0

            else:

                return (
                    "Ya estás en la última "
                    "canción de la playlist."
                )

        self.indice_actual = (
            siguiente_indice
        )

        return self._abrir_cancion()

    # =========================================================
    # ANTERIOR
    # =========================================================

    def anterior(self):

        if not self.playlist_actual:

            return (
                "No hay ninguna playlist "
                "seleccionada. Primero "
                "reproduce una playlist."
            )

        if not self.canciones:

            self.canciones = (
                self.cargar_canciones(
                    self.playlist_actual
                )
            )

        if not self.canciones:

            return (
                "No hay canciones disponibles."
            )

        anterior_indice = (
            self.indice_actual - 1
        )

        if anterior_indice < 0:

            if self.repetir_playlist:

                anterior_indice = (
                    len(self.canciones) - 1
                )

            else:

                return (
                    "Ya estás en la primera "
                    "canción de la playlist."
                )

        self.indice_actual = (
            anterior_indice
        )

        return self._abrir_cancion()

    # =========================================================
    # ESTADO
    # =========================================================

    def estado(self):

        if not self.playlist_actual:

            return (
                "No hay ninguna canción "
                "reproduciéndose."
            )

        if not self.canciones:

            self.canciones = (
                self.cargar_canciones(
                    self.playlist_actual
                )
            )

        if not self.canciones:

            return (
                "No se pudo obtener el "
                "estado de reproducción."
            )

        cancion = self.canciones[
            self.indice_actual
        ]

        playlist = self.playlists[
            self.playlist_actual
        ]

        nombre_playlist = playlist.get(
            "nombre",
            self.playlist_actual
        )

        return (
            f"Estás escuchando "
            f"'{cancion['titulo']}' "
            f"de la playlist "
            f"'{nombre_playlist}'. "
            f"Canción "
            f"{self.indice_actual + 1} "
            f"de {len(self.canciones)}."
        )

    # =========================================================
    # CERRAR NAVEGADOR
    # =========================================================

    def cerrar(self):

        if self.driver is not None:

            try:
                self.driver.quit()
            except Exception:
                pass

            self.driver = None