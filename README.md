# Sales and Inventory System – Ferretería El Clavo Torcido

## Description

This project is a management system for a hardware store, developed in **Python** using **PyQt5** for the graphical interface and **SQLite** as the database.  
It allows you to manage products, inventory, customers, and sales, generating professional **PDF invoices** with automatic storage in a cloud-synced folder (e.g., OneDrive).

## Main Features

- Product and inventory management  
- Customer registration with CUIT validation (`XX-XXXXXXXX-X` format)  
- Sales flow with cart and item details  
- PDF invoice generation with logo and full metadata  
- Automatic opening of the generated invoice  
- Storage of invoices in a OneDrive-synced folder  
- Normalized database with tables: `ventas`, `detalle_ventas`, `productos`, `clientes`, `facturas`

## Database Structure

Main tables:
- **productos**: product catalog  
- **ventas**: sale headers  
- **detalle_ventas**: product lines per sale (includes brand)  
- **clientes**: customer data  
- **facturas**: issued invoice records

## Technologies Used

- Python 3  
- PyQt5  
- SQLite3  
- ReportLab (PDF generation)  
- Pillow (image handling, e.g., logo)  
- Colorama (console formatting)

## Project Structure
├── main.py                      # Main entry point ├── launcher.py                  # Launches the GUI ├── productos_backend.py         # Product logic (no GUI) ├── ventas.py                    # Sales flow and cart ├── facturacion.py               # PDF invoice generation ├── inventario.db                # SQLite database ├── ventana_login.py             # Login interface ├── ventana_ventas.py            # Sales interface ├── ventana_reporte_stock.py     # Low stock report interface ├── ventana_agregar_producto.py  # Add product interface ├── ventana_actualizar_producto.py # Update product interface ├── ventana_eliminar_producto.py   # Delete product interface ├── ventana_inventario.py        # Inventory overview ├── historial_de_facturas.py     # Invoice history viewer ├── detalle_venta_facturar.py    # Product details per invoice ├── resetventas.py               # Reset sales script ├── borrar_tabla_facturas.py     # Clear invoice table script ├── requirements.txt             # Project dependencies ├── README.md                    # Documentation (Spanish) ├── README_en.md                 # Documentation (English) ├── img_logo/                    # Logo ├── img_gui/                     # Screenshots ├── Facturas/                    # Generated PDFs (synced with OneDrive) └── user.txt                     # Basic user data

## Screenshots

### Login
![Login](img_gui/login.png)

### Sales and Cart Window
![Sales - Add to Cart](img_gui/ventas_carrito.png)

### Generated PDF Invoice
![Invoice PDF](img_gui/factura_pdf.png)

### Low Stock Report
![Low Stock Report](img_gui/reporte_stock.png)

## Installation and Usage

1. Clone the repository:
```bash
git clone https://github.com/Bigote499/Proyecto-final.git
cd Proyecto-final

2. Create a virtual environment (optional but recommended):
python -m venv venv
venv\Scripts\activate   # Windows


3. Install dependencies:
pip install -r requirements.txt


4. Run the system:
python launcher.py

License
This project is licensed under the MIT License.
See the LICENSE file for details.

Author
Sergio Sosa
Python Developer specialized in PyQt5, ReportLab, and business management systems
GitHub: Bigote499





# 📦 Inventario de Productos – Ferretería El Clavo Torcido  
# 🛠️ Sistema de Ventas e Inventario - Ferretería El Clavo Torcido

## 📋 Descripción
Este proyecto es un sistema de gestión para una ferretería, desarrollado en **Python** con **PyQt5** para la interfaz gráfica y **SQLite** como base de datos.  
Permite manejar ventas, clientes, productos e inventario, generando facturas en **PDF** con formato profesional y guardándolas automáticamente en la nube (OneDrive).

## 🚀 Funcionalidades principales
- Gestión de productos e inventario.  
- Registro de clientes con validación de CUIT en formato `XX-XXXXXXXX-X`.  
- Flujo de ventas con carrito y detalle de productos.  
- Generación de facturas en PDF con logo y datos completos.  
- Apertura automática del PDF al emitir la factura.  
- Almacenamiento de facturas en carpeta sincronizada con OneDrive.  
- Base de datos normalizada con tablas: `ventas`, `detalle_ventas`, `productos`, `clientes`, `facturas`.  

## 🗄️ Base de datos
Tablas principales:
- **productos**: catálogo de artículos.  
- **ventas**: encabezado de cada venta.  
- **detalle_ventas**: líneas de productos por venta (incluye `marca`).  
- **clientes**: datos de clientes.  
- **facturas**: registro de facturas emitidas.  

## 🖥️ Tecnologías utilizadas
- Python 3  
- PyQt5  
- SQLite3  
- ReportLab (para generación de PDFs)  
- Pillow (para manejo de imágenes, como el logo)  

## 📂 Organización de archivos
├── main.py                      # Punto de entrada principal ├── launcher.py                 # Lanza la interfaz gráfica ├── productos_backend.py        # Lógica de productos (sin GUI) ├── ventas.py                   # Flujo de ventas y carrito ├── facturacion.py              # Generación de facturas en PDF ├── inventario.db               # Base de datos SQLite ├── ventana_login.py            # Interfaz de login ├── ventana_ventas.py           # Interfaz de ventas ├── ventana_reporte_stock.py    # Interfaz de reporte de stock ├── ventana_agregar_producto.py # Interfaz para agregar productos ├── ventana_actualizar_producto.py # Interfaz para actualizar productos ├── ventana_eliminar_producto.py   # Interfaz para eliminar productos ├── ventana_inventario.py       # Vista general del inventario ├── historial_de_facturas.py    # Consulta de facturas emitidas ├── detalle_venta_facturar.py   # Detalle de productos en cada venta ├── resetventas.py              # Script para reiniciar ventas ├── borrar_tabla_facturas.py    # Script para limpiar facturas ├── requirements.txt            # Dependencias del proyecto ├── README.md                   # Documentación del sistema ├── img_logo/ │   └── logo.png                # Logo de la ferretería ├── Facturas/                   # PDFs generados (sincronizados con OneDrive) └── user.txt                    # Datos de usuarios (versión básica)

## 📸 Capturas de pantalla

A continuación se muestran algunas ventanas del sistema en funcionamiento:

### 🧑‍💻 Inicio de sesión
![Inicio de sesión](img_gui/login.png)

### 🛒 Ventana de ventas y carrito
![Ventas - Agregar al carrito](img_gui/ventas_carrito.png)

### 🧾 Factura generada en PDF
![Factura PDF](img_gui/factura_pdf.png)

### 📉 Reporte de bajo stock
![Reporte de bajo stock](img_gui/reporte_stock.png)

## Instalación y uso

1. Clonar el repositorio:
```bash
git clone https://github.com/Bigote499/Proyecto-final.git
cd ferreteria

- Crear entorno virtual (opcional pero recomendado):
python -m venv venv
venv\Scripts\activate   # Windows


- Instalar dependencias:
pip install -r requirements.txt


- Ejecutar el sistema:
python launcher.py


Autor
Sergio Sosa
Desarrollador Python especializado en PyQt5, Reportlab y sistema de gestion
GitHub: Bigote499