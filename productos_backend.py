# Gestión de Productos
# Autor: [Sosa Sergio Hernan]

import sqlite3
from colorama import Fore, Back, Style, init
from datetime import datetime

init(autoreset=True)

# Lista para agregar marcas solo seleccionandola.
marcas = [Back.GREEN + "Bosch", "Makita", "Stanley", "Black+Decker", "Dewalt", "Metabo", "Hitachi", "Milwaukee", "Ryobi", "Worx", "Skil",
"Einhell", "Fercor", "Robust", "Gherardi", "Driwall", "Gardex", "Pretul", "lusqtoff"]
marcas.sort()

"""
Este módulo permite gestionar un inventario de productos en una base de datos SQLite.
Incluye funciones para inicializar la base de datos, basada en la clase 15 main_12.py
(Autor: Daniel Rivero) y adaptada para productos."""
def inicializar_db():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    sql= """ 
        CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        marca TEXT,
        descripcion TEXT,
        cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
        precio REAL NOT NULL,
        categoria TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_actualizacion text

    ) 
"""

    cursor.execute(sql)

    # Verificar si la columna fecha_actualizacion existe, y si no, añadirla. También renombrar CATEGORIA (o renombrar cualquier otra columna) a categoria si es necesario.
     # Investigue en la documentación de sqlite3 y con la ayuda de Copilot(AI).
    cursor.execute("PRAGMA table_info(productos)")
    columns = [col[1] for col in cursor.fetchall()]

    
    if 'CATEGORIA' in columns:
        print(Fore.YELLOW + "La columna 'CATEGORIA' existe. Renombrándola a 'categoria'...")
        cursor.execute("ALTER TABLE productos RENAME COLUMN CATEGORIA TO categoria;")


    
    if 'fecha_actualizacion' not in columns:
        print(Fore.YELLOW + "La columna 'fecha_actualizacion' no existe. Añadiéndola a la tabla 'productos'...")
        cursor.execute("ALTER TABLE productos ADD COLUMN fecha_actualizacion TEXT")
        # Actualizar las filas existentes para que fecha_actualizacion sea igual a fecha_creacion
        cursor.execute("UPDATE productos SET fecha_actualizacion = fecha_creacion WHERE fecha_actualizacion IS NULL")
        print(Fore.GREEN + "Columna 'fecha_actualizacion' añadida y datos existentes actualizados.")


    # Reinicia el contador de ID para que comience desde 1. 
    # Lo busque en la documentación de sqlite3 y la ayuda de Gemini(AI).
    cursor.execute("SELECT name FROM sqlite_sequence WHERE name = 'productos'")
    exists_in_sequence = cursor.fetchone()

    if exists_in_sequence:
        cursor.execute("UPDATE sqlite_sequence SET seq = 999 WHERE name = 'productos'")
    else:
        cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('productos', 999)")
    conexion.commit()
    conexion.close()


"""Agrega un nuevo producto a la base de datos con validaciones y selección de marca y categoría.
 Una parte la cree a partir del código proporcionado en clase 15 main_12.py (Autor: Daniel Rivero)
 y otra parte es de mi autoría creada con lo aprendido en las ultimas clases y basada en la pre-entrega."""
