from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QTextEdit, QTableWidget, QTableWidgetItem, QDialog,
    QAbstractItemView, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from datetime import datetime
import sqlite3
import ventas
import os


class BusquedaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar producto")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Campos de búsqueda
        self.buscar_nombre = QLineEdit()
        self.buscar_marca = QLineEdit()

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar)

        # Tabla de resultados
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Marca", "Precio"])
        self.tabla.cellDoubleClicked.connect(self.seleccionar_y_cerrar)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)

        # Layout
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.buscar_nombre)
        layout.addWidget(QLabel("Marca:"))
        layout.addWidget(self.buscar_marca)
        layout.addWidget(btn_buscar)
        layout.addWidget(self.tabla)

        

        self.setLayout(layout)
        self.producto_seleccionado = None

    def buscar(self):
        try:
            nombre = self.buscar_nombre.text()
            marca = self.buscar_marca.text()

            productos = ventas.buscar_filtrado(nombre, marca)
            if not productos:
                QMessageBox.information(self, "Sin resultados", "No se encontraron productos.")
                self.tabla.setRowCount(0)
                return

            self.tabla.setRowCount(len(productos))
            for row, p in enumerate(productos):
                try:
                    self.tabla.setItem(row, 0, QTableWidgetItem(str(p[0])))
                    self.tabla.setItem(row, 1, QTableWidgetItem(p[1]))
                    self.tabla.setItem(row, 2, QTableWidgetItem(p[2]))
                    precio = float(str(p[3]).replace(",", "."))
                    self.tabla.setItem(row, 3, QTableWidgetItem(f"${precio:.2f}"))
                except Exception as e:
                    self.tabla.setItem(row, 3, QTableWidgetItem(f"Error: {e}"))
        except Exception as e:
            QMessageBox.critical(self, "Error al buscar", f"Ocurrió un problema: {e}")

    def seleccionar_y_cerrar(self, row, column):
        item_id = self.tabla.item(row, 0)
        if item_id:
            try:
                self.producto_seleccionado = int(item_id.text())
            except ValueError:
                self.producto_seleccionado = None
            self.accept()


