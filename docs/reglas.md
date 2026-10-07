# Reglas de NIVY

NIVY utiliza reglas de producción de la forma:

**SI** se cumple una condición  
**ENTONCES** se ejecuta una acción.

Ejemplo:

- SI el usuario dice "qué hora es"
- ENTONCES ejecutar la acción `hora`.

## Reglas iniciales

| ID | Regla | Acción |
|---|---|---|
| R001 | Consultar la hora | hora |
| R002 | Consultar la fecha | fecha |
| R003 | Reproducir playlist | reproducir_playlist |
| R004 | Abrir YouTube | youtube |
| R005 | Consultar noticias | noticias |
| R006 | Buscar en internet | buscar |
| R007 | Mostrar ayuda | ayuda |

El sistema usa prioridad para resolver coincidencias cuando una entrada puede activar más de una regla.
