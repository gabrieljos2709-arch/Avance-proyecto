"""Prepara filas de datos para mostrar catálogos y reportes en la interfaz."""
from config import (
    P_ID, P_DNI, P_NOMBRE, P_CODIGO,
    P_FECHA_PRESTAMO, P_FECHA_LIMITE, P_ESTADO,
)
from fechas import calcular_dias_retraso
from prestamos import prestamos_vencidos


def filas_catalogo(catalogo):
    """Devuelve los libros como filas listas para una tabla."""
    return [
        (catalogo["cod"][i], catalogo["tit"][i], catalogo["aut"][i],
         catalogo["cat"][i], catalogo["stk"][i])
        for i in range(len(catalogo["cod"]))
    ]


def fila_prestamo(prestamo):
    """Devuelve los campos principales de un préstamo."""
    return tuple(prestamo[indice] for indice in (
        P_ID, P_DNI, P_NOMBRE, P_CODIGO,
        P_FECHA_PRESTAMO, P_FECHA_LIMITE, P_ESTADO
    ))


def filas_prestamos(prestamos):
    """Devuelve el historial como filas listas para una tabla."""
    return [fila_prestamo(prestamo) for prestamo in prestamos]


def filas_vencidos(prestamos):
    """Devuelve préstamos vencidos e incluye sus días de retraso."""
    vencidos = prestamos_vencidos(prestamos)
    return [
        fila_prestamo(prestamo) +
        (calcular_dias_retraso(prestamo[P_FECHA_LIMITE]),)
        for prestamo in vencidos
    ]
