from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class VentanaInventario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario de Productos")
        self.resize(600, 400)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí va la lógica de Inventario"))
        self.setLayout(layout)