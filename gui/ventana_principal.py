# ui/ventana_principal.py

import tkinter as tk
from tkinter import ttk
from core.gestor_productos import cargar_productos, guardar_productos, buscar_producto, agregar_o_actualizar_producto
from gui.formularios import FormularioAgregar, FormularioEditar


class VentanaPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Tienda de Abarrotes - Escáner")
        
        # Maximizar de forma compatible con Linux
        self.ventana.attributes('-zoomed', True)
        
        # Aplicar tema clam
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Cargar productos al inicio
        self.productos = cargar_productos()
        
        # Configurar la interfaz
        self._crear_interfaz()
        
        # Mostrar mensaje de bienvenida
        self.resultado_label.config(text="Tienda de Abarrotes\nEscanea un código de barras", foreground="black")
        
        # Enfocar el campo de entrada al inicio
        self.entrada.focus_set()
        
        # Restaurar foco cuando la ventana principal gana foco
        self.ventana.bind("<FocusIn>", self._al_ganar_foco)

    def _crear_interfaz(self):
        # Frame principal para centrar contenido
        frame_principal = ttk.Frame(self.ventana)
        frame_principal.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Campo de entrada (invisible pero funcional)
        self.entrada = ttk.Entry(frame_principal, width=1)
        self.entrada.pack()
        self.entrada.bind("<Return>", self.procesar_codigo)
        
        # Etiqueta para mostrar el resultado (muy grande)
        self.resultado_label = ttk.Label(
            frame_principal,
            text="",
            font=("Helvetica", 48, "bold"),
            justify="center"
        )
        self.resultado_label.pack(expand=True, fill='both', pady=20)
        
        # Frame para botones (abajo)
        self.frame_botones = ttk.Frame(frame_principal)
        self.frame_botones.pack(pady=10)
        
        # Botones (se crean/ocultan dinámicamente)
        self.boton_agregar = None
        self.boton_editar = None

    def _al_ganar_foco(self, event=None):
        """Restaura el foco al campo de entrada cuando la ventana principal se activa."""
        # Solo restaurar foco si no hay ventanas emergentes abiertas
        # (Tkinter no tiene forma directa de saberlo, pero si el foco no está en la ventana, no forzamos)
        self.ventana.after(50, lambda: self.entrada.focus_set())

    def procesar_codigo(self, event=None):
        codigo = self.entrada.get().strip()
        self.entrada.delete(0, tk.END)
        
        if not codigo:
            self.mostrar_mensaje("Código vacío", "error")
            return

        producto = buscar_producto(codigo, self.productos)
        
        if producto:
            nombre, precio = producto
            self.mostrar_mensaje(f"{nombre}\n${precio:.2f}", "exito")
            self.mostrar_botones_editar(codigo, nombre, precio)
        else:
            self.mostrar_mensaje("Producto no encontrado", "error")
            self.mostrar_botones_agregar(codigo)

    def mostrar_mensaje(self, texto, tipo):
        self.resultado_label.config(text=texto)
        if tipo == "exito":
            self.resultado_label.config(foreground="green")
        elif tipo == "error":
            self.resultado_label.config(foreground="red")
        else:
            self.resultado_label.config(foreground="black")

    def mostrar_botones_agregar(self, codigo):
        self._limpiar_botones()
        self.boton_agregar = ttk.Button(
            self.frame_botones,
            text="➕ Agregar Producto",
            command=lambda: self.abrir_formulario_agregar(codigo)
        )
        self.boton_agregar.pack(side=tk.LEFT, padx=10)

    def mostrar_botones_editar(self, codigo, nombre, precio):
        self._limpiar_botones()
        self.boton_editar = ttk.Button(
            self.frame_botones,
            text="✏️ Editar Producto",
            command=lambda: self.abrir_formulario_editar(codigo, nombre, precio)
        )
        self.boton_editar.pack(side=tk.LEFT, padx=10)

    def _limpiar_botones(self):
        if self.boton_agregar:
            self.boton_agregar.destroy()
            self.boton_agregar = None
        if self.boton_editar:
            self.boton_editar.destroy()
            self.boton_editar = None

    def abrir_formulario_agregar(self, codigo):
        def callback(codigo, nombre, precio):
            agregar_o_actualizar_producto(codigo, nombre, precio, self.productos)
            if guardar_productos(self.productos):
                producto = buscar_producto(codigo, self.productos)
                if producto:
                    nombre_nuevo, precio_nuevo = producto
                    self.mostrar_mensaje(f"{nombre_nuevo}\n${precio_nuevo:.2f}", "exito")
                    self.mostrar_botones_editar(codigo, nombre_nuevo, precio_nuevo)
            else:
                self.mostrar_mensaje("Error al guardar", "error")
        
        # Abrir formulario
        FormularioAgregar(self.ventana, codigo, callback=callback)

    def abrir_formulario_editar(self, codigo, nombre_actual, precio_actual):
        def callback(codigo, nombre, precio):
            agregar_o_actualizar_producto(codigo, nombre, precio, self.productos)
            if guardar_productos(self.productos):
                self.mostrar_mensaje(f"{nombre}\n${precio:.2f}", "exito")
                self.mostrar_botones_editar(codigo, nombre, precio)
            else:
                self.mostrar_mensaje("Error al guardar", "error")
        
        FormularioEditar(self.ventana, codigo, nombre_actual, precio_actual, callback=callback)

    def iniciar(self):
        self.ventana.mainloop()