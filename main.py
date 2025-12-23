import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from ventana_ventas import VentanaVentas
from ventana_inventario import VentanaInventario

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión")
        self.resize(400, 200)

        layout = QVBoxLayout()

        # Botón para Ventas
        btn_ventas = QPushButton("Ventas y Facturación")
        btn_ventas.clicked.connect(self.abrir_ventas)
        layout.addWidget(btn_ventas)

        # Botón para Inventario
        btn_inventario = QPushButton("Inventario de Productos")
        btn_inventario.clicked.connect(self.abrir_inventario)
        layout.addWidget(btn_inventario)

        self.setLayout(layout)

    def abrir_ventas(self):
        self.ventana_ventas = VentanaVentas()
        self.ventana_ventas.show()

    def abrir_inventario(self):
        self.ventana_inventario = VentanaInventario()
        self.ventana_inventario.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec_())