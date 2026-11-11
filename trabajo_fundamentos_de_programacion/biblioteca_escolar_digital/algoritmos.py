"""Algoritmos de ordenamiento y búsqueda del catálogo."""
import unicodedata


def clave_orden(texto):
    texto = unicodedata.normalize("NFD", str(texto))
    sin_tildes = "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )
    return sin_tildes.lower()


def ordenar_catalogo(catalogo, criterio):
    """Ordena por inserción y mueve juntas las cinco listas paralelas."""
    if criterio not in ("cod", "tit"):
        return False

    campos = list(catalogo.keys())
    for i in range(1, len(catalogo[criterio])):
        fila = [catalogo[campo][i] for campo in campos]
        clave = clave_orden(fila[campos.index(criterio)])
        j = i - 1

        while j >= 0 and clave_orden(catalogo[criterio][j]) > clave:
            for campo in campos:
                catalogo[campo][j + 1] = catalogo[campo][j]
            j -= 1

        for indice, campo in enumerate(campos):
            catalogo[campo][j + 1] = fila[indice]

    return True


def buscar_binaria(catalogo, codigo):
    """Busca un código. El catálogo debe estar ordenado por código."""
    inicio = 0
    fin = len(catalogo["cod"]) - 1

    while inicio <= fin:
        medio = (inicio + fin) // 2
        actual = catalogo["cod"][medio]

        if actual == codigo:
            return medio
        if actual < codigo:
            inicio = medio + 1
        else:
            fin = medio - 1

    return -1


def buscar_por_titulo(catalogo, texto):
    """Búsqueda lineal por coincidencia parcial, ignorando tildes."""
    texto = clave_orden(texto)
    encontrados = []

    for i, titulo in enumerate(catalogo["tit"]):
        if texto in clave_orden(titulo):
            encontrados.append(i)

    return encontrados
