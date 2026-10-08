def mostrar_bienvenida():

    print("=" * 60)
    print("NIVY - SISTEMA EXPERTO")
    print("=" * 60)
    print("Escribe una instrucción. Ejemplos:")
    print("  • ¿Qué hora es?")
    print("  • ¿Qué fecha es?")
    print("  • Reproduce Electronica")
    print("  • Reproduce bajo")
    print("  • Siguiente canción")
    print("  • Canción anterior")
    print("  • ¿Qué estoy escuchando?")
    print("  • Abre YouTube")
    print("  • Dame las noticias")
    print("  • Busca en internet inteligencia artificial")
    print("  • ayuda")
    print("Escribe 'salir' para terminar.")
    print("=" * 60)


def leer_comando():

    return input(
        "\nTú > "
    ).strip()


def responder(texto):

    print(
        f"NIVY > {texto}"
    )