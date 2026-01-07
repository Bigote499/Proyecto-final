import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from ventana_ventas import VentanaVentas
from ventana_inventario import VentanaInventario
from ventana_login import VentanaLogin
from launcher import Launcher


# Función para leer usuarios desde user.txt
def cargar_usuarios():
    usuarios = {}
    try:
        with open("user.txt", "r") as f:
            for linea in f:
                usuario, contraseña, rol = linea.strip().split(":")
                usuarios[usuario] = {"password": contraseña, "rol": rol}
    except FileNotFoundError:
        print("Archivo de usuarios no encontrado.")
    return usuarios

# Callback que se ejecuta cuando el login es correcto
def abrir_menu(rol):
    ventana = Launcher()

    # Ejemplo: limitar botones según rol
    if rol == "empleado":
        # ocultar botón de Inventario si no es admin
        for boton in ventana.findChildren(QPushButton):
            if boton.text() == "Inventario de Productos":
                boton.hide()



    ventana.show()
    return ventana

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar usuarios desde user.txt
    usuarios = cargar_usuarios()

    # Mostrar ventana de login primero
    login = VentanaLogin(usuarios, abrir_menu)
    login.show()

    sys.exit(app.exec_())