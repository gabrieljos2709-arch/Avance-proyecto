"""Funciones de validación y limpieza de datos."""


def validar_texto(texto):
    """Limpia espacios y rechaza textos vacíos o con el separador de archivos."""
    if texto is None:
        return None
    texto = " ".join(str(texto).strip().split())
    if not texto or "|" in texto or "\n" in texto or "\r" in texto:
        return None
    return texto


def validar_dni(dni):
    dni = str(dni).strip()
    if len(dni) == 8 and all("0" <= digito <= "9" for digito in dni):
        return dni
    return None


def validar_codigo(codigo):
    codigo = str(codigo).strip().upper()
    if (len(codigo) == 7 and codigo.startswith("LIB-")
            and all("0" <= digito <= "9" for digito in codigo[4:])):
        return codigo
    return None


def validar_cantidad(dato, minimo=1, maximo=50):
    dato = str(dato).strip()
    if dato.isdecimal():
        numero = int(dato)
        if minimo <= numero <= maximo:
            return numero
    return None


def validar_id_prestamo(identificador):
    identificador = str(identificador).strip().upper()
    if (len(identificador) == 6 and identificador.startswith("PR-")
            and all("0" <= digito <= "9" for digito in identificador[3:])):
        return identificador
    return None
