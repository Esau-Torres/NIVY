# Asistente Personal Inteligente (Sistema Experto)

## Descripción
Este proyecto es un **Sistema Experto** diseñado para actuar como un asistente personal integral. Su objetivo es automatizar y facilitar tareas básicas del día a día, gestionando tu entorno digital, comunicaciones y hardware mediante comandos de voz o texto.

## ✨ Funcionalidades Principales
El asistente está capacitado para realizar las siguientes tareas:

### 🌐 Información y Entretenimiento
* 🔍 **Búsquedas en Internet:** Realiza consultas en la web y extrae la información más relevante.
* 📰 **Noticias:** Te mantiene informado leyendo los titulares y noticias más recientes.
* 🎵 **Música en YouTube:** Reproduce tus canciones, playlists o artistas favoritos directamente en YouTube.
* 📅 **Fecha, Hora y Clima:** Te informa de la fecha, hora actual y el estado del tiempo en tu ubicación.

### 📱 Comunicación y Productividad
* 💬 **WhatsApp:** Envía mensajes a tus contactos y lee automáticamente tus mensajes no leídos.
* 🎙️⌨️ **Modos de Interacción:** Cambia dinámicamente entre **modo voz** (interacción por micrófono) y **modo texto** (escribir comandos en la consola).

### 🩺 Mantenimiento
* 💻 **Diagnóstico de PC:** Detecta problemas de rendimiento, como falta de memoria RAM, cuando tu computadora se vuelve lenta.

---

## ⚙️ Configuración del Navegador (Requisito Indispensable)

Para que el sistema experto pueda controlar el navegador, abrir pestañas y reproducir contenido (como música en YouTube o búsquedas), es necesario iniciar tu navegador en **modo de depuración remota** desde la consola de comandos (CMD o PowerShell). 

### 🚀 Cómo iniciar el navegador remoto
Dependiendo del navegador que utilices, debes ejecutar el siguiente comando en tu terminal **antes** de iniciar el asistente. 

**Ejemplo para Brave Browser:**
```cmd
"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222
```
*(Nota: Si usas Chrome, Edge u otro, asegúrate de cambiar la ruta de ejecución y mantener el parámetro `--remote-debugging-port=9222`)*.

---

## 🏃 Ejecución del Programa

Una vez que el navegador remoto está corriendo en segundo plano, puedes iniciar el sistema experto.

Abre tu terminal en el directorio raíz del proyecto y ejecuta:

```bash
python main.py
```

---

## 🧪 Ejecución de Pruebas (Tests)

El proyecto cuenta con pruebas unitarias para validar las reglas del sistema experto y su funcionamiento general. Para ejecutar los tests, utiliza los siguientes comandos:

**Para probar las reglas de reconocimiento:**
```bash
python -m unittest test/test_reglas.py
```

**Para probar el sistema experto en general:**
```bash
python -m unittest tests/test_sistema_experto.py
```

---

## 💡 Ejemplos de uso
Una vez iniciado el programa, puedes interactuar con él usando frases naturales como:

**Modos y Sistema:**
* *"Cambiar a modo texto"* / *"Cambiar a modo voz"*

**WhatsApp:**
* *"Envía un mensaje a Juan que diga que llegaré tarde"*
* *"Lee mis mensajes de WhatsApp"* / *"¿Tengo mensajes no leídos?"*

**Tareas Básicas:**
* *"¿Qué hora es?"* / *"¿Cómo está el clima hoy?"*
* *"Busca información sobre la inteligencia artificial"*
* *"Pon las noticias de tecnología"*
* *"Reproduce música de Lo-Fi en YouTube"*

---
*Desarrollado como un Sistema Experto de Asistencia Personal.*

## Reglas agregadas en el Parcial 2

```bash
{
      "id": "R021",
      "nombre": "Recomendación por lluvia",
      "prioridad": 95,
      "patrones": [
        "\\b¿esta lloviendo?\\b",
        "\\bnecesito paraguas\\b",
        "\\bclima lluvioso\\b",
        "\\bva a llover\\b",
        "\\bcomo esta el clima de lluvia\\b"
      ],
      "accion": "consejo_lluvia",
      "respuesta": "Detecto condiciones de lluvia. Te recomiendo llevar paraguas, usar calzado impermeable y conducir con precaución en las calles."
    },
    {
      "id": "R022",
      "nombre": "Recomendación por clima soleado",
      "prioridad": 95,
      "patrones": [
        "\\bhace mucho sol\\b",
        "\\bclima soleado\\b",
        "\\bnecesito bloqueador\\b",
        "\\besta muy caluroso\\b",
        "\\bcomo esta el clima de sol\\b"
      ],
      "accion": "consejo_sol",
      "respuesta": "El clima está soleado y caluroso. Te recomiendo aplicar bloqueador solar, mantener una buena hidratación y evitar la exposición prolongada al sol."
    }
```