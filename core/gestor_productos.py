import csv
import os

RUTA_CSV_POR_DEFECTO = "productos.csv"

def cargar_productos(ruta_csv=RUTA_CSV_POR_DEFECTO):
    """
    Carga productos desde un archivo CSV.
    Retorna un diccionario: {codigo: (nombre, precio)}
    Si el archivo no existe, lo crea con encabezado.
    """
    productos = {}
    
    # Crear el archivo con encabezado si no existe
    if not os.path.exists(ruta_csv):
        with open(ruta_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["codigo", "nombre", "precio"])
        return productos

    try:
        with open(ruta_csv, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                codigo = row["codigo"].strip()
                nombre = row["nombre"].strip()
                try:
                    precio = float(row["precio"])
                except (ValueError, KeyError):
                    precio = 0.0
                productos[codigo] = (nombre, precio)
    except Exception as e:
        print(f"Error al cargar productos: {e}")
    
    return productos

def guardar_productos(productos, ruta_csv=RUTA_CSV_POR_DEFECTO):
    """
    Guarda los productos en el archivo CSV.
    Retorna True si tiene éxito, False en caso de error.
    """
    try:
        with open(ruta_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["codigo", "nombre", "precio"])
            for codigo, (nombre, precio) in productos.items():
                writer.writerow([codigo, nombre, precio])
        return True
    except Exception as e:
        print(f"Error al guardar productos: {e}")
        return False
    

def buscar_producto(codigo, productos):
    """
    Busca un producto por código.
    Retorna (nombre, precio) si se encuentra, None si no.
    """
    return productos.get(codigo.strip())

def agregar_o_actualizar_producto(codigo, nombre, precio, productos):
    """
    Agrega o actualiza un producto en el diccionario.
    """
    productos[codigo.strip()] = (nombre.strip(), float(precio))


