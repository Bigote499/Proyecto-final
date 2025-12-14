📦 Inventario de Productos – Ferretería El Clavo Torcido
Este proyecto permite gestionar un inventario de productos utilizando SQLite como base de datos y una interfaz de consola con menús interactivos.
Incluye funciones para agregar, visualizar, actualizar, eliminar y buscar productos, además de generar reportes de bajo stock.

🚀 Características principales
- Base de datos SQLite persistente (inventario.db).
- Menú interactivo en consola con opciones:
- Agregar producto
- Ver productos
- Actualizar precio o cantidad
- Eliminar producto
- Buscar producto
- Reporte de productos con bajo stock
- Uso de Colorama para salida en colores.
- Validación de entradas (precio > 0, cantidad ≥ 0, nombre obligatorio).
- Registro automático de fecha de creación.

📂 Estructura del proyecto
inventario/
│── main.py              # Archivo principal con menú e inicialización
│── funciones.py         # Funciones: agregar, ver, actualizar, eliminar, buscar, reporte
│── inventario.db        # Base de datos SQLite (se crea automáticamente)
│── requirements.txt     # Dependencias del proyecto



⚙️ Requisitos
- Python 3.10+
- Dependencias:
- sqlite3 (incluido en Python estándar)
- colorama
Instalación de dependencias:
pip install -r requirements.txt


Contenido sugerido de requirements.txt:
colorama



▶️ Uso
- Clonar el repositorio:
git clone https://github.com/usuario/inventario.git
cd inventario
- Ejecutar el programa:
python main.py
- Interactuar con el menú:
============================================
GESTIÓN DE INVENTARIO DE PRODUCTOS
1. Agregar producto
2. Ver productos
3. Actualizar precio o cantidad
4. Eliminar producto
5. Buscar producto
6. Reporte de productos con bajo stock
7. Salir
============================================



🧩 Ejemplos de funciones
1. Agregar producto
Solicita nombre, marca (selección de lista o nueva), descripción, cantidad, precio y categoría.
Valida que el precio sea mayor a 0 y la cantidad no negativa.
Ejemplo:
===Agregar un nuevo producto===
Ingresa el nombre del producto: Taladro
Marcas disponibles:
1. Bosch
2. Makita
...
Seleccione una marca por número o ingrese una nueva marca: 1
Ingresa la descripción del producto: Taladro percutor 500W
Ingrese la cantidad: 10
Ingrese el precio: $ 25000
Categorías disponibles:
1. Herramientas manuales
2. Herramientas eléctricas
...
Ingrese el número correspondiente a la categoría: 2
Producto agregado exitosamente.



2. Ver productos
Dos modos:
- Lista con descripción y precio
- Inventario completo (categoría y fecha de creación)
Ejemplo:
Lista de productos
--------------------------------------------------------------------------------
ID     NOMBRE                        MARCA                PRECIO $     CATEGORIA
--------------------------------------------------------------------------------
1      Taladro                       Bosch                $25000.00    Herramientas eléctricas   2025-11-28



3. Actualizar precio o cantidad
Permite elegir entre actualizar precio o cantidad de un producto existente.
Ejemplo:
===Actualizar precio o cantidad de un producto===
Ingresa el ID del producto a actualizar: 1
Producto seleccionado: ID: 1, Nombre: Taladro, Precio: 25000.0, Cantidad: 10
¿Qué deseas actualizar? (1- Precio, 2- Cantidad): 2
Ingresa la nueva cantidad: 15
Producto actualizado exitosamente.



4. Eliminar producto
Elimina un producto por su ID.
Ejemplo:
===Eliminar producto===
Ingresa el ID del producto a eliminar: 3
Producto eliminado exitosamente.



5. Buscar producto
Busca por nombre o marca y muestra coincidencias.
Ejemplo:
===Buscar producto===
Ingresa el nombre o marca a buscar: Bosch
Resultados:
ID: 1 | Nombre: Taladro | Marca: Bosch | Precio: $25000 | Cantidad: 10



6. Reporte de productos con bajo stock
Lista productos cuya cantidad está por debajo de un umbral (ej. ≤ 5 unidades).
Ejemplo:
===Reporte de productos con bajo stock===
ID: 4 | Nombre: Tornillo | Cantidad: 2 | Precio: $0.50
ID: 7 | Nombre: Martillo | Cantidad: 1 | Precio: $3500



🗄️ Base de datos
Tabla productos:
- id → Identificador único (autoincremental).
- nombre → Nombre del producto.
- marca → Marca del producto.
- descripcion → Detalle opcional.
- cantidad → Stock disponible (≥ 0).
- precio → Precio unitario.
- categoria → Clasificación del producto.
- fecha_creacion → Fecha de registro automático.

📌 Roadmap
- Exportar inventario a CSV/Excel.
- Implementar interfaz gráfica (Tkinter o PyQt).
- Reportes avanzados (ventas, ganancias).

📜 Licencia
Este proyecto se distribuye bajo licencia MIT.
Puedes usarlo, modificarlo y compartirlo libremente.

👨‍💻 Créditos
- Autor principal: Sergio
- Basado en código de clase 15 (Daniel Rivero) y adaptado con mejoras propias.


