from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
import sqlite3

class VentanaBuscarProducto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscar Producto")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Selector de criterio
        self.combo_criterio = QComboBox()
        self.combo_criterio.addItems(["Nombre", "Marca", "Categoría"])
        layout.addWidget(QLabel("Buscar por:"))
        layout.addWidget(self.combo_criterio)

        # Campo de búsqueda
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Ingrese texto de búsqueda")
        layout.addWidget(self.input_busqueda)

        # Botón buscar
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_producto)
        layout.addWidget(self.btn_buscar)

        # Tabla resultados
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Marca", "Cantidad", "Precio", "Categoría"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    def buscar_producto(self):
        criterio = self.combo_criterio.currentText().lower()
        texto = self.input_busqueda.text().strip()

        if not texto:
            QMessageBox.warning(self, "Error", "Debe ingresar un texto para buscar.")
            return

        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        query = f"SELECT id, nombre, marca, cantidad, precio, categoria FROM productos WHERE {criterio} LIKE ?"
        cursor.execute(query, (f"%{texto}%",))
        resultados = cursor.fetchall()
        conexion.close()

        if not resultados:
            QMessageBox.information(self, "Sin resultados", f"No se encontraron productos con {criterio}: {texto}")
            self.tabla.setRowCount(0)
            return

        self.tabla.setRowCount(len(resultados))
        for fila, producto in enumerate(resultados):
            for columna, valor in enumerate(producto):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))