import sqlite3
import os
from datetime import datetime

def guardar_factura(cliente, direccion, cuit, carrito, modo_pago, tipo_comprobante, venta_id):
    total = sum(item["subtotal"] for item in carrito)

    with sqlite3.connect('inventario.db') as conexion:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO facturas (cliente, direccion, cuit, fecha, modo_pago, comprobante, total, venta_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente,
            direccion,
            cuit,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            modo_pago,
            tipo_comprobante,
            total,
            venta_id
        ))

        factura_id = cursor.lastrowid

    return factura_id

def guardar_cliente(nombre, direccion, cuit):
    with sqlite3.connect("inventario.db") as conexion:
        cursor = conexion.cursor()

        # Buscar por CUIT si está presente
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

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def guardar_factura_pdf(cliente, direccion, cuit, carrito, modo_pago, tipo_comprobante, venta_id):
    carpeta_facturas = r"C:\Users\sergi\OneDrive\Facturas de Ferreteria El Clavo Torcido"
    archivo = os.path.join(carpeta_facturas, f"factura_{venta_id}.pdf")
    c = canvas.Canvas(archivo, pagesize=A4)
    ancho, alto = A4

    # Datos del negocio
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, alto - 50, "Ferretería El Clavo Torcido")
    c.setFont("Helvetica", 10)
    c.drawString(50, alto - 65, "Dirección: Av. Siempreviva 1234")
    c.drawString(50, alto - 80, "CUIT: 20-12345678-9")

    # Encabezado de factura
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, alto - 50, f"Factura {tipo_comprobante}")
    c.setFont("Helvetica", 10)
    c.drawString(400, alto - 65, f"Venta ID: {venta_id}")
    c.drawString(400, alto - 80, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Datos del cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, alto - 120, "Cliente:")
    c.setFont("Helvetica", 10)
    c.drawString(120, alto - 120, cliente)
    c.drawString(50, alto - 135, "Dirección: ")
    c.drawString(120, alto - 135, direccion)
    c.drawString(50, alto - 150, "CUIT: ")
    c.drawString(120, alto - 150, cuit)

    # Tabla de productos
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

    # Total y forma de pago
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"TOTAL: ${total:.2f}")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Modo de pago: {modo_pago}")

    # Guardar PDF
    c.save()
    print(f" Factura PDF generada: {archivo}")
    os.startfile(archivo)  # Esto abre el PDF automáticamente