def agregar_producto():
    global marcas
    try:
        while True:
            print(Fore.CYAN + "===Agregar un nuevo producto===")
            nombre = input("Ingresa el nombre del producto o 'n' para salir: ").strip().capitalize()
            if nombre == "n" or nombre == "N":
                print("Saliendo de agregar producto...")
                break
            if nombre == "":
                print("Debe ingresar un producto, la casilla esta vacia")
                continue
            
            print("Marcas disponibles:")       
            for i, marca in enumerate(marcas, start=1):
                print(f"{i}. {marca}")
            print(f"{len(marcas)+1}. Ingresar una nueva marca")

            while True:
                marca_seleccionada = input("Seleccione una marca por número o ingrese una nueva marca: ").strip()
                if marca_seleccionada.isdigit():
                    indice = int(marca_seleccionada) - 1
                    if 0 <= indice < len(marcas):
                        marca = marcas[indice]
                        break
                    elif indice == len(marcas):
                        marca = input("Ingrese el nombre de la nueva marca: ").strip().capitalize()
                        if marca == "":
                            print(Fore.RED + "La marca no puede estar vacía. Intente nuevamente.")
                            continue
                        marcas.append(marca)
                        break
                    else:
                        print(Fore.RED + "Número inválido. Intente nuevamente.")
                else:
                    marca = marca_seleccionada.capitalize()
                    if marca not in marcas:
                        print(f"Marca '{marca}' agregada a la lista")
                        marcas.append(marca)
                    break
            print("\n Listado de marcas actualizado:")
            for i, m in enumerate(marcas, start=1):
                print(f"{i}. {m}")
            descripcion = input("Ingresa la descripción del producto: ").strip()  
            cantidad = input("Ingrese la cantidad: ")
            precio= None
            while precio is None:
                ingresar_precio=(input("Ingrese el precio: $ ").strip())
                try:
                    precio= float(ingresar_precio)
                    if precio<= 0:
                        print(Fore.RED + "precio debe ser mayor a 0")
                        continue
                    break
                except ValueError:
                    print(Fore.RED + "Precio inválido. Ingrese un número (ej. 12.50).")
            categoria_opciones = [
                    "Herramientas manuales",
                    "Herramientas eléctricas",
                    "Elementos de fijación",
                    "Construcción"
]

            print("\nCategorías disponibles:")
            for i, cat in enumerate(categoria_opciones, start=1):
                print(f"{i}. {cat}")
            print("\n")

            fecha_creacion= None  
            fecha_creacion = datetime.now()
            fecha_creacion_str = fecha_creacion.strftime("%Y-%m-%d")  
            fecha_actualizacion = None
            while True:
                try:
                    selec_categoria = int(input("Ingrese el número correspondiente a la categoría: ").strip())
                except ValueError:
                    print(Fore.RED + "Debe ingresar un número válido. Intente nuevamente.")
                    continue

                if 1 <= selec_categoria <= len(categoria_opciones):
                    categoria = categoria_opciones[selec_categoria - 1]
                    break
                else:
                    print(Fore.RED + "Número de categoría inválida. Por favor ingrese un número del 1 al",
                           len(categoria_opciones))

            if not nombre:
                print(Fore.RED + "Error: El nombre del producto es un campo obligatorio.")
                return

            conexion = sqlite3.connect('inventario.db')
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO productos (nombre, marca, descripcion, cantidad, precio, categoria, fecha_creacion, fecha_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, marca, descripcion, int(cantidad), float(precio), categoria, fecha_creacion_str, fecha_creacion_str))
            conexion.commit()


            print(Fore.GREEN + "Producto agregado exitosamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al ingresar los datos: {e}")
        return
    finally:
        if 'conexion' in locals():
            conexion.close()


# Visualiza la lista de productos con dos opciones: descripción y precio, o inventario completo. 
# Es una combinacion del código proyecto final_sql_tabla_productos2 - copia.py y la pre-entrega de mi autoría.
def ver_producto():
    print(Fore.CYAN + "1_Lista de Productos con descripción y precio")
    print(Fore.CYAN + "2_Lista de productos en inventario")
    seleccionar_opcion= input("Selecione la opción a visualizar: ")
    if seleccionar_opcion== "1":
        conexion_db = sqlite3.connect("inventario.db")
        cursor_db = conexion_db.cursor()
        cursor_db.execute("SELECT * FROM productos")
        productos= cursor_db.fetchall()
        conexion_db.close()

        print("Lista de productos")
        print("\n")
        print(Back.GREEN + f"{'ID':<6} {'NOMBRE':<40} {'MARCA':<20} {'DESCRIPCION':<70} {'PRECIO $ ':<25}")
        print("\n")
        


        if productos:
            for producto in productos:
                try:
                    precio= float(producto[5])
                    print(Back.LIGHTBLUE_EX + f"{producto[0]:<6} {producto[1]:<40} {producto[2]:<20} {producto[3]:<70} ${producto[5]:<25.2f}")
                except ValueError:
                    print(Fore.RED + f"{producto[0]:<6} {producto[1]:<40} {producto[2]:<20} {producto[3]:<70} {'ERROR'[5]:<25}")
                print("\n")
                
        else:
            print(Fore.RED + "No hay productos en la lista.")
    elif seleccionar_opcion== "2":
        conexion_db = sqlite3.connect("inventario.db")
        cursor_db = conexion_db.cursor()
        cursor_db.execute("SELECT * FROM productos")
        productos1= cursor_db.fetchall()
        conexion_db.close()

        print("Lista de productos")
        print("\n")
        print(Back.GREEN + f"{'ID':<6} {'NOMBRE':<40} {'MARCA':<20} {'CANTIDAD ':<15} {'CATEGORIA':<30} {'FECHA ACTUALIZACION':<30} ")
        print("\n")


        if productos1:
            for producto in productos1:
                try:
                    cantidad = int(producto[4])
                    print(Back.LIGHTYELLOW_EX + f"{producto[0]:<6} {producto[1]:<40} {producto[2]:<20} {producto[4]:<15} {producto[6]:<30}  {producto[8]:<30}")
                except ValueError:
                    print(Fore.RED + f"{producto[0]:<6} {producto[1]:<40} {producto[2]:<20} {'ERROR'[4]:<15} {producto[6]:<30}  {producto[8]:<30}")
                print("\n")

        else:
            print(Fore.RED + "No hay productos en la lista.")


