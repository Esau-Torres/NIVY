
import time
import unicodedata

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)


class GestorWhatsApp:

    def __init__(self):
        self.driver = None
        self.whatsapp_url = "https://web.whatsapp.com/"

    # ---------------------------------------------------------
    # NORMALIZACION DE TEXTO
    # ---------------------------------------------------------

    @staticmethod
    def _normalizar(texto):
        texto = unicodedata.normalize("NFD", str(texto or ""))
        texto = "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

        return " ".join(texto.casefold().split())

    # ---------------------------------------------------------
    # INICIAR O CONECTAR CON BRAVE
    # ---------------------------------------------------------

    def _iniciar_navegador(self):
        if self.driver is not None:
            try:
                # Comprobar que la sesión de Selenium siga activa.
                self.driver.current_url
                return
            except WebDriverException:
                self.driver = None

        opciones = Options()

        # Brave debe haberse iniciado con el puerto 9222 habilitado.
        opciones.debugger_address = "127.0.0.1:9222"

        opciones.binary_location = (
            r"C:\Program Files\BraveSoftware"
            r"\Brave-Browser\Application\brave.exe"
        )

        self.driver = webdriver.Chrome(options=opciones)

        try:
            self.driver.maximize_window()
        except WebDriverException:
            pass

    # ---------------------------------------------------------
    # ABRIR O ENFOCAR WHATSAPP WEB
    # ---------------------------------------------------------

    def _abrir_o_enfocar_whatsapp(self):
        try:
            self._iniciar_navegador()

            pestaña_encontrada = False

            # Reutilizar una pestaña de WhatsApp ya abierta.
            for handle in self.driver.window_handles:
                try:
                    self.driver.switch_to.window(handle)

                    if (
                        "web.whatsapp.com"
                        in self.driver.current_url.lower()
                    ):
                        pestaña_encontrada = True
                        break

                except WebDriverException:
                    continue

            # Si no existe, abrir WhatsApp en una nueva pestaña.
            if not pestaña_encontrada:
                handles_anteriores = set(
                    self.driver.window_handles
                )

                self.driver.execute_script(
                    "window.open(arguments[0], '_blank');",
                    self.whatsapp_url
                )

                WebDriverWait(self.driver, 10).until(
                    lambda d: len(d.window_handles)
                    > len(handles_anteriores)
                )

                handles_nuevos = [
                    handle
                    for handle in self.driver.window_handles
                    if handle not in handles_anteriores
                ]

                if not handles_nuevos:
                    return False

                self.driver.switch_to.window(handles_nuevos[-1])

            # Esperar a que cargue la interfaz principal.
            WebDriverWait(self.driver, 45).until(
                lambda d: d.find_elements(
                    By.CSS_SELECTOR,
                    "#pane-side, [aria-label='Chat list']"
                )
            )

            print("[WHATSAPP_DEBUG] Interfaz principal cargada.")
            return True

        except TimeoutException:
            print(
                "[WHATSAPP_DEBUG] WhatsApp no terminó de cargar. "
                "Revisa la sesión y el inicio de sesión."
            )

            if self.driver is not None:
                try:
                    print(
                        "[WHATSAPP_DEBUG] URL:",
                        self.driver.current_url
                    )
                    print(
                        "[WHATSAPP_DEBUG] Título:",
                        self.driver.title
                    )
                except WebDriverException:
                    pass

            return False

        except Exception as e:
            print(
                f"[WHATSAPP_DEBUG] Error al abrir WhatsApp: {e!r}"
            )
            return False

    # ---------------------------------------------------------
    # VERIFICAR SI UN ELEMENTO ESTA VISIBLE Y ES EDITABLE
    # ---------------------------------------------------------

    @staticmethod
    def _es_visible_y_editable(elemento):
        try:
            if not elemento.is_displayed():
                return False

            if not elemento.is_enabled():
                return False

            etiqueta = elemento.tag_name.lower()
            contenteditable = (
                elemento.get_attribute("contenteditable") or ""
            ).lower()

            rol = (
                elemento.get_attribute("role") or ""
            ).lower()

            return (
                etiqueta in ("input", "textarea")
                or contenteditable == "true"
                or rol == "textbox"
            )

        except (
            StaleElementReferenceException,
            WebDriverException
        ):
            return False

    # ---------------------------------------------------------
    # LOCALIZAR LA CAJA DE BUSQUEDA LATERAL
    # ---------------------------------------------------------

    def _encontrar_caja_busqueda(self, driver):
        selectores = [
            (
                By.CSS_SELECTOR,
                'input[placeholder="Buscar un chat o iniciar uno nuevo"]'
            ),
            (
                By.CSS_SELECTOR,
                'input[aria-label="Buscar un chat o iniciar uno nuevo"]'
            ),
            (
                By.CSS_SELECTOR,
                'input[data-tab="3"]'
            ),
            (
                By.CSS_SELECTOR,
                'input[role="textbox"][placeholder*="Buscar"]'
            ),
            (
                By.CSS_SELECTOR,
                "#side [contenteditable='true'][data-tab='3']"
            ),
            (
                By.CSS_SELECTOR,
                "#side [role='textbox'][contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "#side [contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "#side input[type='text']"
            ),
            (
                By.CSS_SELECTOR,
                "[data-testid='chat-list-search'] "
                "[contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "[data-testid='chat-list-search']"
                "[contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "div[contenteditable='true'][data-tab='3']"
            ),
            (
                By.CSS_SELECTOR,
                "[aria-label='Ask Meta AI or Search']"
            ),
            (
                By.CSS_SELECTOR,
                "[aria-label*='Search' i][contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "[aria-label*='Buscar' i][contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "[title*='Search or start new chat' i]"
                "[contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "[title*='Buscar o empezar un chat nuevo' i]"
                "[contenteditable='true']"
            ),
        ]

        for by, selector in selectores:
            try:
                elementos = driver.find_elements(by, selector)

                for elemento in elementos:
                    if not self._es_visible_y_editable(elemento):
                        continue

                    # No confundir la caja de búsqueda con
                    # el editor del mensaje.
                    esta_en_editor_mensaje = driver.execute_script(
                        """
                        return arguments[0].closest(
                            '#main footer'
                        ) !== null;
                        """,
                        elemento
                    )

                    if esta_en_editor_mensaje:
                        continue

                    return elemento

            except (
                StaleElementReferenceException,
                WebDriverException
            ):
                continue

        return False

    # ---------------------------------------------------------
    # ACTIVAR LA BUSQUEDA SI SOLO APARECE UN BOTON
    # ---------------------------------------------------------

    def _activar_control_busqueda(self):
        selectores = [
            "#side [aria-label*='Search' i]",
            "#side [aria-label*='Buscar' i]",
            "#side [title*='Search' i]",
            "#side [title*='Buscar' i]",
            "#side [data-testid*='search' i]",
            "[aria-label='Ask Meta AI or Search']",
        ]

        for selector in selectores:
            try:
                elementos = self.driver.find_elements(
                    By.CSS_SELECTOR, selector
                )

                for elemento in elementos:
                    try:
                        if not elemento.is_displayed():
                            continue

                        # Si ya es un campo editable, no hace falta
                        # activar un botón.
                        if self._es_visible_y_editable(elemento):
                            return True

                        elemento.click()
                        time.sleep(0.4)

                        if self._encontrar_caja_busqueda(
                            self.driver
                        ):
                            return True

                    except (
                        StaleElementReferenceException,
                        WebDriverException
                    ):
                        continue

            except WebDriverException:
                continue

        return False

    def _obtener_caja_busqueda(self, timeout=8):
        caja = self._encontrar_caja_busqueda(self.driver)

        if caja:
            return caja

        self._activar_control_busqueda()

        try:
            return WebDriverWait(
                self.driver, timeout
            ).until(
                lambda d: self._encontrar_caja_busqueda(d)
                or False
            )

        except TimeoutException:
            return None

    # ---------------------------------------------------------
    # DIAGNOSTICO DE LOS CAMPOS VISIBLES
    # ---------------------------------------------------------

    def _diagnosticar_campos(self):
        try:
            campos = self.driver.execute_script(
                """
                return Array.from(
                    document.querySelectorAll(
                        'input, textarea, '
                        + '[contenteditable="true"], '
                        + '[role="textbox"]'
                    )
                )
                .filter(e =>
                    e.offsetWidth > 0 &&
                    e.offsetHeight > 0
                )
                .map(e => ({
                    tag: e.tagName,
                    role: e.getAttribute('role'),
                    aria: e.getAttribute('aria-label'),
                    title: e.getAttribute('title'),
                    placeholder: e.getAttribute('placeholder'),
                    dataTab: e.getAttribute('data-tab'),
                    testid: e.getAttribute('data-testid')
                }))
                .slice(0, 25);
                """
            )

            print(
                "[WHATSAPP_DEBUG] Campos visibles:",
                campos
            )

        except Exception as e:
            print(
                "[WHATSAPP_DEBUG] No se pudieron inspeccionar "
                f"los campos: {e!r}"
            )

    # ---------------------------------------------------------
    # LIMPIAR Y ESCRIBIR EN UN CAMPO
    # ---------------------------------------------------------

    @staticmethod
    def _escribir_en_caja(caja, texto):
        try:
            caja.click()
            caja.send_keys(Keys.CONTROL, "a")
            caja.send_keys(Keys.BACKSPACE)
            caja.send_keys(texto)
            return True

        except (
            StaleElementReferenceException,
            WebDriverException
        ):
            return False

    # ---------------------------------------------------------
    # ENCONTRAR EL RESULTADO EXACTO DEL CONTACTO
    # ---------------------------------------------------------

    def _encontrar_resultado_contacto(
        self, driver, contacto
    ):
        objetivo = self._normalizar(contacto)

        selectores = [
            "#pane-side span[title]",
            "#pane-side [data-testid='cell-frame-title']",
            "[role='dialog'] span[title]",
            "[data-testid='cell-frame-title']",
            "#app span[title]",
        ]

        elementos_vistos = set()

        for selector in selectores:
            try:
                elementos = driver.find_elements(
                    By.CSS_SELECTOR, selector
                )

                for elemento in elementos:
                    try:
                        if not elemento.is_displayed():
                            continue

                        if elemento.id in elementos_vistos:
                            continue

                        elementos_vistos.add(elemento.id)

                        # Evitar confundir el encabezado de un
                        # chat abierto con un resultado de búsqueda.
                        esta_en_chat = driver.execute_script(
                            """
                            return arguments[0].closest('#main')
                                !== null;
                            """,
                            elemento
                        )

                        if esta_en_chat:
                            continue

                        titulo = (
                            elemento.get_attribute("title")
                            or elemento.text
                            or ""
                        )

                        if self._normalizar(titulo) == objetivo:
                            return elemento

                    except (
                        StaleElementReferenceException,
                        WebDriverException
                    ):
                        continue

            except WebDriverException:
                continue

        return False

    def _esperar_resultado_contacto(self, contacto, timeout=7 ):
        try:
            return WebDriverWait(
                self.driver, timeout
            ).until(
                lambda d: self._encontrar_resultado_contacto(
                    d, contacto
                )
                or False
            )

        except TimeoutException:
            return None

    # ---------------------------------------------------------
    # ABRIR EL BOTON DE NUEVO CHAT
    # ---------------------------------------------------------

    def _abrir_nuevo_chat(self):
        selectores = [
            "[data-testid='compose-btn']",
            "#side [aria-label*='New chat' i]",
            "#side [aria-label*='Nuevo chat' i]",
            "#side [title*='New chat' i]",
            "#side [title*='Nuevo chat' i]",
        ]

        # Primero probar los selectores conocidos.
        for selector in selectores:
            try:
                elementos = self.driver.find_elements(
                    By.CSS_SELECTOR, selector
                )

                for elemento in elementos:
                    try:
                        if not elemento.is_displayed():
                            continue

                        elemento.click()
                        time.sleep(0.5)
                        return True

                    except WebDriverException:
                        try:
                            self.driver.execute_script(
                                "arguments[0].click();",
                                elemento
                            )
                            time.sleep(0.5)
                            return True
                        except WebDriverException:
                            continue

            except WebDriverException:
                continue

        # Como alternativa, inspeccionar los botones laterales.
        try:
            elementos = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#side button, #side [role='button'], "
                "#side [aria-label], #side [title]"
            )

            for elemento in elementos:
                try:
                    if not elemento.is_displayed():
                        continue

                    etiqueta = " ".join([
                        elemento.get_attribute("aria-label") or "",
                        elemento.get_attribute("title") or "",
                        elemento.get_attribute("data-testid") or "",
                    ])

                    etiqueta = self._normalizar(etiqueta)

                    terminos = (
                        "new chat",
                        "nuevo chat",
                        "new conversation",
                        "nueva conversacion",
                        "compose",
                    )

                    if any(
                        termino in etiqueta
                        for termino in terminos
                    ):
                        elemento.click()
                        time.sleep(0.5)
                        return True

                except (
                    StaleElementReferenceException,
                    WebDriverException
                ):
                    continue

        except WebDriverException:
            pass

        return False

    # ---------------------------------------------------------
    # BUSCAR EN EL PANEL DE NUEVO CHAT
    # ---------------------------------------------------------

    def _encontrar_busqueda_contactos(
        self, driver, caja_anterior=None
    ):
        selectores = [
            (By.CSS_SELECTOR, "[role='dialog'] input"),
            (
                By.CSS_SELECTOR,
                "[role='dialog'] [contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "[role='dialog'] [role='textbox']"
            ),
            (
                By.CSS_SELECTOR,
                "input[aria-label*='Search contacts' i]"
            ),
            (
                By.CSS_SELECTOR,
                "input[aria-label*='Buscar contactos' i]"
            ),
            (
                By.CSS_SELECTOR,
                "[contenteditable='true']"
                "[aria-label*='Search' i]"
            ),
            (
                By.CSS_SELECTOR,
                "[contenteditable='true']"
                "[aria-label*='Buscar' i]"
            ),
            (
                By.CSS_SELECTOR,
                "input[placeholder*='Search' i]"
            ),
            (
                By.CSS_SELECTOR,
                "input[placeholder*='Buscar' i]"
            ),
            (By.CSS_SELECTOR, "input[type='text']"),
            (
                By.CSS_SELECTOR,
                "[role='textbox'][contenteditable='true']"
            ),
            (By.CSS_SELECTOR, "[contenteditable='true']"),
        ]

        for by, selector in selectores:
            try:
                elementos = driver.find_elements(by, selector)

                for elemento in elementos:
                    if not self._es_visible_y_editable(elemento):
                        continue

                    # No devolver el mismo campo anterior.
                    if caja_anterior is not None:
                        try:
                            if elemento.id == caja_anterior.id:
                                continue
                        except WebDriverException:
                            pass

                    # No confundir el editor del mensaje con
                    # el buscador de contactos.
                    try:
                        esta_en_footer = driver.execute_script(
                            """
                            return arguments[0].closest(
                                '#main footer'
                            ) !== null;
                            """,
                            elemento
                        )

                        if esta_en_footer:
                            continue

                    except WebDriverException:
                        continue

                    return elemento

            except WebDriverException:
                continue

        return False

    # ---------------------------------------------------------
    # CONFIRMAR QUE EL CHAT ABIERTO ES EL CORRECTO
    # ---------------------------------------------------------

    def _chat_abierto(self, driver, nombre):
        objetivo = self._normalizar(nombre)

        selectores = [
            "#main header [title]",
            "#main header span[dir='auto']",
            "#main header "
            "[data-testid='conversation-info-header-chat-title']",
        ]

        for selector in selectores:
            try:
                elementos = driver.find_elements(
                    By.CSS_SELECTOR, selector
                )

                for elemento in elementos:
                    try:
                        if not elemento.is_displayed():
                            continue

                        titulo = (
                            elemento.get_attribute("title")
                            or elemento.text
                            or ""
                        )

                        if self._normalizar(titulo) == objetivo:
                            return True

                    except StaleElementReferenceException:
                        continue

            except WebDriverException:
                continue

        return False

    # ---------------------------------------------------------
    # ENCONTRAR EL EDITOR DEL MENSAJE
    # ---------------------------------------------------------

    def _encontrar_caja_mensaje(self, driver):
        selectores = [
            (
                By.CSS_SELECTOR,
                "#main footer "
                "[data-testid='conversation-compose-box-input']"
            ),
            (
                By.CSS_SELECTOR,
                "#main footer "
                "[contenteditable='true'][role='textbox']"
            ),
            (
                By.CSS_SELECTOR,
                "#main footer [contenteditable='true']"
            ),
            (
                By.CSS_SELECTOR,
                "#main [contenteditable='true']"
                "[aria-label*='Type a message' i]"
            ),
            (
                By.CSS_SELECTOR,
                "#main [contenteditable='true']"
                "[aria-label*='Escribe un mensaje' i]"
            ),
        ]

        for by, selector in selectores:
            try:
                elementos = driver.find_elements(by, selector)

                for elemento in elementos:
                    if self._es_visible_y_editable(elemento):
                        return elemento

            except WebDriverException:
                continue

        return False

    # ---------------------------------------------------------
    # ENVIAR MENSAJE
    # ---------------------------------------------------------

    def enviar_mensaje(self, contacto, mensaje):
        contacto = str(contacto or "").strip()
        mensaje = str(mensaje or "").strip()

        if not contacto:
            return "Error: no se especificó el contacto."

        if not mensaje:
            return "Error: el mensaje está vacío."

        if not self._abrir_o_enfocar_whatsapp():
            return (
                "No pude cargar WhatsApp Web. "
                "Verifica que Brave esté abierto, "
                "que el puerto 9222 esté habilitado "
                "y que hayas iniciado sesión."
            )

        try:
            print(
                f"[WHATSAPP_DEBUG] Contacto solicitado: "
                f"{contacto!r}"
            )
            print(
                f"[WHATSAPP_DEBUG] Mensaje: {mensaje!r}"
            )

            # PASO 1: Buscar mediante el campo lateral.
            caja_busqueda = self._obtener_caja_busqueda()

            resultado = None

            if caja_busqueda:
                escrito = self._escribir_en_caja(
                    caja_busqueda, contacto
                )

                if escrito:
                    resultado = self._esperar_resultado_contacto(
                        contacto, timeout=7
                    )
            else:
                print(
                    "[WHATSAPP_DEBUG] No se localizó "
                    "el buscador lateral."
                )

            # PASO 2: Si no se encontró, probar nuevo chat.
            # Esto ayuda cuando el contacto no aparece entre
            # los chats existentes.
            if resultado is None:
                if caja_busqueda is not None:
                    try:
                        caja_busqueda.click()
                        caja_busqueda.send_keys(
                            Keys.CONTROL, "a"
                        )
                        caja_busqueda.send_keys(Keys.BACKSPACE)
                        caja_busqueda.send_keys(Keys.ESCAPE)
                    except WebDriverException:
                        pass

                nuevo_chat_abierto = self._abrir_nuevo_chat()

                if nuevo_chat_abierto:
                    try:
                        caja_contactos = WebDriverWait(
                            self.driver, 8
                        ).until(
                            lambda d:
                            self._encontrar_busqueda_contactos(
                                d, caja_busqueda
                            )
                            or False
                        )

                    except TimeoutException:
                        caja_contactos = None

                    if caja_contactos:
                        escrito = self._escribir_en_caja(
                            caja_contactos, contacto
                        )

                        if escrito:
                            resultado = (
                                self._esperar_resultado_contacto(
                                    contacto, timeout=10
                                )
                            )

                    else:
                        print(
                            "[WHATSAPP_DEBUG] No se encontró "
                            "la búsqueda de contactos del "
                            "nuevo chat."
                        )

            # PASO 3: Si sigue sin existir resultado exacto,
            # no enviar a ningún contacto.
            if resultado is None:
                self._diagnosticar_campos()

                return (
                    f"No encontré un resultado exacto para "
                    f"'{contacto}'. Verifica el nombre del "
                    "contacto en WhatsApp."
                )

            nombre_real = (
                resultado.get_attribute("title")
                or resultado.text
                or contacto
            ).strip()

            print(
                "[WHATSAPP_DEBUG] Contacto localizado:",
                repr(nombre_real)
            )

            # PASO 4: Abrir el resultado localizado.
            try:
                fila_contacto = self.driver.execute_script(
                    """
                    const elemento = arguments[0];

                    return elemento.closest(
                        '[data-testid="cell-frame-container"], ' +
                        '[role="listitem"], ' +
                        '[role="option"], ' +
                        '[role="row"], ' +
                        '[role="button"]'
                    ) || elemento;
                    """,
                    resultado
                )

                # Asegurar que la fila esté visible antes del clic.
                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    fila_contacto
                )

                try:
                    fila_contacto.click()

                except WebDriverException:
                    self.driver.execute_script(
                        "arguments[0].click();",
                        fila_contacto
                    )

                print(
                    f"[WHATSAPP_DEBUG] Se hizo clic en la fila de "
                    f"{nombre_real!r}"
                )

            except Exception as e:
                print(
                    f"[WHATSAPP_DEBUG] No se pudo abrir la fila "
                    f"del contacto: {e!r}"
                )

                return (
                    f"Encontré a '{nombre_real}', pero no pude "
                    "abrir su chat. No se envió el mensaje."
                )

            # PASO 5: Confirmar el encabezado del chat.
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: self._chat_abierto(d, nombre_real)
                )

            except TimeoutException:
                try:
                    datos_cabecera = self.driver.execute_script(
                        """
                        return Array.from(
                            document.querySelectorAll(
                                '#main header [title], ' +
                                '#main header span[dir="auto"], ' +
                                '#main header [data-testid]'
                            )
                        )
                        .filter(e =>
                            e.offsetWidth > 0 &&
                            e.offsetHeight > 0
                        )
                        .map(e => ({
                            titulo: e.getAttribute('title'),
                            texto: (e.innerText || e.textContent || '').trim(),
                            aria: e.getAttribute('aria-label'),
                            testid: e.getAttribute('data-testid')
                        }));
                        """
                    )

                    print(
                        "[WHATSAPP_DEBUG] URL actual:",
                        self.driver.current_url
                    )

                    print(
                        "[WHATSAPP_DEBUG] Datos de la cabecera:",
                        datos_cabecera
                    )

                except Exception as e:
                    print(
                        "[WHATSAPP_DEBUG] Error inspeccionando "
                        f"la cabecera: {e!r}"
                    )

                return (
                    f"Localicé '{nombre_real}', pero no pude "
                    "confirmar que se abrió su chat. "
                    "No se envió el mensaje."
                )
            
            # PASO 6: Encontrar el editor del mensaje.
            try:
                caja_mensaje = WebDriverWait(
                    self.driver, 10
                ).until(
                    lambda d: self._encontrar_caja_mensaje(d)
                    or False
                )

            except TimeoutException:
                return (
                    "El chat está abierto, pero no encontré "
                    "la caja para escribir el mensaje."
                )

            # PASO 7: Escribir el contenido.
            caja_mensaje.click()

            # Conservar saltos de línea sin enviar antes
            # de tiempo el mensaje.
            lineas = mensaje.split("\n")

            for indice, linea in enumerate(lineas):
                if linea:
                    caja_mensaje.send_keys(linea)

                if indice < len(lineas) - 1:
                    caja_mensaje.send_keys(
                        Keys.SHIFT, Keys.ENTER
                    )

            # PASO 8: Enviar.
            caja_mensaje.send_keys(Keys.ENTER)

            print(
                f"[WHATSAPP_DEBUG] Se solicitó el envío "
                f"del mensaje a {nombre_real!r}."
            )

            return f"Mensaje enviado a {nombre_real}."

        except Exception as e:
            print(
                f"[WHATSAPP] Error general al enviar "
                f"el mensaje: {e!r}"
            )

            return (
                "Ocurrió un error inesperado al intentar "
                "enviar el mensaje. Revisa la terminal."
            )

    # ---------------------------------------------------------
    # LEER MENSAJES NO LEIDOS
    # ---------------------------------------------------------

    def leer_no_leidos(self):
        if not self._abrir_o_enfocar_whatsapp():
            return (
                "No pude cargar WhatsApp Web.",
                "Abre WhatsApp en Brave e inicia sesión."
            )

        try:
            chats_no_leidos = self.driver.find_elements(
                By.XPATH,
                "//span[contains(@aria-label, 'no leíd') "
                "or contains(@aria-label, 'unread')]"
            )

            if not chats_no_leidos:
                return (
                    "No tienes mensajes nuevos.",
                    "No tienes mensajes nuevos en WhatsApp."
                )

            resumen_consola = []
            resumen_voz = []

            for badge in chats_no_leidos:
                try:
                    fila_chat = badge.find_element(
                        By.XPATH,
                        "./ancestor::*["
                        "@role='listitem' or @role='row'"
                        "][1]"
                    )

                    nombre_elemento = fila_chat.find_element(
                        By.XPATH, ".//span[@title]"
                    )

                    nombre = (
                        nombre_elemento.get_attribute("title")
                        or "Contacto desconocido"
                    )

                    texto_fila = fila_chat.text.split("\n")

                    mensaje_previo = (
                        "Mensaje multimedia o ilegible"
                    )

                    if len(texto_fila) >= 2:
                        candidatos = [
                            texto
                            for texto in texto_fila
                            if (
                                texto != nombre
                                and not texto.replace(
                                    ":", ""
                                ).isdigit()
                                and "no leíd" not in texto.lower()
                                and "unread" not in texto.lower()
                            )
                        ]

                        if candidatos:
                            mensaje_previo = candidatos[-1]

                    cantidad = (
                        badge.get_attribute("aria-label")
                        or "mensaje no leído"
                    )

                    resumen_consola.append(
                        f"📩 {nombre} ({cantidad}): "
                        f"{mensaje_previo}"
                    )

                    resumen_voz.append(
                        f"Tienes {cantidad} de {nombre}, "
                        f"que dice: {mensaje_previo}."
                    )

                except Exception as e:
                    print(
                        "[WHATSAPP_DEBUG] No se pudo extraer "
                        f"el detalle de un chat: {e!r}"
                    )

            if resumen_consola:
                texto = (
                    "Tus mensajes nuevos son:\n\n"
                    + "\n".join(resumen_consola)
                )

                voz = " ".join(resumen_voz)

                return texto, voz

            return (
                "Detecté notificaciones, pero no logré "
                "leer sus detalles.",
                "Detecté notificaciones, pero no pude "
                "extraer el contenido."
            )

        except Exception as e:
            print(
                f"[WHATSAPP] Error al leer mensajes: {e!r}"
            )

            return (
                "Ocurrió un error al buscar mensajes no leídos.",
                "Hubo un problema al revisar los mensajes."
            )

    # ---------------------------------------------------------
    # CERRAR LA CONEXION DE SELENIUM
    # ---------------------------------------------------------

    def cerrar(self):
        if self.driver is not None:
            try:
                # Detener ChromeDriver sin enviar el comando quit
                # que puede cerrar la sesión de Brave conectada.
                self.driver.service.stop()

            except Exception:
                pass

            self.driver = None
