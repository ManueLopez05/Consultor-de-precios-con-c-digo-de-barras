import tkinter as tk
from tkinter import ttk, messagebox

class FormularioProducto:
    """Clase base para formularios de producto."""
    def __init__(self, parent, titulo, codigo, nombre_inicial="", precio_inicial=""):
        self.parent = parent
        self.codigo = codigo
        self.callback = None

        self.ventana = tk.Toplevel(parent)
        self.ventana.title(titulo)
        self.ventana.geometry("500x300")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        self.ventana.focus_set()

        estilo = ttk.Style()
        estilo.theme_use('clam')

        # Código (solo lectura)
        ttk.Label(self.ventana, text="Código:", font=("Arial", 16)).pack(pady=(10, 0))
        ttk.Label(self.ventana, text=codigo, font=("Arial", 17, "bold")).pack()

        # Nombre
        ttk.Label(self.ventana, text="Nombre:", font=("Arial", 16)).pack(pady=(12, 0))
        self.entry_nombre = ttk.Entry(self.ventana, width=40, font=("Arial", 16))
        self.entry_nombre.insert(0, nombre_inicial)
        self.entry_nombre.pack()
        self.entry_nombre.focus()

        # Precio
        ttk.Label(self.ventana, text="Precio:", font=("Arial", 16)).pack(pady=(10, 0))
        self.entry_precio = ttk.Entry(self.ventana, width=40, font=("Arial", 16))
        self.entry_precio.insert(0, str(precio_inicial) if precio_inicial else "")
        self.entry_precio.pack()

        # Botones
        frame_botones = ttk.Frame(self.ventana)
        frame_botones.pack(pady=20)

        self.boton_guardar = ttk.Button(
            frame_botones,
            text="Guardar",
            command=self._guardar,
            width=12
        )
        self.boton_guardar.pack(side=tk.LEFT, padx=10)

        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.ventana.destroy,
            width=12
        ).pack(side=tk.LEFT, padx=10)

        # Permitir usar la tecla Espacio para guardar
        # self.ventana.bind("<space>", lambda e: self._guardar())
        # self.boton_guardar.focus()  # Opcional: enfocar botón para que Space funcione

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        precio_str = self.entry_precio.get().strip()

        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre no puede estar vacío.")
            return

        if not precio_str:
            messagebox.showwarning("Advertencia", "El precio no puede estar vacío.")
            return

        try:
            precio = float(precio_str)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido y positivo.")
            return

        if self.callback:
            self.callback(self.codigo, nombre, precio)

        self.ventana.destroy()


class FormularioAgregar(FormularioProducto):
    def __init__(self, parent, codigo, callback=None):
        super().__init__(parent, "Agregar Producto", codigo)
        self.callback = callback


class FormularioEditar(FormularioProducto):
    def __init__(self, parent, codigo, nombre_actual, precio_actual, callback=None):
        super().__init__(parent, "Editar Producto", codigo, nombre_actual, precio_actual)
        self.callback = callback