# Actualiza el precio o la cantidad de un producto existente en la base de datos. 
# Basada en el código proyecto final_sql_tabla_productos2 - copia.py(solo actualizaba el precio),
#  adaptada a partir de la pre-entrega y con el agregado de actualizar la cantidad. Todo de mi autoría.
def actualizar_precio_o_cantidad():
    try:
        print(Fore.CYAN + "===Actualizar precio o cantidad de un producto===")
        id_producto = input("Ingresa el ID del producto a actualizar: ").strip()
        if not id_producto.isdigit():
            print(Fore.RED + "Error: El ID del producto debe ser un número válido.")
            return

        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, precio, cantidad FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.RED + f"Error: No se encontró ningún producto con ID {id_producto}.")
            return

        print(Fore.CYAN + f"Producto seleccionado: ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]:.2f}, Cantidad: {producto[3]}")
        campo_actualizar = input("¿Qué deseas actualizar? (1- Precio, 2- Cantidad): ").strip()

        # Actualizar la fecha al modificar el precio o cantidad.
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if campo_actualizar == "1":
            nuevo_precio = input("Ingresa el nuevo precio: ").strip()
            try:
                nuevo_precio = float(nuevo_precio)
                if nuevo_precio <= 0:
                    print(Fore.RED + "Error: El precio debe ser mayor a 0.")
                    return
            except ValueError:
                print(Fore.RED + "Error: Precio inválido.")
                return

            cursor.execute(
                "UPDATE productos SET precio = ?, fecha_actualizacion = ? WHERE id = ?",
                (nuevo_precio,fecha_actual, id_producto))
        
        elif campo_actualizar == "2":
            nueva_cantidad = input("Ingresa la nueva cantidad: ").strip()
            if not nueva_cantidad.isdigit() or int(nueva_cantidad) < 0:
                print(Fore.RED + "Error: La cantidad debe ser un número entero no negativo.")
                return

            cursor.execute("UPDATE productos SET cantidad = ?, fecha_actualizacion = ? WHERE id = ?",
                            (int(nueva_cantidad), fecha_actual, id_producto))
        
        else:
            print(Fore.RED + "Opción no válida.")
            return

        conexion.commit()
        print(Fore.GREEN + "Producto actualizado exitosamente.")

    except sqlite3.Error as e:
        print(Fore.RED + f"Error al actualizar los datos: {e}")


