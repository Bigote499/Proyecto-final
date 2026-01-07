from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class VentanaLogin(QWidget):
    def __init__(self, usuarios, abrir_menu_callback):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.resize(300, 150)
        self.usuarios = usuarios
        self.abrir_menu_callback = abrir_menu_callback

        layout = QVBoxLayout()

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Usuario")
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.input_usuario)

        self.input_contraseña = QLineEdit()
        self.input_contraseña.setPlaceholderText("Contraseña")
        self.input_contraseña.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.input_contraseña)

        self.btn_login = QPushButton("Ingresar")
        self.btn_login.clicked.connect(self.verificar_login)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def verificar_login(self):
        usuario = self.input_usuario.text().strip()
        contraseña = self.input_contraseña.text().strip()
    
        if usuario in self.usuarios and self.usuarios[usuario]["password"] == contraseña:
            rol = self.usuarios[usuario]["rol"]
    
            # Guardar la ventana principal como atributo para que no se cierre
            self.ventana_principal = self.abrir_menu_callback(rol)
    
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")