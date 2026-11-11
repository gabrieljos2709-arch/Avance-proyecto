"""Sistema de Biblioteca Escolar Digital.
"""
from almacenamiento import cargar_todo
from interfaz import iniciar_aplicacion


def main():
    catalogo, prestamos = cargar_todo()
    iniciar_aplicacion(catalogo, prestamos)


if __name__ == "__main__":
    main()