# Elimina un producto de la base de datos basado en su ID, con confirmación del usuario.
# Basada en el código proyecto final_sql_tabla_productos2 - copia.py y adaptada a partir de la pre-entrega (Ambos de mi autoría).
def eliminar_producto():
        print("Eliminar producto por codigo de producto.")
        id_producto_str = input("Ingrese el ID del producto a eliminar: ").strip()
    
        if not id_producto_str.isdigit():            
            print(Fore.YELLOW + "Debe ingresar un valor valido, intente nuevamente")
            return
        
        id_producto= int(id_producto_str)
        
        conexion_db = None 
        try:
            conexion_db = sqlite3.connect("inventario.db")
            cursor_db = conexion_db.cursor()
            cursor_db.execute("SELECT id, nombre, marca, precio FROM productos WHERE id = ?", (id_producto,))
            fila=cursor_db.fetchone()
            if not fila:
                print(Fore.YELLOW + f"No se encontró el producto con id '{id_producto}'.")
                return
            print(Fore.GREEN + f"Producto encontrado: Código: {fila[0]}, Nombre: {fila[1].capitalize()}, Marca: {fila[2].capitalize()}")       
            
            while True:
                confirmacion= input("Seleccione 's' o 'n' ").strip().lower()
                    
                if confirmacion == "s":
                    cursor_db.execute("DELETE FROM productos  WHERE id = ?", (id_producto,))
                    conexion_db.commit()
                    print(Fore.RED + f"producto eliminado exitosamente de la base de datos.")
                    break
                elif confirmacion == "n":
                    print(Fore.LIGHTYELLOW_EX + "Operación cancelada, el producto no será eliminado")
                    break
                else:
                    print(Fore.LIGHTYELLOW_EX + "Debe ingresar una opción válida ('s' o 'n'). Intente nuevamente.")
                    
                        
        except sqlite3.Error as e:
            print(Fore.RED + f"Error de base de datos: {e}")
        finally:
            if conexion_db: # Asegurarse de que la conexión fue establecida antes de intentar cerrarla
                conexion_db.close()


# Busca productos por nombre, marca o categoría, mostrando los resultados encontrados.  
# Basada en el código proyecto final_sql_tabla_productos2 - copia.py y adaptada a partir de la pre-entrega (Ambos de mi autoría).
# Si bien para el trabajo final no se pide un submenú, ni tampoco buscar por marca, lo agregué para mejorar la experiencia del usuario.
def buscar_producto(seleccion=None):
    print("Buscar producto por nombre , por marca o categoria.")
    if seleccion is None:
        seleccion= input("Buscar por (1) nombre, (2) marca, (3) categoria: ").strip()
    if seleccion == "1":
        buscar= input("Ingrese producto a buscar: ").strip().capitalize()
        columna_busqueda = "nombre"
    elif seleccion == "2":
        buscar= input("Ingrese marca a buscar: ").strip().capitalize()  
        columna_busqueda = "marca"
    elif seleccion == "3":
        buscar= input("Ingrese categoria a buscar: ").strip().capitalize()
        columna_busqueda = "categoria"
    else:
        print(Fore.RED + "Opción inválida. Seleccione 1, 2 o 3.")
        return
    
    if buscar == "":
        print(Fore.RED + "Cadena de busqueda vacía. Intente nuevamente.")
        return
    conexion_db = sqlite3.connect("inventario.db")
    cursor_db = conexion_db.cursor()
    query = f"SELECT * FROM productos WHERE {columna_busqueda} LIKE ?"
    cursor_db.execute(query, (f"{buscar}%",))
    productos_encontrados = cursor_db.fetchall()
    conexion_db.close()

    print("Productos encontrados")
    print("\n")
    print(Back.GREEN + f"{'ID':<6} {'NOMBRE':<40} {'MARCA':<20} {'DESCRIPCION':<70} {'CANTIDAD':<15} {'PRECIO $ ':<25}")
    print("\n")

    if productos_encontrados:
        for producto in productos_encontrados:
            try:
                precio= float(producto[5])  
                print(Fore.BLUE + f"{producto[0]:<6} {producto[1]:<40} {producto[2]:<20} {producto[3]:<70} {producto[4]:<15} {producto[5]:<15.2f}")
            except (ValueError, TypeError):
                print(Fore.RED + f"{producto[0]:<6} {producto[1]:<40} {producto[2]:<20} {producto[3]:<70} {producto[4]:<15}  ERROR: {[5]:<25}")
    else:
        print(Fore.RED + Style.BRIGHT + f"No se encontró el producto {buscar}")

