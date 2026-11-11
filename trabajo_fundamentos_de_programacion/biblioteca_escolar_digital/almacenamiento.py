"""Lectura y escritura de los archivos de texto de la biblioteca."""
from config import (CARPETA_DATOS, ARCHIVO_LIBROS, ARCHIVO_PRESTAMOS,
                    P_ID, P_DNI, P_NOMBRE, P_CODIGO, P_FECHA_PRESTAMO,
                    P_FECHA_LIMITE, P_ESTADO, TOTAL_CAMPOS_PRESTAMO,
                    ESTADO_PRESTADO, ESTADO_DEVUELTO)
from catalogo import nuevo_catalogo, buscar_lineal_codigo
from validaciones import validar_texto, validar_dni, validar_codigo, validar_id_prestamo
from fechas import convertir_fecha


def preparar_archivos():
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    ARCHIVO_LIBROS.touch(exist_ok=True)
    ARCHIVO_PRESTAMOS.touch(exist_ok=True)


def cargar_catalogo():
    catalogo = nuevo_catalogo()
    preparar_archivos()

    with ARCHIVO_LIBROS.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.rstrip("\n").split("|")
            if len(partes) != 5:
                continue

            codigo = validar_codigo(partes[0])
            titulo = validar_texto(partes[1])
            autor = validar_texto(partes[2])
            categoria = validar_texto(partes[3])
            try:
                stock = int(partes[4])
            except ValueError:
                continue

            if (codigo is None or titulo is None or autor is None
                    or categoria is None or stock < 0
                    or buscar_lineal_codigo(catalogo, codigo) != -1):
                continue

            catalogo["cod"].append(codigo)
            catalogo["tit"].append(titulo)
            catalogo["aut"].append(autor)
            catalogo["cat"].append(categoria)
            catalogo["stk"].append(stock)

    return catalogo


def cargar_prestamos():
    prestamos = []
    preparar_archivos()

    with ARCHIVO_PRESTAMOS.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.rstrip("\n").split("|")
            if len(partes) != TOTAL_CAMPOS_PRESTAMO:
                continue

            identificador = validar_id_prestamo(partes[P_ID])
            dni = validar_dni(partes[P_DNI])
            nombre = validar_texto(partes[P_NOMBRE])
            codigo = validar_codigo(partes[P_CODIGO])
            fecha_inicio = convertir_fecha(partes[P_FECHA_PRESTAMO])
            fecha_tope = convertir_fecha(partes[P_FECHA_LIMITE])
            estado = partes[P_ESTADO]

            if (identificador is None or dni is None or nombre is None
                    or codigo is None or fecha_inicio is None or fecha_tope is None
                    or estado not in (ESTADO_PRESTADO, ESTADO_DEVUELTO)):
                continue

            prestamos.append([identificador, dni, nombre, codigo,
                              fecha_inicio.isoformat(), fecha_tope.isoformat(), estado])

    return prestamos


def guardar_catalogo(catalogo):
    preparar_archivos()
    with ARCHIVO_LIBROS.open("w", encoding="utf-8") as archivo:
        for i in range(len(catalogo["cod"])):
            fila = [catalogo[campo][i] for campo in ("cod", "tit", "aut", "cat", "stk")]
            archivo.write("|".join(str(valor) for valor in fila) + "\n")


def guardar_prestamos(prestamos):
    preparar_archivos()
    with ARCHIVO_PRESTAMOS.open("w", encoding="utf-8") as archivo:
        for fila in prestamos:
            archivo.write("|".join(str(valor) for valor in fila) + "\n")


def guardar_todo(catalogo, prestamos):
    guardar_catalogo(catalogo)
    guardar_prestamos(prestamos)


def cargar_todo():
    return cargar_catalogo(), cargar_prestamos()
