from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
import sqlite3
from datetime import datetime

class VentanaActualizarProducto(QWidget):
    def __init__(self, recargar_tabla_callback):
        super().__init__()
        self.setWindowTitle("Actualizar Producto")
        self.resize(400, 250)
        self.recargar_tabla_callback = recargar_tabla_callback

        layout = QVBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID del producto")
        layout.addWidget(QLabel("ID del producto:"))
        layout.addWidget(self.input_id)

        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Nuevo precio")
        layout.addWidget(QLabel("Nuevo precio:"))
        layout.addWidget(self.input_precio)

        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Nueva cantidad")
        layout.addWidget(QLabel("Nueva cantidad:"))
        layout.addWidget(self.input_cantidad)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.actualizar_producto)
        layout.addWidget(self.btn_actualizar)

        self.setLayout(layout)

    def actualizar_producto(self):
        id_producto = self.input_id.text().strip()
        nuevo_precio = self.input_precio.text().strip()
        nueva_cantidad = self.input_cantidad.text().strip()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not id_producto.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número.")
            return

        try:
            conexion = sqlite3.connect("inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT id FROM productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            if not producto:
                QMessageBox.warning(self, "Error", f"No se encontró el producto con ID {id_producto}.")
                return

            if nuevo_precio:
                try:
                    precio = float(nuevo_precio)
                    if precio <= 0:
                        raise ValueError
                    cursor.execute("UPDATE productos SET precio = ?, fecha_actualizacion = ? WHERE id = ?", (precio, fecha_actual, id_producto))
                except ValueError:
                    QMessageBox.warning(self, "Error", "Precio inválido.")
                    return

            if nueva_cantidad:
                if not nueva_cantidad.isdigit() or int(nueva_cantidad) < 0:
                    QMessageBox.warning(self, "Error", "Cantidad inválida.")
                    return
                cursor.execute("UPDATE productos SET cantidad = ?, fecha_actualizacion = ? WHERE id = ?", (int(nueva_cantidad), fecha_actual, id_producto))

            conexion.commit()
            conexion.close()
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
            self.recargar_tabla_callback()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el producto:\n{str(e)}")