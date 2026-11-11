"""Registro, devolución y consultas de préstamos."""
from datetime import date
from config import (P_ID, P_DNI, P_NOMBRE, P_CODIGO, P_FECHA_PRESTAMO,
                    P_FECHA_LIMITE, P_ESTADO, MAX_PRESTAMOS_ACTIVOS, MAX_ID_PRESTAMO,
                    ESTADO_PRESTADO, ESTADO_DEVUELTO)
from validaciones import validar_dni, validar_texto, validar_codigo, validar_id_prestamo
from fechas import fecha_actual, fecha_limite, calcular_dias_retraso, esta_vencido


def buscar_posicion_libro(catalogo, codigo):
    for i, codigo_actual in enumerate(catalogo["cod"]):
        if codigo_actual == codigo:
            return i
    return -1


def siguiente_id_prestamo(prestamos):
    mayor = 0
    for fila in prestamos:
        identificador = fila[P_ID]
        if identificador.startswith("PR-") and identificador[3:].isdigit():
            mayor = max(mayor, int(identificador[3:]))
    if mayor >= MAX_ID_PRESTAMO:
        return None
    return "PR-" + str(mayor + 1).zfill(3)


def registrar_prestamo(catalogo, prestamos, dni, nombre, codigo, hoy=None):
    dni = validar_dni(dni)
    nombre = validar_texto(nombre)
    codigo = validar_codigo(codigo)

    if dni is None:
        return False, "El DNI debe tener exactamente 8 dígitos.", None
    if nombre is None or codigo is None:
        return False, "Nombre o código de libro inválidos.", None

    posicion = buscar_posicion_libro(catalogo, codigo)
    if posicion == -1:
        return False, "El libro no existe en el catálogo.", None
    if catalogo["stk"][posicion] <= 0:
        return False, "No hay ejemplares disponibles.", None

    activos = [fila for fila in prestamos
               if fila[P_DNI] == dni and fila[P_ESTADO] == ESTADO_PRESTADO]
    if len(activos) >= MAX_PRESTAMOS_ACTIVOS:
        return False, "El estudiante ya tiene 2 préstamos activos.", None

    if any(fila[P_DNI] == dni and fila[P_CODIGO] == codigo
           and fila[P_ESTADO] == ESTADO_PRESTADO for fila in prestamos):
        return False, "El estudiante ya tiene este libro prestado.", None

    if hoy is None:
        hoy = fecha_actual()
    identificador = siguiente_id_prestamo(prestamos)
    if identificador is None:
        return False, "Se alcanzó el límite de identificadores PR-999.", None
    fecha_inicio = hoy.isoformat()
    limite = fecha_limite(hoy)
    fila = [identificador, dni, nombre, codigo, fecha_inicio, limite, ESTADO_PRESTADO]

    prestamos.append(fila)
    catalogo["stk"][posicion] -= 1
    return True, f"Préstamo {identificador} registrado. Devolver hasta el {limite}.", identificador


def devolver_prestamo(catalogo, prestamos, identificador, hoy=None):
    identificador = validar_id_prestamo(identificador)
    if identificador is None:
        return False, "El ID debe tener el formato PR-001.", None

    fila = None
    for prestamo in prestamos:
        if prestamo[P_ID] == identificador:
            fila = prestamo
            break

    if fila is None:
        return False, "No se encontró ese préstamo.", None
    if fila[P_ESTADO] == ESTADO_DEVUELTO:
        return False, "Este préstamo ya fue devuelto.", None

    posicion = buscar_posicion_libro(catalogo, fila[P_CODIGO])
    if posicion == -1:
        return False, "No se encontró el libro asociado; no se modificó el préstamo.", None

    if hoy is None:
        hoy = fecha_actual()
    retraso = calcular_dias_retraso(fila[P_FECHA_LIMITE], hoy)
    fila[P_ESTADO] = ESTADO_DEVUELTO
    catalogo["stk"][posicion] += 1

    if retraso > 0:
        mensaje = f"Devolución registrada con {retraso} día(s) de retraso."
    else:
        mensaje = "Devolución registrada dentro del plazo."
    return True, mensaje, retraso


def prestamos_de_estudiante(prestamos, dni):
    dni = validar_dni(dni)
    if dni is None:
        return None
    return [fila for fila in prestamos if fila[P_DNI] == dni]


def prestamos_vencidos(prestamos, hoy=None):
    if hoy is None:
        hoy = fecha_actual()
    return [fila for fila in prestamos
            if fila[P_ESTADO] == ESTADO_PRESTADO
            and esta_vencido(fila[P_FECHA_LIMITE], hoy)]


def prestamos_activos(prestamos):
    return [fila for fila in prestamos if fila[P_ESTADO] == ESTADO_PRESTADO]
