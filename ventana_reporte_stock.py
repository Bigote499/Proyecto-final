from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
import sqlite3
import os

class VentanaReporteStock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reporte de Bajo Stock")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Campo para ingresar límite
        self.input_limite = QLineEdit()
        self.input_limite.setPlaceholderText("Ingrese límite de cantidad")
        layout.addWidget(QLabel("Cantidad límite:"))
        layout.addWidget(self.input_limite)

        # Botón generar reporte
        self.btn_generar = QPushButton("Generar reporte")
        self.btn_generar.clicked.connect(self.generar_reporte)
        layout.addWidget(self.btn_generar)

        # Tabla resultados
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Marca", "Cantidad"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    def generar_reporte(self):
        limite_str = self.input_limite.text().strip()
        if not limite_str.isdigit():
            QMessageBox.warning(self, "Error", "El límite debe ser un número entero.")
            return

        limite = int(limite_str)

        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, marca, cantidad FROM productos WHERE cantidad < ?", (limite,))
        productos_bajo_stock = cursor.fetchall()
        conexion.close()

        if not productos_bajo_stock:
            QMessageBox.information(self, "Sin resultados", f"No hay productos con cantidad menor a {limite}.")
            self.tabla.setRowCount(0)
            return

        self.tabla.setRowCount(len(productos_bajo_stock))
        for fila, producto in enumerate(productos_bajo_stock):
            for columna, valor in enumerate(producto):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))

        # 👉 Generar PDF automáticamente
        self.exportar_pdf(productos_bajo_stock, limite)

    def exportar_pdf(self, productos, limite):
        archivo = "reporte_bajo_stock.pdf"
        doc = SimpleDocTemplate(archivo, pagesize=A4)
        elementos = []

        estilos = getSampleStyleSheet()
        titulo = Paragraph("Reporte de Bajo Stock", estilos["Title"])
        fecha = Paragraph(f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')}", estilos["Normal"])
        subtitulo = Paragraph(f"Productos con cantidad menor a {limite}", estilos["Heading2"])

        elementos.extend([titulo, fecha, subtitulo, Spacer(1, 20)])

        # Encabezados
        data = [["ID", "Nombre", "Marca", "Cantidad"]]

        # Agregar productos
        for p in productos:
            data.append([p[0], p[1], p[2], p[3]])

        tabla = Table(data, colWidths=[50, 200, 150, 80])

        estilo = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])

        # Resaltar filas críticas
        for i, fila in enumerate(data[1:], start=1):
            if int(fila[3]) < 5:
                estilo.add("BACKGROUND", (0, i), (-1, i), colors.lightcoral)

        tabla.setStyle(estilo)
        elementos.append(tabla)

        doc.build(elementos)
        QMessageBox.information(self, "PDF generado", f"Se creó el archivo {archivo} correctamente.")
        os.startfile(archivo)  # Abrir el PDF generado automáticamente