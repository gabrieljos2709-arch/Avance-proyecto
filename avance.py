"""Biblioteca escolar digital - Primer avance (Fundamentos de Programación I).

Implementado: catálogo con listas paralelas, validaciones, código automático,
listado, ordenamiento por inserción, búsqueda por código (binaria) y título (lineal).
Pendiente: préstamos, devoluciones y almacenamiento permanente.
"""
import unicodedata


def nuevo_catalogo():
    # Las posiciones equivalentes describen un mismo libro.
    return {"cod": [], "tit": [], "aut": [], "cat": [], "stk": []}


def validar_texto(texto):
    texto = " ".join(texto.strip().split())
    if not texto or "|" in texto:
        return None
    return texto


def validar_cantidad(dato):
    if dato.isdigit():
        numero = int(dato)
        if 1 <= numero <= 50:
            return numero
    return None


def validar_codigo(codigo):
    codigo = codigo.strip().upper()
    if len(codigo) == 7 and codigo[:4] == "LIB-" and codigo[4:].isdigit():
        return codigo
    return None


def buscar_lineal_codigo(catalogo, codigo):
    for i in range(len(catalogo["cod"])):
        if catalogo["cod"][i] == codigo:
            return i
    return -1


def siguiente_codigo(catalogo):
    mayor = 0
    for codigo in catalogo["cod"]:
        numero = int(codigo[4:])
        if numero > mayor:
            mayor = numero
    if mayor >= 999:
        return None
    return "LIB-" + str(mayor + 1).zfill(3)


def registrar_libro(catalogo):
    print("\n--- REGISTRAR LIBRO ---")
    codigo = siguiente_codigo(catalogo)
    if codigo is None:
        print("No hay códigos LIB-### disponibles.")
        return
    titulo = validar_texto(input("Título: "))
    autor = validar_texto(input("Autor: "))
    categoria = validar_texto(input("Categoría: "))
    cantidad = validar_cantidad(input("Ejemplares (1 a 50): ").strip())

    if titulo is None or autor is None or categoria is None:
        print("Error: título, autor y categoría deben tener texto válido (sin '|').")
        return
    if cantidad is None:
        print("Error: la cantidad debe ser un entero entre 1 y 50.")
        return
    if buscar_lineal_codigo(catalogo, codigo) != -1:
        print("Error: código duplicado.")
        return

    catalogo["cod"].append(codigo)
    catalogo["tit"].append(titulo)
    catalogo["aut"].append(autor)
    catalogo["cat"].append(categoria)
    catalogo["stk"].append(cantidad)
    print("Libro registrado correctamente. Código generado:", codigo)


def mostrar_libro(catalogo, i):
    print(catalogo["cod"][i], "|", catalogo["tit"][i], "|",
          catalogo["aut"][i], "|", catalogo["cat"][i], "| Disponibles:",
          catalogo["stk"][i])


def mostrar_catalogo(catalogo):
    print("\n--- CATÁLOGO ---")
    if not catalogo["cod"]:
        print("Todavía no hay libros registrados.")
        return
    for i in range(len(catalogo["cod"])):
        mostrar_libro(catalogo, i)


def clave_orden(texto):
    texto = unicodedata.normalize("NFD", texto)
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn").lower()


def ordenar_catalogo(catalogo, criterio):
    # Inserción: mover todos los campos juntos para evitar mezclar libros.
    for i in range(1, len(catalogo["cod"])):
        fila = {campo: catalogo[campo][i] for campo in catalogo}
        j = i - 1
        while j >= 0 and clave_orden(catalogo[criterio][j]) > clave_orden(fila[criterio]):
            for campo in catalogo:
                catalogo[campo][j + 1] = catalogo[campo][j]
            j -= 1
        for campo in catalogo:
            catalogo[campo][j + 1] = fila[campo]


def buscar_binaria(catalogo, codigo):
    inicio = 0
    fin = len(catalogo["cod"]) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if catalogo["cod"][medio] == codigo:
            return medio
        elif catalogo["cod"][medio] < codigo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1


def buscar_por_codigo(catalogo):
    codigo = validar_codigo(input("Código (ejemplo LIB-001): "))
    if codigo is None:
        print("Formato inválido. Utilice LIB-001.")
        return
    ordenar_catalogo(catalogo, "cod")  # requisito de búsqueda binaria
    posicion = buscar_binaria(catalogo, codigo)
    if posicion == -1:
        print("Libro no encontrado.")
    else:
        mostrar_libro(catalogo, posicion)


def buscar_por_titulo(catalogo):
    texto = validar_texto(input("Parte del título: "))
    if texto is None:
        print("Ingrese un texto válido.")
        return
    encontrados = 0
    for i in range(len(catalogo["tit"])):
        if clave_orden(texto) in clave_orden(catalogo["tit"][i]):
            mostrar_libro(catalogo, i)
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron coincidencias.")


def menu():
    catalogo = nuevo_catalogo()
    while True:
        print("\n========= BIBLIOTECA ESCOLAR =========")
        print("1. Registrar libro")
        print("2. Mostrar catálogo")
        print("3. Ordenar catálogo")
        print("4. Buscar por código")
        print("5. Buscar por título")
        print("6. Registrar préstamo [PENDIENTE]")
        print("7. Registrar devolución [PENDIENTE]")
        print("8. Préstamos de estudiante [PENDIENTE]")
        print("9. Préstamos vencidos [PENDIENTE]")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_libro(catalogo)
        elif opcion == "2":
            mostrar_catalogo(catalogo)
        elif opcion == "3":
            criterio = input("Ordenar por 1) código o 2) título: ").strip()
            if criterio in ("1", "2"):
                ordenar_catalogo(catalogo, "cod" if criterio == "1" else "tit")
                print("Catálogo ordenado.")
                mostrar_catalogo(catalogo)
            else:
                print("Criterio inválido.")
        elif opcion == "4":
            buscar_por_codigo(catalogo)
        elif opcion == "5":
            buscar_por_titulo(catalogo)
        elif opcion in ("6", "7", "8", "9"):
            print("Esta opción se implementará en la siguiente etapa.")
        elif opcion == "0":
            print("Fin del avance. Los datos de esta versión no se guardan al cerrar.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu()
