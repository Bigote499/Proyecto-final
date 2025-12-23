import sqlite3

conexion = sqlite3.connect('inventario.db')
cursor = conexion.cursor()

# Eliminar la tabla si existe
cursor.execute("DROP TABLE IF EXISTS ventas")

# Crear la tabla con la estructura completa (encabezado de la venta)
cursor.execute("""
    CREATE TABLE ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        cliente TEXT,
        modo_pago TEXT,
        comprobante TEXT,
        total REAL
    )
""")

conexion.commit()
conexion.close()
print("Tabla 'ventas' reiniciada con éxito.")

with sqlite3.connect('inventario.db') as conexion:
    cursor = conexion.cursor()

    # 1. Crear tabla nueva con orden deseado
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_ventas_nueva (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER,
            producto_id INTEGER,
            marca TEXT,
            cantidad INTEGER,
            precio_unitario REAL,
            subtotal REAL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    # 2. Copiar datos desde la tabla vieja
    cursor.execute("""
        INSERT INTO detalle_ventas_nueva (id, venta_id, producto_id, marca, cantidad, precio_unitario, subtotal)
        SELECT id, venta_id, producto_id, marca, cantidad, precio_unitario, subtotal FROM detalle_ventas
    """)

    # 3. Borrar tabla vieja
    cursor.execute("DROP TABLE detalle_ventas")

    # 4. Renombrar la nueva
    cursor.execute("ALTER TABLE detalle_ventas_nueva RENAME TO detalle_ventas")