"""Operaciones del catálogo usando cinco listas paralelas."""
from config import MAX_CODIGO_LIBRO
from validaciones import validar_texto, validar_cantidad, validar_codigo


def nuevo_catalogo():
    return {"cod": [], "tit": [], "aut": [], "cat": [], "stk": []}


def catalogo_consistente(catalogo):
    longitudes = [len(catalogo[campo]) for campo in catalogo]
    return len(set(longitudes)) <= 1


def buscar_lineal_codigo(catalogo, codigo):
    for i, codigo_actual in enumerate(catalogo["cod"]):
        if codigo_actual == codigo:
            return i
    return -1


def siguiente_codigo(catalogo):
    mayor = 0
    for codigo in catalogo["cod"]:
        if validar_codigo(codigo):
            numero = int(codigo[4:])
            mayor = max(mayor, numero)

    if mayor >= MAX_CODIGO_LIBRO:
        return None
    return "LIB-" + str(mayor + 1).zfill(3)


def registrar_libro(catalogo, titulo, autor, categoria, cantidad):
    titulo = validar_texto(titulo)
    autor = validar_texto(autor)
    categoria = validar_texto(categoria)
    cantidad = validar_cantidad(cantidad)

    if not catalogo_consistente(catalogo):
        return False, "El catálogo tiene datos desalineados.", None
    if None in (titulo, autor, categoria, cantidad):
        return False, "Verifique los datos: textos obligatorios y cantidad de 1 a 50.", None

    codigo = siguiente_codigo(catalogo)
    if codigo is None:
        return False, "Se alcanzó el límite de códigos LIB-999.", None
    if buscar_lineal_codigo(catalogo, codigo) != -1:
        return False, "El código generado ya existe. Revise el catálogo.", None

    catalogo["cod"].append(codigo)
    catalogo["tit"].append(titulo)
    catalogo["aut"].append(autor)
    catalogo["cat"].append(categoria)
    catalogo["stk"].append(cantidad)

    return True, "Libro registrado correctamente.", codigo


def actualizar_stock(catalogo, codigo, cantidad):
    codigo = validar_codigo(codigo)
    cantidad = validar_cantidad(cantidad)

    if codigo is None or cantidad is None:
        return False, "Código o cantidad inválidos."

    posicion = buscar_lineal_codigo(catalogo, codigo)
    if posicion == -1:
        return False, "No existe un libro con ese código."

    catalogo["stk"][posicion] += cantidad
    return True, "Stock actualizado correctamente."


def editar_libro(catalogo, codigo, titulo, autor, categoria, stock):
    """Actualiza los datos descriptivos y el stock de un libro existente.

    El código se conserva para no alterar las referencias de los préstamos.
    El stock disponible puede ser 0, por ejemplo cuando no quedan ejemplares.
    """
    codigo = validar_codigo(codigo)
    titulo = validar_texto(titulo)
    autor = validar_texto(autor)
    categoria = validar_texto(categoria)
    stock = validar_cantidad(stock, minimo=0)

    if not catalogo_consistente(catalogo):
        return False, "El catálogo tiene datos desalineados."
    if codigo is None:
        return False, "El código del libro no tiene un formato válido."
    if None in (titulo, autor, categoria, stock):
        return False, "Revise los datos. El stock debe ser un número entre 0 y 50."

    posicion = buscar_lineal_codigo(catalogo, codigo)
    if posicion == -1:
        return False, "No existe un libro con ese código."

    catalogo["tit"][posicion] = titulo
    catalogo["aut"][posicion] = autor
    catalogo["cat"][posicion] = categoria
    catalogo["stk"][posicion] = stock
    return True, f"Libro {codigo} actualizado correctamente."


def eliminar_libro(catalogo, codigo, prestamos):
    """Elimina un libro si no tiene referencias en el historial de préstamos.

    Se conserva el historial íntegro: no se permite borrar libros que hayan
    sido prestados alguna vez, aunque el préstamo ya esté devuelto.
    """
    from config import P_CODIGO

    codigo = validar_codigo(codigo)
    if not catalogo_consistente(catalogo):
        return False, "El catálogo tiene datos desalineados."
    if codigo is None:
        return False, "El código del libro no tiene un formato válido."

    posicion = buscar_lineal_codigo(catalogo, codigo)
    if posicion == -1:
        return False, "No existe un libro con ese código."

    tiene_historial = any(
        len(fila) > P_CODIGO and fila[P_CODIGO] == codigo
        for fila in prestamos
    )
    if tiene_historial:
        return False, (
            "No se puede eliminar: el libro aparece en el historial de préstamos. "
            "Puede editar sus datos, pero debe conservarse su registro."
        )

    for campo in ("cod", "tit", "aut", "cat", "stk"):
        catalogo[campo].pop(posicion)

    return True, f"Libro {codigo} eliminado correctamente del catálogo."
