"""Operaciones de fechas para préstamos y devoluciones."""
from datetime import date, timedelta
from config import DIAS_PRESTAMO


def fecha_actual():
    return date.today()


def convertir_fecha(texto):
    try:
        return date.fromisoformat(texto)
    except (TypeError, ValueError):
        return None


def fecha_limite(fecha_inicio=None):
    if fecha_inicio is None:
        fecha_inicio = fecha_actual()
    return (fecha_inicio + timedelta(days=DIAS_PRESTAMO)).isoformat()


def calcular_dias_retraso(fecha_tope, fecha_devolucion=None):
    limite = convertir_fecha(fecha_tope)
    if limite is None:
        return 0
    if fecha_devolucion is None:
        fecha_devolucion = fecha_actual()
    return max((fecha_devolucion - limite).days, 0)


def esta_vencido(fecha_tope, fecha_referencia=None):
    limite = convertir_fecha(fecha_tope)
    if limite is None:
        return False
    if fecha_referencia is None:
        fecha_referencia = fecha_actual()
    return limite < fecha_referencia
