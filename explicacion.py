def generar_explicacion(resultado):
    if resultado is None:
        return "NIVY no encontró una regla que coincida con la solicitud."

    regla = resultado["regla"]
    return (
        f"NIVY analizó la entrada y activó la regla {regla['id']}: "
        f"{regla['nombre']}. La acción seleccionada fue '{regla['accion']}'."
    )
