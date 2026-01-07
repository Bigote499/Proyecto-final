import sqlite3
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import traceback  # ✅ agregado para mostrar errores detallados

def guardar_factura(cliente_id, carrito, modo_pago, comprobante, venta_id, ruta_pdf):
    """Guarda la factura en la base de datos facturas_old."""
    if not carrito:
        raise ValueError("El carrito está vacío. No se puede guardar la factura.")

    total = sum(item["subtotal"] for item in carrito)

    try:
        with sqlite3.connect('inventario.db') as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO facturas_old (cliente_id, fecha, modo_pago, comprobante, total, venta_id, ruta_pdf)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                cliente_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                modo_pago,
                comprobante,
                total,
                venta_id,
                ruta_pdf
            ))

            factura_id = cursor.lastrowid
            conexion.commit()
            print(f"Factura guardada con ID: {factura_id}")
            return factura_id

    except sqlite3.Error as e:
        print("Error al guardar la factura:", e)
        print("TRACEBACK:")
        traceback.print_exc()
        return None


def guardar_cliente(nombre, direccion, cuit):
    """Guarda o actualiza un cliente en la base de datos."""
    with sqlite3.connect("inventario.db") as conexion:
        cursor = conexion.cursor()

        if cuit:
            cursor.execute("SELECT id FROM clientes WHERE cuit = ?", (cuit,))
            existente = cursor.fetchone()
        else:
            cursor.execute("SELECT id FROM clientes WHERE nombre = ?", (nombre,))
            existente = cursor.fetchone()

        if existente:
            cursor.execute("""
                UPDATE clientes
                SET nombre = ?, direccion = ?, cuit = ?
                WHERE id = ?
            """, (nombre, direccion, cuit, existente[0]))
        else:
            cursor.execute("""
                INSERT INTO clientes (nombre, direccion, cuit)
                VALUES (?, ?, ?)
            """, (nombre, direccion, cuit))

        conexion.commit()


def guardar_factura_pdf(cliente_id, carrito, modo_pago, tipo_comprobante, venta_id):
    """Genera el PDF de la factura con los datos del cliente y los productos."""
    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, direccion, cuit FROM clientes WHERE id = ?", (cliente_id,))
        resultado = cursor.fetchone()
        if resultado:
            cliente, direccion, cuit = resultado
            cliente = cliente or "Cliente desconocido"
            direccion = direccion or ""
            cuit = cuit or ""
        else:
            cliente, direccion, cuit = "Cliente desconocido", "", ""

    carpeta_facturas = r"C:\Users\sergi\OneDrive\Facturas de Ferreteria El Clavo Torcido"
    os.makedirs(carpeta_facturas, exist_ok=True)
    archivo = os.path.join(carpeta_facturas, f"factura_{venta_id}.pdf")

    c = canvas.Canvas(archivo, pagesize=A4)
    ancho, alto = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, alto - 50, "Ferretería El Clavo Torcido")
    c.setFont("Helvetica", 10)
    c.drawString(50, alto - 65, "Dirección: Av. Siempreviva 1234")
    c.drawString(50, alto - 80, "CUIT: 20-12345678-9")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, alto - 50, f"Factura {tipo_comprobante}")
    c.setFont("Helvetica", 10)
    c.drawString(400, alto - 65, f"Venta ID: {venta_id}")
    c.drawString(400, alto - 80, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, alto - 120, "Cliente:")
    c.setFont("Helvetica", 10)
    c.drawString(120, alto - 120, cliente)
    c.drawString(50, alto - 135, "Dirección:")
    c.drawString(120, alto - 135, direccion)
    c.drawString(50, alto - 150, "CUIT:")
    c.drawString(120, alto - 150, cuit)

    y = alto - 200
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Producto")
    c.drawString(150, y, "Marca")
    c.drawString(250, y, "Cantidad")
    c.drawString(320, y, "Precio Unit.")
    c.drawString(420, y, "Subtotal")

    c.setFont("Helvetica", 10)
    total = 0
    for item in carrito:
        y -= 20
        c.drawString(50, y, item['nombre'])
        c.drawString(150, y, item['marca'])
        c.drawString(250, y, str(item['cantidad']))
        c.drawString(320, y, f"${item['precio']:.2f}")
        c.drawString(420, y, f"${item['subtotal']:.2f}")
        total += item['subtotal']

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"TOTAL: ${total:.2f}")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Modo de pago: {modo_pago}")

    c.save()
    print(f"Factura PDF generada: {archivo}")
    try:
        os.startfile(archivo)
    except Exception as e:
        print("No se pudo abrir automáticamente el PDF:", e)