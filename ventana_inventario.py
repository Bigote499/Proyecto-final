from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
import sqlite3

class VentanaInventario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario de Productos")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Marca", "Cantidad", "Precio", "Categoría", "Actualización"])
        layout.addWidget(self.tabla)

        # Botones
        botones_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.clicked.connect(self.abrir_ventana_agregar)
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.abrir_ventana_buscar)
        self.btn_reporte = QPushButton("Reporte bajo stock")
        self.btn_reporte.clicked.connect(self.abrir_ventana_reporte)
        botones_layout.addWidget(self.btn_agregar)
        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_eliminar)
        botones_layout.addWidget(self.btn_buscar)
        botones_layout.addWidget(self.btn_reporte)
        layout.addLayout(botones_layout)

        # Mensaje
        self.mensaje = QLabel("")
        layout.addWidget(self.mensaje)

        self.cargar_productos()

    def cargar_productos(self):
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, marca, cantidad, precio, categoria, fecha_actualizacion FROM productos")
        productos = cursor.fetchall()
        conexion.close()

        self.tabla.setRowCount(len(productos))
        for fila, producto in enumerate(productos):
            for columna, valor in enumerate(producto):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def abrir_ventana_agregar(self):
        from ventana_agregar_producto import VentanaAgregarProducto
        self.ventana_agregar = VentanaAgregarProducto(self.cargar_productos)
        self.ventana_agregar.show()

    def abrir_ventana_actualizar(self):
        from ventana_actualizar_producto import VentanaActualizarProducto
        self.ventana_actualizar = VentanaActualizarProducto(self.cargar_productos)
        self.ventana_actualizar.show()

    def abrir_ventana_eliminar(self):
        from ventana_eliminar_producto import VentanaEliminarProducto
        self.ventana_eliminar = VentanaEliminarProducto(self.cargar_productos)
        self.ventana_eliminar.show()

    def abrir_ventana_buscar(self):
        from ventana_buscar_producto import VentanaBuscarProducto
        self.ventana_buscar = VentanaBuscarProducto()
        self.ventana_buscar.show()

    def abrir_ventana_reporte(self):
        from ventana_reporte_stock import VentanaReporteStock
        self.ventana_reporte = VentanaReporteStock()
        self.ventana_reporte.show()