"""Configuración general del sistema de biblioteca."""
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA_PROYECTO / "datos"
ARCHIVO_LIBROS = CARPETA_DATOS / "libros.txt"
ARCHIVO_PRESTAMOS = CARPETA_DATOS / "prestamos.txt"

MAX_CODIGO_LIBRO = 999
MAX_ID_PRESTAMO = 999
MAX_CANTIDAD_INGRESO = 50
MAX_PRESTAMOS_ACTIVOS = 2
DIAS_PRESTAMO = 7

ESTADO_PRESTADO = "PRESTADO"
ESTADO_DEVUELTO = "DEVUELTO"

# Posiciones de cada campo dentro de una fila de préstamos.
P_ID = 0
P_DNI = 1
P_NOMBRE = 2
P_CODIGO = 3
P_FECHA_PRESTAMO = 4
P_FECHA_LIMITE = 5
P_ESTADO = 6
TOTAL_CAMPOS_PRESTAMO = 7
