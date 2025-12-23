import sqlite3



def init_db():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    # Tabla de ventas (encabezado)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        modo_pago TEXT,
        comprobante TEXT,
        total REAL
    )
    """)

    # Tabla de detalle de ventas (líneas de productos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_ventas (
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

    # Tabla de facturas (opcional, si la usás)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        direccion TEXT,
        cuit TEXT,
        fecha TEXT,
        modo_pago TEXT,
        comprobante TEXT,
        total REAL,
        venta_id INTEGER REFERENCES ventas(id)
    )
    """)

    #Tabla clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        cuit TEXT UNIQUE
    )
    """)

    conexion.commit()
    conexion.close()
    print("Base inicializada: ventas, detalle_ventas, facturas listas y clientes.")

if __name__ == "__main__":
    init_db()