class VentanaVentas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventas - Agregar al Carrito")
        self.resize(900, 650)

        layout = QVBoxLayout()
        self.producto_seleccionado_id = None
        self.carrito = []
        layout.addWidget(QLabel("--- PRODUCTOS ---"))

        # Boton buscar producto
        btn_buscar = QPushButton("Buscar producto")
        btn_buscar.clicked.connect(self.abrir_busqueda)
        layout.addWidget(btn_buscar)

        self.lbl_seleccion = QLabel("Producto seleccionado: Ninguno")
        layout.addWidget(self.lbl_seleccion)

        layout.addWidget(QLabel("Cantidad:"))
        self.cantidad = QLineEdit()
        self.cantidad.setEnabled(False)
        self.cantidad.returnPressed.connect(self.agregar_directo_carrito)
        layout.addWidget(self.cantidad)

        # Botón agregar al carrito
        btn_agregar_carrito = QPushButton("Agregar producto al carrito")
        btn_agregar_carrito.clicked.connect(self.agregar_directo_carrito)
        layout.addWidget(btn_agregar_carrito)

        # Botón eliminar producto del carrito
        btn_eliminar = QPushButton("Eliminar producto del carrito")
        btn_eliminar.clicked.connect(self.eliminar_producto_carrito)
        layout.addWidget(btn_eliminar)
        
        # Botón vaciar carrito
        btn_vaciar = QPushButton("Vaciar carrito")
        btn_vaciar.clicked.connect(self.limpiar_carrito)
        layout.addWidget(btn_vaciar)

        # Botón cerrrar carrito
        btn_cerrar_carrito = QPushButton("Cerrar carrito")
        btn_cerrar_carrito.clicked.connect(self.cerrar_carrito)
        layout.addWidget(btn_cerrar_carrito)

        # Botón buscar o agregar cliente
        self.btn_buscar_cliente = QPushButton("Buscar o agregar cliente")
        self.btn_buscar_cliente.clicked.connect(self.buscar_o_agregar_cliente)
        layout.addWidget(self.btn_buscar_cliente)

        # Crear los campos antes de usarlos
        self.input_nombre_cliente = QLineEdit()
        self.input_cuit = QLineEdit()
        self.input_cuit.setInputMask("00-00000000-0;_")
        self.input_direccion = QLineEdit()

        layout.addWidget(QLabel("Nombre del cliente"))
        layout.addWidget(self.input_nombre_cliente)

        layout.addWidget(QLabel("CUIT"))
        layout.addWidget(self.input_cuit)

        layout.addWidget(QLabel("Dirección"))
        layout.addWidget(self.input_direccion)

        # Combo para modo de pago
        layout.addWidget(QLabel("Modo de pago"))
        self.combo_pago = QComboBox()
        self.combo_pago.addItems(["Efectivo", "Débito", "Crédito", "Transferencia"])
        layout.addWidget(self.combo_pago)

        # Combo para tipo de comprobante
        layout.addWidget(QLabel("Tipo de comprobante"))
        self.combo_comprobante = QComboBox()
        self.combo_comprobante.addItems(["Factura A", "Factura B", "Presupuesto"])
        layout.addWidget(self.combo_comprobante)

        # Botón facturar
        self.btn_facturar = QPushButton("Facturar")
        self.btn_facturar.clicked.connect(self.facturar)
        layout.addWidget(self.btn_facturar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Marca", "Cantidad", "Precio Unitario", "Subtotal"])
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.tabla)

        self.lbl_total = QLabel("Total del carrito: $0.00")
        layout.addWidget(self.lbl_total)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def abrir_busqueda(self):
        dialogo = BusquedaDialog(self)
        if dialogo.exec_() and dialogo.producto_seleccionado:
            self.producto_seleccionado_id = dialogo.producto_seleccionado
            producto = ventas.buscar_por_id(self.producto_seleccionado_id)
            if producto:
                try:
                    nombre = producto[1]
                    marca = producto[2]
                    precio = float(producto[3])
                    stock = int(producto[4])
                    categoria = producto[5] if len(producto) > 5 else ""
                except Exception as e:
                    self.output.append(f"Error leyendo producto: {e}")
                    return

                self.lbl_seleccion.setText(
                    f"Producto seleccionado: {nombre} | Marca: {marca} | Precio: ${precio:.2f} | Stock: {stock}"
                )
                self.cantidad.setEnabled(True)
                self.cantidad.setFocus()

    def agregar_directo_carrito(self):
        if not self.producto_seleccionado_id:
            self.output.append("Error: no se ha seleccionado ningún producto")
            return
        try:
            cantidad = int(self.cantidad.text())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            self.output.append("Cantidad inválida")
            return

        producto = ventas.buscar_por_id(self.producto_seleccionado_id)
        if not producto:
            self.output.append("Producto no encontrado")
            return

        nombre = producto[1]
        marca = producto[2]
        precio = float(producto[3])
        stock = int(producto[4])

        if cantidad > stock:
            self.output.append(f"No hay suficiente stock. Disponible: {stock}")
            return

        ventas.agregar_producto_a_carrito(self.producto_seleccionado_id, cantidad)
        self.output.append(f"Producto agregado: {cantidad} x {nombre} ✅")
        self.mostrar_carrito()
        self.cantidad.clear()
        self.cantidad.setEnabled(False)
        self.lbl_seleccion.setText("Producto seleccionado: Ninguno")
        self.producto_seleccionado_id = None

    def mostrar_carrito(self):
        self.tabla.clearContents()
        total = 0
        filas = len(ventas.carrito)
        self.tabla.setRowCount(filas + 1)

        for row, item in enumerate(ventas.carrito):
            subtotal = item.get("subtotal", item["precio"] * item["cantidad"])
            total += subtotal

            self.tabla.setItem(row, 0, QTableWidgetItem(str(item["id"])))
            self.tabla.setItem(row, 1, QTableWidgetItem(item["nombre"]))
            self.tabla.setItem(row, 2, QTableWidgetItem(item.get("marca", "")))

            celda_cantidad = QTableWidgetItem(str(item["cantidad"]))
            celda_cantidad.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(row, 3, celda_cantidad)

            celda_precio = QTableWidgetItem(f"${item['precio']:.2f}")
            celda_precio.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(row, 4, celda_precio)

            celda_subtotal = QTableWidgetItem(f"${subtotal:.2f}")
            celda_subtotal.setTextAlignment(Qt.AlignCenter)
            self.tabla.setItem(row, 5, celda_subtotal)

        # Fila final: total
        total_label = QTableWidgetItem("TOTAL")
        total_label.setFlags(Qt.ItemIsEnabled)
        total_label.setTextAlignment(Qt.AlignCenter)
        total_label.setBackground(Qt.lightGray)
        font = total_label.font()
        font.setBold(True)
        total_label.setFont(font)

        total_value = QTableWidgetItem(f"${total:.2f}")
        total_value.setFlags(Qt.ItemIsEnabled)
        total_value.setTextAlignment(Qt.AlignCenter)
        total_value.setBackground(Qt.lightGray)
        total_value.setFont(font)

        self.tabla.setItem(filas, 4, total_label)
        self.tabla.setItem(filas, 5, total_value)

        self.lbl_total.setText(f"Total del carrito: ${total:.2f}")

    def eliminar_producto_carrito(self):
        fila = self.tabla.currentRow()
        # Evitar que se elimine la fila de TOTAL
        if fila < 0 or fila >= len(ventas.carrito):
            self.output.append("No se ha seleccionado ningún producto válido para eliminar.")
            return

        producto = ventas.carrito.pop(fila)
        self.output.append(f"Producto eliminado: {producto['nombre']}")
        self.mostrar_carrito()

    def limpiar_carrito(self):
        ventas.vaciar_carrito()
        self.tabla.setRowCount(0)
        self.lbl_total.setText("Total del carrito: $0.00")
        self.output.append("Carrito vaciado manualmente.")

    def cerrar_carrito(self):
        if not ventas.carrito:
            self.output.append("❌ No hay productos en el carrito para cerrar.")
            return

        try:
            venta_id = ventas.guardar_detalle_venta()  # Esta función guarda los productos y devuelve el ID de venta
            self.venta_id_actual = venta_id  # Guardamos el ID para usarlo en la facturación

            total = ventas.mostrar_carrito()
            self.lbl_total.setText(f"Total del carrito: ${total:.2f}")
            self.output.append(f"✅ Carrito cerrado. Total: ${total:.2f}\nAhora completá los datos del cliente para facturar.")

        except Exception as e:
            self.output.append(f"❌ Error al cerrar el carrito: {e}")

    def buscar_o_agregar_cliente(self):
        try:
            nombre = self.input_nombre_cliente.text().strip()
            cuit = self.input_cuit.text().strip()
            direccion = self.input_direccion.text().strip()


            if not nombre:
                QMessageBox.warning(self, "Nombre faltante", "Por favor ingresá el nombre del cliente.")
                return
    
            with sqlite3.connect("inventario.db") as conexion:
                cursor = conexion.cursor()

                # Buscar cliente por nombre (coincidencia parcial)
                cursor.execute("SELECT id, nombre, cuit, direccion FROM clientes WHERE nombre LIKE ?", (f"%{nombre}%",))
                cliente = cursor.fetchone()

                if cliente:
                    self.cliente_id_actual = cliente[0]  # ✅ Guardamos el ID
                    # Normalizamos valores
                    nombre_db = cliente[1] or ""
                    cuit_db = cliente[2] or ""   #  nunca será None
                    direccion_db = cliente[3] or ""

                    # Rellenar automáticamente los campos encontrados
                    self.input_nombre_cliente.setText(nombre_db)
                    self.input_cuit.setText(cuit_db)
                    self.input_direccion.setText(direccion_db)
                    QMessageBox.information(
                        self,
                        "Cliente encontrado",
                        f"Nombre: {nombre_db}\nCUIT: {cuit_db if cuit_db else 'No registrado'}\nDirección: {direccion_db}"
                    )


                else:
                    # Registrar nuevo cliente (sin CUIT obligatorio)
                    cursor.execute("INSERT INTO clientes (nombre, cuit, direccion) VALUES (?, ?, ?)", (nombre, cuit if cuit else None, direccion))
                    conexion.commit()
                    self.cliente_id_actual = cursor.lastrowid  # ✅ Guardamos el nuevo ID

                    QMessageBox.information(self, "Cliente agregado", "Cliente registrado correctamente.")


        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un problema:\n{str(e)}")

    def facturar(self):
        if hasattr(self, "facturando") and self.facturando:
            self.output.append("⚠️ Ya se está procesando la factura. Esperá un momento.")
            return

        self.facturando = True
        self.btn_facturar.setEnabled(False)

        try:
            cliente = self.input_nombre_cliente.text().strip()
            direccion = self.input_direccion.text().strip()
            cuit = self.input_cuit.text().strip()
            modo_pago = self.combo_pago.currentText()
            comprobante = self.combo_comprobante.currentText()

            if not direccion or not cuit:
                self.output.append("⚠️ El cliente no tiene CUIT o dirección. Se facturará igual, pero los datos estarán incompletos.")

            # Validar que haya cliente cargado
            if not cliente:
                self.output.append("⚠️ Por favor completá el nombre del cliente antes de facturar.")
                return

            # Validar que exista cliente_id_actual
            if not hasattr(self, "cliente_id_actual") or not self.cliente_id_actual:
                self.output.append("❌ No se pudo identificar el cliente. Buscá o agregá un cliente antes de facturar.")
                return

            # Validar que haya venta cerrada
            if not hasattr(self, "venta_id_actual"):
                self.output.append("❌ No hay venta registrada. Cerrá el carrito primero.")
                return

            # Crear ruta del PDF
            nombre_archivo = f"factura_{self.venta_id_actual}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            carpeta_facturas = "Facturas"
            os.makedirs(carpeta_facturas, exist_ok=True)
            ruta_pdf = os.path.join(carpeta_facturas, nombre_archivo)

            # ✅ Guardar factura en la base de datos usando 'with'
            with sqlite3.connect("inventario.db") as conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    INSERT INTO facturas_old (cliente_id, venta_id, modo_pago, comprobante, fecha)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    self.cliente_id_actual,
                    self.venta_id_actual,
                    modo_pago,
                    comprobante,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

                factura_id = cursor.lastrowid

            # ✅ Generar PDF de la factura
            ventas.generar_factura(
                venta_id=self.venta_id_actual,
                cliente_id=self.cliente_id_actual,
                modo_pago=modo_pago,
                comprobante= comprobante,
                ruta_pdf=ruta_pdf
            )

            # ✅ Mensaje de confirmación y limpieza
            self.output.append(f"✅ Venta facturada correctamente con {modo_pago} - {comprobante}.")
            self.lbl_total.setText("Total del carrito: $0.00")
            self.tabla.setRowCount(0)
            ventas.vaciar_carrito()
            del self.venta_id_actual

        except Exception as e:
            self.output.append(f"❌ Error al facturar: {e}")

        self.btn_facturar.setEnabled(True)
        self.facturando = False