import tkinter as tk
from tkinter import ttk, messagebox

class FormularioAgregar:

    def __init__(self, parent, codigo, callback=None):
        self.parent = parent
        self.codigo = codigo
        self.callback = callback

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Agregar Producto")
        self.ventana.geometry("320x500")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        self.ventana.focus_set()

        # Aplicar estilo clam (solo una vez es suficiente, pero no duele)
        estilo = ttk.Style()
        estilo.theme_use('clam')

        # Código (solo lectura)
        ttk.Label(self.ventana, text="Código:", font=("Arial", 9)).pack(pady=(10, 0))
        ttk.Label(self.ventana, text=codigo, font=("Arial", 10, "bold")).pack()

        # Nombre
        ttk.Label(self.ventana, text="Nombre:").pack(pady=(10, 0))
        self.entry_nombre = ttk.Entry(self.ventana, width=35)
        self.entry_nombre.pack()
        self.entry_nombre.focus()

        # Precio
        ttk.Label(self.ventana, text="Precio:").pack(pady=(8, 0))
        self.entry_precio = ttk.Entry(self.ventana, width=35)
        self.entry_precio.pack()

        # Botones
        frame_botones = ttk.Frame(self.ventana)
        frame_botones.pack(pady=15)

        ttk.Button(frame_botones, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.ventana.destroy).pack(side=tk.LEFT, padx=5)

    def guardar(self):
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


class FormularioEditar:
    def __init__(self, parent, codigo, nombre_actual, precio_actual, callback=None):
        self.parent = parent
        self.codigo = codigo
        self.callback = callback

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Producto")
        self.ventana.geometry("320x500")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()
        self.ventana.focus_set()

        estilo = ttk.Style()
        estilo.theme_use('clam')

        # Código
        ttk.Label(self.ventana, text="Código:", font=("Arial", 9)).pack(pady=(10, 0))
        ttk.Label(self.ventana, text=codigo, font=("Arial", 10, "bold")).pack()

        # Nombre
        ttk.Label(self.ventana, text="Nombre:").pack(pady=(10, 0))
        self.entry_nombre = ttk.Entry(self.ventana, width=35)
        self.entry_nombre.insert(0, nombre_actual)
        self.entry_nombre.pack()
        self.entry_nombre.focus()

        # Precio
        ttk.Label(self.ventana, text="Precio:").pack(pady=(8, 0))
        self.entry_precio = ttk.Entry(self.ventana, width=35)
        self.entry_precio.insert(0, str(precio_actual))
        self.entry_precio.pack()

        # Botones
        frame_botones = ttk.Frame(self.ventana)
        frame_botones.pack(pady=15)

        ttk.Button(frame_botones, text="Guardar", command=self.guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.ventana.destroy).pack(side=tk.LEFT, padx=5)

    def guardar(self):
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
