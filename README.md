📦 Inventario de Productos – Ferretería El Clavo Torcido
# Sistema de Ventas e Inventario - Ferretería El Buen Clavo

## 📋 Descripción
Este proyecto es un sistema de gestión para una ferretería, desarrollado en **Python** con **PyQt** para la interfaz gráfica y **SQLite** como base de datos.  
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

## 📂 Organización de archivos
- `ventas.py` → Lógica de ventas y facturación.
- `facturacion.py` → Generación de facturas y PDFs.
- `inventario.db` → Base de datos SQLite.
- Carpeta `Facturas` → PDFs generados y sincronizados con OneDrive.

## ⚙️ Instalación y uso
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/ferreteria.git