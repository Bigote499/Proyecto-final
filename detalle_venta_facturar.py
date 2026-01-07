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

    # Tabla clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        cuit TEXT UNIQUE
    )
    """)

    # 🔧 Corrección: renombrar columna en facturas_old
    try:
        cursor.execute("ALTER TABLE facturas_old RENAME COLUMN cliente TO cliente_id")
        print("Columna 'cliente' renombrada a 'cliente_id' en facturas_old.")
    except Exception as e:
        print("No se pudo renombrar la columna:", e)

    try:
        cursor.execute("ALTER TABLE facturas_old ADD COLUMN ruta_pdf TEXT")
        print("Columna 'ruta_pdf' agregada a facturas_old.")
    except Exception as e:
        print("No se pudo agregar la columna ruta_pdf:", e)


    conexion.commit()
    conexion.close()
    print("Base inicializada: ventas, detalle_ventas, clientes y facturas_old corregida.")

if __name__ == "__main__":
    init_db()