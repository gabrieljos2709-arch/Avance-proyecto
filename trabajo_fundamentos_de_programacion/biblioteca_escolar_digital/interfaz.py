"""Interfaz gráfica sencilla para la Biblioteca Escolar Digital.

Mantiene las operaciones del sistema en sus módulos correspondientes.
Tkinter solo se encarga de mostrar el menú, pedir datos y presentar resultados.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog

from almacenamiento import guardar_todo
from algoritmos import ordenar_catalogo, buscar_binaria, buscar_por_titulo
from catalogo import (
    registrar_libro, actualizar_stock, editar_libro, eliminar_libro,
    buscar_lineal_codigo,
)
from prestamos import (
    registrar_prestamo,
    devolver_prestamo,
    prestamos_de_estudiante,
    prestamos_vencidos,
    prestamos_activos,
)
from validaciones import validar_codigo, validar_dni, validar_texto
from reportes import filas_catalogo, filas_prestamos, filas_vencidos


class BibliotecaApp:
    """Ventana principal con menú de operaciones y área de resultados."""

    def __init__(self, root, catalogo, prestamos):
        self.root = root
        self.catalogo = catalogo
        self.prestamos = prestamos

        self.root.title("Biblioteca Escolar Digital")
        self.root.geometry("1000x680")
        self.root.minsize(850, 570)
        self.root.configure(bg="#f2f3f5")
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

        self._crear_interfaz()
        self.mostrar_inicio()
        self.actualizar_estado()

    # ----------------------------------------------------------
    # VENTANA Y ELEMENTOS VISUALES
    # ----------------------------------------------------------

    def _crear_interfaz(self):
        encabezado = tk.Frame(self.root, bg="#e5e8ec", height=76)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="Biblioteca Escolar Digital",
            font=("Segoe UI", 17, "bold"),
            bg="#e5e8ec",
            fg="#263445",
        ).pack(anchor="w", padx=20, pady=(13, 0))

        tk.Label(
            encabezado,
            text="Gestión de libros, préstamos y devoluciones",
            font=("Segoe UI", 9),
            bg="#e5e8ec",
            fg="#536170",
        ).pack(anchor="w", padx=21, pady=(1, 10))

        cuerpo = tk.Frame(self.root, bg="#f2f3f5")
        cuerpo.pack(fill="both", expand=True, padx=12, pady=12)

        self.panel_menu = tk.Frame(cuerpo, bg="#e9ecef", width=218)
        self.panel_menu.pack(side="left", fill="y", padx=(0, 12))
        self.panel_menu.pack_propagate(False)

        self._crear_menu_lateral()

        panel_derecho = tk.Frame(cuerpo, bg="#f2f3f5")
        panel_derecho.pack(side="left", fill="both", expand=True)

        barra_superior = tk.Frame(panel_derecho, bg="#f2f3f5")
        barra_superior.pack(fill="x", pady=(0, 7))

        tk.Label(
            barra_superior,
            text="Actividad del sistema",
            font=("Segoe UI", 11, "bold"),
            bg="#f2f3f5",
            fg="#263445",
        ).pack(side="left")

        tk.Button(
            barra_superior,
            text="Limpiar",
            command=self.limpiar_pantalla,
            font=("Segoe UI", 9),
            relief="groove",
            bd=1,
            padx=10,
            pady=3,
            bg="#ffffff",
            activebackground="#e3e7eb",
        ).pack(side="right")

        marco_salida = tk.Frame(panel_derecho, bg="#ffffff", bd=1, relief="solid")
        marco_salida.pack(fill="both", expand=True)

        self.salida = tk.Text(
            marco_salida,
            wrap="word",
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#252525",
            insertbackground="#252525",
            padx=12,
            pady=10,
            relief="flat",
            state="disabled",
        )
        barra = tk.Scrollbar(marco_salida, command=self.salida.yview)
        self.salida.configure(yscrollcommand=barra.set)
        self.salida.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        pie = tk.Frame(self.root, bg="#e5e8ec", height=30)
        pie.pack(fill="x", side="bottom")
        pie.pack_propagate(False)

        self.etiqueta_estado = tk.Label(
            pie,
            text="Sistema listo.",
            font=("Segoe UI", 8),
            bg="#e5e8ec",
            fg="#536170",
            anchor="w",
        )
        self.etiqueta_estado.pack(fill="both", padx=12)

    def _crear_menu_lateral(self):
        tk.Label(
            self.panel_menu,
            text="CATÁLOGO",
            font=("Segoe UI", 8, "bold"),
            bg="#e9ecef",
            fg="#5c6875",
        ).pack(anchor="w", padx=13, pady=(13, 5))

        opciones_catalogo = [
            ("1  Registrar libro", self.registrar_libro),
            ("2  Mostrar catálogo", self.mostrar_catalogo),
            ("3  Ordenar catálogo", self.ordenar),
            ("4  Buscar por código", self.buscar_codigo),
            ("5  Buscar por título", self.buscar_titulo),
            ("6  Aumentar ejemplares", self.aumentar_stock),
            ("7  Editar libro", self.editar_libro),
            ("8  Eliminar libro", self.eliminar_libro),
        ]
        for texto, accion in opciones_catalogo:
            self._crear_boton_menu(texto, accion)

        tk.Label(
            self.panel_menu,
            text="PRÉSTAMOS",
            font=("Segoe UI", 8, "bold"),
            bg="#e9ecef",
            fg="#5c6875",
        ).pack(anchor="w", padx=13, pady=(13, 5))

        opciones_prestamos = [
            ("9  Registrar préstamo", self.registrar_prestamo),
            ("10  Registrar devolución", self.registrar_devolucion),
            ("11  Préstamos de estudiante", self.consultar_estudiante),
            ("12  Préstamos vencidos", self.mostrar_vencidos),
            ("13  Historial de préstamos", self.mostrar_historial),
        ]
        for texto, accion in opciones_prestamos:
            self._crear_boton_menu(texto, accion)

        tk.Frame(self.panel_menu, bg="#d3d8de", height=1).pack(
            fill="x", padx=11, pady=(12, 8)
        )
        tk.Button(
            self.panel_menu,
            text="Guardar y salir",
            command=self.cerrar,
            font=("Segoe UI", 9),
            anchor="w",
            padx=10,
            pady=6,
            bg="#dfe3e8",
            fg="#263445",
            activebackground="#cfd6de",
            relief="flat",
            bd=0,
        ).pack(fill="x", padx=8, pady=(0, 10))

    def _crear_boton_menu(self, texto, accion):
        tk.Button(
            self.panel_menu,
            text=texto,
            command=lambda: self.ejecutar_accion(texto, accion),
            font=("Segoe UI", 9),
            anchor="w",
            padx=10,
            pady=5,
            bg="#f7f8f9",
            fg="#263445",
            activebackground="#dce3ea",
            activeforeground="#172536",
            relief="flat",
            bd=0,
        ).pack(fill="x", padx=8, pady=1)

    # ----------------------------------------------------------
    # MENSAJES Y ESTADO
    # ----------------------------------------------------------

    def escribir(self, texto=""):
        self.salida.configure(state="normal")
        self.salida.insert("end", str(texto) + "\n")
        self.salida.see("end")
        self.salida.configure(state="disabled")

    def mostrar_inicio(self):
        self.escribir("BIBLIOTECA ESCOLAR DIGITAL")
        self.escribir("=" * 52)
        self.escribir("Seleccione una operación del menú de la izquierda.")
        self.escribir("")
        self.escribir("El sistema permite administrar el catálogo y controlar")
        self.escribir("los préstamos y devoluciones de los libros.")
        self.escribir("")
        self.escribir("Los cambios se guardan en la carpeta 'datos'.")

    def limpiar_pantalla(self):
        self.salida.configure(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.configure(state="disabled")
        self.mostrar_inicio()

    def actualizar_estado(self):
        titulos = len(self.catalogo["cod"])
        ejemplares = sum(self.catalogo["stk"])
        activos = len(prestamos_activos(self.prestamos))
        vencidos = len(prestamos_vencidos(self.prestamos))
        self.etiqueta_estado.config(
            text=(f"{titulos} títulos registrados   |   "
                  f"{ejemplares} ejemplares disponibles   |   "
                  f"{activos} préstamos activos   |   {vencidos} vencidos")
        )

    def ejecutar_accion(self, nombre, accion):
        self.escribir("\n" + "-" * 52)
        self.escribir(nombre.upper())
        self.escribir("-" * 52)
        try:
            accion()
        except Exception as error:
            messagebox.showerror(
                "Error", f"No se pudo completar la operación.\n\n{error}",
                parent=self.root,
            )
            self.escribir(f"Error en la operación: {error}")
        self.actualizar_estado()

    def pedir(self, mensaje):
        return simpledialog.askstring(
            "Biblioteca Escolar", mensaje, parent=self.root
        )

    def guardar_cambios(self):
        try:
            guardar_todo(self.catalogo, self.prestamos)
            return True
        except OSError as error:
            messagebox.showerror("Error al guardar", str(error), parent=self.root)
            self.escribir("ERROR: no se pudieron guardar los cambios.")
            return False

    # ----------------------------------------------------------
    # OPERACIONES DEL CATÁLOGO
    # ----------------------------------------------------------

    def registrar_libro(self):
        titulo = self.pedir("Título del libro:")
        if titulo is None:
            self.escribir("Operación cancelada.")
            return
        autor = self.pedir("Autor:")
        if autor is None:
            self.escribir("Operación cancelada.")
            return
        categoria = self.pedir("Categoría:")
        if categoria is None:
            self.escribir("Operación cancelada.")
            return
        cantidad = self.pedir("Ejemplares iniciales (1 a 50):")
        if cantidad is None:
            self.escribir("Operación cancelada.")
            return

        correcto, mensaje, codigo = registrar_libro(
            self.catalogo, titulo, autor, categoria, cantidad
        )
        self.escribir(mensaje)
        if correcto:
            self.escribir(f"Código generado: {codigo}")
            if self.guardar_cambios():
                self.escribir("Datos guardados correctamente.")

    def mostrar_catalogo(self):
        filas = filas_catalogo(self.catalogo)
        if not filas:
            self.escribir("Todavía no hay libros registrados.")
            return
        self.escribir(f"Libros registrados: {len(filas)}")
        self.escribir("CÓDIGO | TÍTULO | AUTOR | CATEGORÍA | STOCK")
        self.escribir("-" * 85)
        for codigo, titulo, autor, categoria, stock in filas:
            self.escribir(
                f"{codigo} | {titulo} | {autor} | {categoria} | {stock}"
            )

    def ordenar(self):
        criterio = self.pedir("Ordenar por:\n1 = código\n2 = título")
        if criterio is None:
            self.escribir("Operación cancelada.")
            return
        if criterio not in ("1", "2"):
            self.escribir("Criterio inválido. Escriba 1 o 2.")
            return
        campo = "cod" if criterio == "1" else "tit"
        ordenar_catalogo(self.catalogo, campo)
        if self.guardar_cambios():
            self.escribir("Catálogo ordenado y guardado correctamente.")
        self.mostrar_catalogo()

    def buscar_codigo(self):
        codigo = self.pedir("Código del libro (ejemplo LIB-001):")
        if codigo is None:
            self.escribir("Búsqueda cancelada.")
            return
        codigo = validar_codigo(codigo)
        if codigo is None:
            self.escribir("Código inválido. Utilice el formato LIB-001.")
            return
        ordenar_catalogo(self.catalogo, "cod")
        posicion = buscar_binaria(self.catalogo, codigo)
        if posicion == -1:
            self.escribir("Libro no encontrado.")
        else:
            fila = filas_catalogo(self.catalogo)[posicion]
            self.escribir("Resultado: " + " | ".join(str(valor) for valor in fila))

    def buscar_titulo(self):
        texto = self.pedir("Escriba el título o una parte del título:")
        if texto is None:
            self.escribir("Búsqueda cancelada.")
            return
        texto = validar_texto(texto)
        if texto is None:
            self.escribir("Ingrese un texto válido.")
            return
        posiciones = buscar_por_titulo(self.catalogo, texto)
        filas = filas_catalogo(self.catalogo)
        if not posiciones:
            self.escribir("No se encontraron coincidencias.")
            return
        for posicion in posiciones:
            self.escribir(" | ".join(str(valor) for valor in filas[posicion]))

    def aumentar_stock(self):
        codigo = self.pedir("Código del libro (LIB-001):")
        if codigo is None:
            self.escribir("Operación cancelada.")
            return
        cantidad = self.pedir("Cantidad de ejemplares que desea agregar (1 a 50):")
        if cantidad is None:
            self.escribir("Operación cancelada.")
            return
        correcto, mensaje = actualizar_stock(self.catalogo, codigo, cantidad)
        self.escribir(mensaje)
        if correcto and self.guardar_cambios():
            self.escribir("Datos guardados.")

    def editar_libro(self):
        if not self.catalogo["cod"]:
            self.escribir("No hay libros registrados para editar.")
            return
        self.mostrar_catalogo()
        codigo = self.pedir("Código del libro que desea editar (LIB-001):")
        if codigo is None:
            self.escribir("Edición cancelada.")
            return
        codigo = validar_codigo(codigo)
        if codigo is None:
            self.escribir("Código inválido. Utilice el formato LIB-001.")
            return
        posicion = buscar_lineal_codigo(self.catalogo, codigo)
        if posicion == -1:
            self.escribir("Libro no encontrado.")
            return

        titulo = simpledialog.askstring(
            "Editar libro", "Nuevo título:",
            initialvalue=self.catalogo["tit"][posicion], parent=self.root
        )
        if titulo is None:
            self.escribir("Edición cancelada.")
            return
        autor = simpledialog.askstring(
            "Editar libro", "Nuevo autor:",
            initialvalue=self.catalogo["aut"][posicion], parent=self.root
        )
        if autor is None:
            self.escribir("Edición cancelada.")
            return
        categoria = simpledialog.askstring(
            "Editar libro", "Nueva categoría:",
            initialvalue=self.catalogo["cat"][posicion], parent=self.root
        )
        if categoria is None:
            self.escribir("Edición cancelada.")
            return
        stock = simpledialog.askstring(
            "Editar libro", "Nuevo stock disponible (0 a 50):",
            initialvalue=str(self.catalogo["stk"][posicion]), parent=self.root
        )
        if stock is None:
            self.escribir("Edición cancelada.")
            return

        correcto, mensaje = editar_libro(
            self.catalogo, codigo, titulo, autor, categoria, stock
        )
        self.escribir(mensaje)
        if correcto and self.guardar_cambios():
            self.escribir("Cambios guardados.")
            self.mostrar_catalogo()

    def eliminar_libro(self):
        if not self.catalogo["cod"]:
            self.escribir("No hay libros registrados para eliminar.")
            return
        self.mostrar_catalogo()
        codigo = self.pedir("Código del libro que desea eliminar (LIB-001):")
        if codigo is None:
            self.escribir("Eliminación cancelada.")
            return
        codigo = validar_codigo(codigo)
        if codigo is None:
            self.escribir("Código inválido. Utilice el formato LIB-001.")
            return
        posicion = buscar_lineal_codigo(self.catalogo, codigo)
        if posicion == -1:
            self.escribir("Libro no encontrado.")
            return

        titulo = self.catalogo["tit"][posicion]
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar este libro?\n\n{codigo} - {titulo}\n\n"
            "Esta acción no se puede deshacer.",
            parent=self.root,
        )
        if not confirmar:
            self.escribir("Eliminación cancelada.")
            return

        correcto, mensaje = eliminar_libro(
            self.catalogo, codigo, self.prestamos
        )
        self.escribir(mensaje)
        if correcto and self.guardar_cambios():
            self.escribir("Cambios guardados.")
            self.mostrar_catalogo()

    # ----------------------------------------------------------
    # OPERACIONES DE PRÉSTAMOS
    # ----------------------------------------------------------

    def registrar_prestamo(self):
        dni = self.pedir("DNI del estudiante (8 dígitos):")
        if dni is None:
            self.escribir("Operación cancelada.")
            return
        nombre = self.pedir("Nombres y apellidos del estudiante:")
        if nombre is None:
            self.escribir("Operación cancelada.")
            return
        codigo = self.pedir("Código del libro (LIB-001):")
        if codigo is None:
            self.escribir("Operación cancelada.")
            return

        correcto, mensaje, identificador = registrar_prestamo(
            self.catalogo, self.prestamos, dni, nombre, codigo
        )
        self.escribir(mensaje)
        if correcto:
            self.escribir(f"ID del préstamo: {identificador}")
            if self.guardar_cambios():
                self.escribir("Datos guardados.")

    def registrar_devolucion(self):
        identificador = self.pedir("ID del préstamo (ejemplo PR-001):")
        if identificador is None:
            self.escribir("Operación cancelada.")
            return
        correcto, mensaje, retraso = devolver_prestamo(
            self.catalogo, self.prestamos, identificador
        )
        self.escribir(mensaje)
        if correcto and self.guardar_cambios():
            self.escribir("Datos guardados.")

    def consultar_estudiante(self):
        dni = self.pedir("DNI del estudiante (8 dígitos):")
        if dni is None:
            self.escribir("Consulta cancelada.")
            return
        registros = prestamos_de_estudiante(self.prestamos, dni)
        if registros is None:
            self.escribir("DNI inválido. Debe contener 8 dígitos.")
            return
        self.escribir(f"Préstamos del estudiante {dni}:")
        self.escribir_filas_prestamos(filas_prestamos(registros))

    def mostrar_vencidos(self):
        self.escribir("Préstamos vencidos:")
        self.escribir_filas_prestamos(filas_vencidos(self.prestamos))

    def mostrar_historial(self):
        self.escribir("Historial de préstamos:")
        self.escribir_filas_prestamos(filas_prestamos(self.prestamos))

    def escribir_filas_prestamos(self, filas):
        if not filas:
            self.escribir("No hay registros para mostrar.")
            return
        for fila in filas:
            self.escribir(" | ".join(str(valor) for valor in fila))

    def cerrar(self):
        confirmar = messagebox.askyesno(
            "Salir",
            "¿Desea guardar los cambios y cerrar la biblioteca?",
            parent=self.root,
        )
        if confirmar and self.guardar_cambios():
            self.root.destroy()


def iniciar_aplicacion(catalogo, prestamos):
    """Inicia la ventana principal de la biblioteca."""
    root = tk.Tk()
    BibliotecaApp(root, catalogo, prestamos)
    root.mainloop()
