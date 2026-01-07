from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3

class VentanaEliminarProducto(QWidget):
    def __init__(self, recargar_tabla_callback):
        super().__init__()
        self.setWindowTitle("Eliminar Producto")
        self.resize(350, 150)
        self.recargar_tabla_callback = recargar_tabla_callback

        layout = QVBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID del producto a eliminar")
        layout.addWidget(QLabel("ID del producto:"))
        layout.addWidget(self.input_id)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        layout.addWidget(self.btn_eliminar)

        self.setLayout(layout)

    def eliminar_producto(self):
        id_producto = self.input_id.text().strip()

        if not id_producto.isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número válido.")
            return

        try:
            conexion = sqlite3.connect("inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, marca FROM productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()

            if not producto:
                QMessageBox.warning(self, "Error", f"No se encontró el producto con ID {id_producto}.")
                conexion.close()
                return

            confirmacion = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar el producto?\n\nID: {producto[0]}\nNombre: {producto[1]}\nMarca: {producto[2]}",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirmacion == QMessageBox.Yes:
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                conexion.commit()
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
                self.recargar_tabla_callback()
                self.close()

            conexion.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto:\n{str(e)}")