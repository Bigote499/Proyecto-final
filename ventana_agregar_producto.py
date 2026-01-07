from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
import sqlite3
from datetime import datetime

class VentanaAgregarProducto(QWidget):
    def __init__(self, recargar_tabla_callback):
        super().__init__()
        self.setWindowTitle("Agregar Producto")
        self.resize(400, 300)
        self.recargar_tabla_callback = recargar_tabla_callback

        layout = QVBoxLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del producto")
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.input_nombre)

        self.input_marca = QLineEdit()
        self.input_marca.setPlaceholderText("Marca")
        layout.addWidget(QLabel("Marca:"))
        layout.addWidget(self.input_marca)

        self.input_descripcion = QLineEdit()
        self.input_descripcion.setPlaceholderText("Descripción")
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.input_descripcion)

        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Cantidad")
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.input_cantidad)

        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Precio")
        layout.addWidget(QLabel("Precio:"))
        layout.addWidget(self.input_precio)

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems([
            "Herramientas manuales",
            "Herramientas eléctricas",
            "Elementos de fijación",
            "Construcción"
        ])
        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.combo_categoria)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_producto)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_producto(self):
        nombre = self.input_nombre.text().strip()
        marca = self.input_marca.text().strip()
        descripcion = self.input_descripcion.text().strip()
        cantidad = self.input_cantidad.text().strip()
        precio = self.input_precio.text().strip()
        categoria = self.combo_categoria.currentText()
        fecha = datetime.now().strftime("%Y-%m-%d")

        if not nombre or not cantidad.isdigit() or not precio.replace(".", "", 1).isdigit():
            QMessageBox.warning(self, "Error", "Verificá los campos obligatorios: nombre, cantidad y precio.")
            return

        try:
            conexion = sqlite3.connect("inventario.db")
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, marca, descripcion, cantidad, precio, categoria, fecha_creacion, fecha_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, marca, descripcion, int(cantidad), float(precio), categoria, fecha, fecha))
            conexion.commit()
            conexion.close()
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.recargar_tabla_callback()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el producto:\n{str(e)}")