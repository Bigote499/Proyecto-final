import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QComboBox
)

class HistorialFacturas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de Facturas")
        self.resize(800, 400)

        layout = QVBoxLayout()

        # --- Filtros ---
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Cliente:"))
        self.filtro_cliente = QLineEdit()
        filtro_layout.addWidget(self.filtro_cliente)

        filtro_layout.addWidget(QLabel("Comprobante:"))
        self.filtro_comprobante = QComboBox()
        self.filtro_comprobante.addItem("Todos")
        self.filtro_comprobante.addItem("Factura A")
        self.filtro_comprobante.addItem("Factura B")
        self.filtro_comprobante.addItem("Factura C")
        filtro_layout.addWidget(self.filtro_comprobante)

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.clicked.connect(self.cargar_facturas)
        filtro_layout.addWidget(btn_filtrar)

        layout.addLayout(filtro_layout)

        # --- Tabla ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Fecha", "Cliente", "Comprobante", "Modo de Pago", "Total", "Abrir PDF"
        ])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        # Cargar facturas al iniciar
        self.cargar_facturas()

    def cargar_facturas(self):
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()

        # Construir query con filtros
        query = """
        SELECT f.fecha, c.nombre, f.comprobante, f.modo_pago, f.total, f.ruta_pdf
        FROM facturas f
        JOIN clientes c ON f.cliente_id = c.id
        WHERE 1=1
        """
        params = []

        if self.filtro_cliente.text():
            query += " AND c.nombre LIKE ?"
            params.append("%" + self.filtro_cliente.text() + "%")

        if self.filtro_comprobante.currentText() != "Todos":
            query += " AND f.comprobante = ?"
            params.append(self.filtro_comprobante.currentText())

        query += " ORDER BY f.fecha DESC"

        cursor.execute(query, params)
        facturas = cursor.fetchall()
        conexion.close()

        # Llenar tabla
        self.tabla.setRowCount(len(facturas))
        for row, factura in enumerate(facturas):
            for col, valor in enumerate(factura[:-1]):  # excepto ruta_pdf
                self.tabla.setItem(row, col, QTableWidgetItem(str(valor)))

            # Botón abrir PDF
            btn_pdf = QPushButton("Abrir")
            ruta_pdf = factura[-1]
            btn_pdf.clicked.connect(lambda _, ruta=ruta_pdf: os.startfile(ruta))
            self.tabla.setCellWidget(row, 5, btn_pdf)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = HistorialFacturas()
    ventana.show()
    sys.exit(app.exec_())