import sqlite3
from colorama import Fore
from datetime import datetime
from facturacion import guardar_factura, guardar_cliente, guardar_factura_pdf

# Carrito temporal
carrito = []

# -------------------------------
# Buscar productos
# -------------------------------
def buscar_por_id(producto_id):
    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, marca, precio, cantidad, categoria FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

    if producto:
        print(Fore.CYAN + f"ID: {producto[0]} | Nombre: {producto[1]} | Marca: {producto[2]} | Precio: ${producto[3]} | Stock: {producto[4]} | Categoría: {producto[5]}")
        return producto
    else:
        print(Fore.RED + "No existe un producto con ese ID.")
        return None


def buscar_por_nombre(nombre):
    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, marca, precio, cantidad, categoria FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
        productos = cursor.fetchall()

    if productos:
        for p in productos:
            print(Fore.CYAN + f"ID: {p[0]} | Nombre: {p[1]} | Marca: {p[2]} | Precio: ${p[3]} | Stock: {p[4]} | Categoría: {p[5]}")
        return productos
    else:
        print(Fore.RED + "No se encontraron productos con ese nombre.")
        return []


def buscar_por_categoria(categoria):
    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, marca, precio, cantidad, categoria FROM productos WHERE categoria LIKE ?", (f"%{categoria}%",))
        productos = cursor.fetchall()

    if productos:
        for p in productos:
            print(Fore.CYAN + f"ID: {p[0]} | Nombre: {p[1]} | Marca: {p[2]} | Precio: ${p[3]} | Stock: {p[4]} | Categoría: {p[5]}")
        return productos
    else:
        print(Fore.RED + "No se encontraron productos en esa categoría.")
        return []


def buscar_filtrado(nombre="", marca=""):
    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()
        query = "SELECT id, nombre, marca, precio FROM productos WHERE 1=1"
        params = []

        if nombre:
            query += " AND nombre LIKE ?"
            params.append(f"%{nombre}%")
        if marca:
            query += " AND marca LIKE ?"
            params.append(f"%{marca}%")

        cursor.execute(query, params)
        productos = cursor.fetchall()

    return productos

# -------------------------------
# Carrito y ventas
# -------------------------------
def agregar_producto_a_carrito(producto_id, cantidad):
    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, marca, precio, cantidad FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

    if producto is None:
        print(Fore.RED + "Producto no encontrado.")
        return

    if cantidad > producto[4]:  # stock
        print(Fore.RED + "No hay suficiente stock.")
        return

    subtotal = producto[3] * cantidad
    carrito.append({
        "id": producto[0],
        "nombre": producto[1],
        "marca": producto[2],
        "precio": producto[3],
        "cantidad": cantidad,
        "subtotal": subtotal
    })
    print(Fore.GREEN + f"{cantidad} x {producto[1]} agregado al carrito. Subtotal: ${subtotal:.2f}")


def mostrar_carrito():
    print(Fore.CYAN + "\n--- Carrito actual ---")
    total = 0
    for item in carrito:
        print(f"{item['cantidad']} x {item['nombre']} ({item['marca']}) (${item['precio']} c/u) = ${item['subtotal']:.2f}")
        total += item['subtotal']
    print(Fore.YELLOW + f"TOTAL: ${total:.2f}")
    return total


def guardar_detalle_venta():
    if not carrito:
        print(Fore.RED + "El carrito está vacío.")
        return None

    total = mostrar_carrito()

    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO ventas (fecha, total)
            VALUES (?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total))
        id_venta = cursor.lastrowid

        for item in carrito:
            cursor.execute("""
                INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (id_venta, item['id'], item['cantidad'], item['precio'], item['subtotal']))

            cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE id = ?", (item['cantidad'], item['id']))

    return id_venta

# -------------------------------
# Generar factura
# -------------------------------
def generar_factura(venta_id, cliente_id, modo_pago, comprobante, ruta_pdf):
    global carrito  # usamos el carrito global

    # Actualizar la venta
    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE ventas
            SET modo_pago = ?, comprobante = ?
            WHERE id = ?
        """, (modo_pago, comprobante, venta_id))

        cursor.execute("SELECT total FROM ventas WHERE id = ?", (venta_id,))
        resultado = cursor.fetchone()
        if resultado:
            total = resultado[0]
        else:
            print(Fore.RED + "No se encontró la venta para generar la factura.")
            return

    print("Carrito recibido:", carrito)

    # Guardar la factura en la base
    guardar_factura(cliente_id, carrito, modo_pago, comprobante, venta_id, ruta_pdf)

    # Generar el PDF (sin ruta_pdf, porque la función ya arma el archivo)
    guardar_factura_pdf(cliente_id, carrito, modo_pago, comprobante, venta_id)

    print(Fore.GREEN + f"Factura {comprobante} emitida para cliente ID {cliente_id} - Total: ${total:.2f}")

# -------------------------------
# Vaciar carrito
# -------------------------------
def vaciar_carrito():
    global carrito
    if carrito:
        carrito.clear()
        print(Fore.CYAN + "Carrito vaciado.")
    else:
        print(Fore.YELLOW + "El carrito ya está vacío.")