def buscar_submenu():
    print("\n---Buscar Producto---")
    print("1_Buscar por nombre")
    print("2_Buscar por marca")     
    print("3_Buscar por categoria")
    seleccion= input("Seleccione una opción ingresando el número correspondiente (1-3) o 'n' para volver: ").strip()
    if seleccion.lower() == 'n':
        print("Saliendo del menú de búsqueda...")
        return
    
# Reporte de productos con bajo stock, basado en un umbral definido por el usuario.
# Creada completamente por mi autoría con la ayuda de colab.
def reporte_productos_bajo_stock():
    try:
        print(Fore.CYAN + "===Reporte de productos con bajo stock===")
        limite_str = input("Ingresa el limite de cantidad para considerar bajo stock: ").strip()
        try:
            limite = int(limite_str)
            if limite < 0:
                print(Fore.RED + Style.BRIGHT + "Error: El limite debe ser un número entero no negativo.")
                return
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Error: limite inválido.")
            return

        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, marca, cantidad FROM productos WHERE cantidad < ?", (limite,))
        productos_bajo_stock = cursor.fetchall()

        if not productos_bajo_stock:
            print(Fore.YELLOW + "[INFO] No hay productos con bajo stock.")
        else:
            print(Fore.CYAN + f"===Productos con cantidad menor a {Fore.RED}{limite}{Fore.CYAN}===")
            for producto in productos_bajo_stock:
                print(
                Fore.RED + Style.BRIGHT 
                    + f"ID: {producto[0]:<6} Nombre: {producto[1]:<40} Marca: {producto[2]:<20} Cantidad: {producto[3]:<15}")

    except sqlite3.Error as e:
        print(Fore.RED + Style.BRIGHT + f"Error al consultar los datos: {e}")
        return
    finally:
        if 'conexion' in locals():
            conexion.close()

# Funcion para cargar usuarios con restrcciones. Basado en ejercicio datos_clientes_clase12.py de mi autoria.
# guardado en archivo user.txt(basico para no complicarme). Segun IA combiene guardarlo e importar en variables de 
# entorno del sistema operativo.(os.environ) o  guardar las credenciales en un archivo externo (.env, config.json, etc.) o
# guardar usuarios en una bd con tabla usuarios con contraseña hasheada (ej. bcrypt)



def cargar_usuarios():
    usuarios = {}
    try:
        with open("user.txt", "r") as f:
            for linea in f:
                linea = linea.strip()
                if linea:  
                    usuario, contraseña, rol = linea.split(":")
                    usuarios[usuario] = {"password": contraseña, "rol" : rol}
    except FileNotFoundError:
        print(Fore.RED + "Archivo de usuarios no encontrado.")
    return usuarios

roles = {
    "admin": ["agregar", "actualizar", "eliminar", "ver", "buscar", "reporte"],
    "empleado": ["ver", "buscar", "reporte"]
}

def login(usuarios):
    print(Fore.GREEN + "=== Inicio de sesión ===")
    usuario = input("Usuario: ").strip()
    contraseña = input("Contraseña: ").strip()
    if usuario in usuarios and usuarios[usuario] ["password"] == contraseña:
        print(Fore.GREEN + "Acceso concedido")
        return usuarios[usuario] ["rol"]
    else:
        print(Fore.RED + "Usuario o contraseña incorrectos")
        return None

def menu(rol):
    inicializar_db()
    while True:
        print("\n===Gestión de Inventario===")
        print("1. Agregar producto")
        print("2. Ver productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Reporte bajo stock")
        print("7. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1" and "agregar" in roles[rol]:
            agregar_producto()
        elif opcion == "2" and "ver" in roles[rol]:
            ver_producto()
        elif opcion == "3" and "actualizar" in roles[rol]:
            actualizar_precio_o_cantidad()
        elif opcion == "4" and "eliminar" in roles[rol]:
            eliminar_producto()
        elif opcion == "5" and "buscar" in roles[rol]:
            buscar_producto()
        elif opcion == "6" and "reporte" in roles[rol]:
            reporte_productos_bajo_stock()
        elif opcion == "7":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print(Fore.YELLOW + "No tienes permisos para esa acción o la opción no es válida.")

if __name__ == "__main__":
    usuarios = cargar_usuarios()
    usuario = None
    while usuario is None:
        usuario = login(usuarios)
    menu(usuario)

