import sqlite3

from database import obtener_conexion


LIMITE_SQLITE_INT = 9_223_372_036_854_775_807


def _mostrar_lista_productos(productos, titulo="Lista de productos"):
    """Función auxiliar interna para imprimir productos con formato uniforme."""
    if not productos:
        return

    print(f"\n============= {titulo} =============")
    for prod in productos:
        print(
            f"ID: {prod[0]} | "
            f"Nombre: {prod[1]} | "
            f"Descripción: {prod[2]} | "
            f"Cantidad: {prod[3]} | "
            f"Precio: ${prod[4]:.2f} | "
            f"Categoría: {prod[5]}"
        )


def agregar_producto():
    """Inserta un nuevo producto en la tabla productos."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        nombre = input("Ingrese el nombre del producto: ").strip()
        while len(nombre) < 3 or len(nombre) > 100:
            print("El nombre no puede estar vacío y debe tener entre 3 y 100 caracteres.")
            nombre = input("Ingrese el nombre del producto: ").strip()

        descripcion = input("Ingrese la descripción del producto: ").strip()
        while not descripcion:
            print("La descripción no puede estar vacía.")
            descripcion = input("Ingrese la descripción del producto: ").strip()

        cantidad = input("Ingrese la cantidad del producto: ").strip()
        while not cantidad.isdigit() or int(cantidad) > LIMITE_SQLITE_INT:
            print(
                "La cantidad debe ser un número entero válido (no puede ser excesivamente grande)."
            )
            cantidad = input("Ingrese la cantidad del producto: ").strip()
        cantidad = int(cantidad)

        precio = input("Ingrese el precio del producto: ").strip()
        while True:
            try:
                precio = float(precio)
                if precio < 0:
                    raise ValueError
                break
            except ValueError:
                print("El precio no puede estar vacío y debe ser un número positivo.")
                precio = input("Ingrese el precio del producto: ").strip()

        categoria = input("Ingrese la categoría del producto: ").strip()
        while not categoria:
            print("La categoría no puede estar vacía.")
            categoria = input("Ingrese la categoría del producto: ").strip()

        sql = """
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            """
        cursor.execute(sql,(nombre, descripcion, cantidad, precio, categoria))

        conexion.commit()
        print("\nProducto agregado exitosamente.")

    except (sqlite3.Error, OverflowError, ValueError) as e:
        print(f"Ocurrió un error al agregar el producto: {e}")
        conexion.rollback()

    finally:
        conexion.close()


def consultar_productos():
    """Recupera todos los registros de la tabla productos."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        productos = cursor.fetchall()

        if(len(productos) == 0):
            print("Aún no hay productos registrados.")
            return None

        _mostrar_lista_productos(productos)

        return productos

    except sqlite3.Error as e:
        print(f"Ocurrió un error al consultar los productos: {e}")
        return None

    finally:
        conexion.close()


def actualizar_producto():
    """Actualiza datos de un producto específico."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        productos = consultar_productos()
        if productos == None or len(productos) == 0:
            return

        ids_validos = {producto[0] for producto in productos}

        id_producto = input("Ingrese el ID del producto a actualizar: ").strip()
        while not id_producto.isdigit() or int(id_producto) not in ids_validos:
            print("Ingrese un ID válido de la lista mostrada.")
            id_producto = input("Ingrese el ID del producto a actualizar: ").strip()
        id_producto = int(id_producto)

        nuevo_precio = input("Ingrese el nuevo precio del producto: ").strip()
        while True:
            try:
                nuevo_precio = float(nuevo_precio)
                if nuevo_precio < 0:
                    raise ValueError
                break
            except ValueError:
                print(
                    "El precio no puede estar vacío y debe ser un número real positivo."
                )
                nuevo_precio = input("Ingrese el nuevo precio del producto: ").strip()

        nueva_cantidad = input("Ingrese la nueva cantidad del producto: ").strip()
        while not nueva_cantidad.isdigit():
            print("La cantidad no puede estar vacía y debe ser un número entero.")
            nueva_cantidad = input("Ingrese la nueva cantidad del producto: ").strip()
        nueva_cantidad = int(nueva_cantidad)

        sql = "UPDATE productos SET precio = ?, cantidad = ? WHERE id = ?"
        cursor.execute(sql,(nuevo_precio, nueva_cantidad, id_producto))

        conexion.commit()
        print(f"Producto con ID {id_producto} actualizado correctamente.")

        sql = "SELECT * FROM productos WHERE id = ?"
        cursor.execute(sql,(id_producto,))
        producto_actualizado = cursor.fetchone()

        _mostrar_lista_productos([producto_actualizado], "Producto Actualizado")

    except sqlite3.Error as e:
        print(f"Ocurrió un error al actualizar el producto: {e}")
        conexion.rollback()

    finally:
        conexion.close()


def eliminar_producto():
    """Elimina un producto específico."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        productos = consultar_productos()
        if productos == None or len(productos) == 0:
            return

        ids_validos = {producto[0] for producto in productos}

        id_producto = input("\nIngrese el ID del producto a eliminar: ").strip()
        while not id_producto.isdigit() or int(id_producto) not in ids_validos:
            print("Ingrese un ID válido de la lista mostrada.")
            id_producto = input("\nIngrese el ID del producto a eliminar: ").strip()
        id_producto = int(id_producto)

        sql = "DELETE FROM productos WHERE id = ?"
        cursor.execute(sql,(id_producto,))


        conexion.commit()
        print(f"Producto con ID {id_producto} eliminado correctamente.")

    except sqlite3.Error as e:
        print(f"Ocurrió un error al eliminar el producto: {e}")
        conexion.rollback()

    finally:
        conexion.close()


def buscar_producto():
    """Busca un producto específico por nombre, categoría o ID."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        productos = consultar_productos()
        if productos == None or len(productos) == 0:
            return

        opcion = input(
            "\nIngrese la opción de búsqueda (1: por nombre, 2: por categoría, 3: por ID): "
        ).strip()
        if opcion == "1":
            nombre = input("\nIngrese el nombre del producto a buscar: ").strip()
            sql = "SELECT * FROM productos WHERE nombre LIKE ?"
            cursor.execute(sql,(f"%{nombre}%",))
        elif opcion == "2":
            categoria = input("\nIngrese la categoría del producto a buscar: ").strip()
            sql = "SELECT * FROM productos WHERE categoria LIKE ?"
            cursor.execute(sql,(f"%{categoria}%",))
        elif opcion == "3":
            id_producto = input("\nIngrese el ID del producto a buscar: ").strip()
            while not id_producto.isdigit():
                print("El ID no puede estar vacío y debe ser un número entero.")
                id_producto = input("\nIngrese el ID del producto a buscar: ").strip()
            id_producto = int(id_producto)
            sql = "SELECT * FROM productos WHERE id = ?"
            cursor.execute(sql,(id_producto,))
        else:
            print("Opción no válida. Ingrese 1, 2 o 3.")
            return

        productos = cursor.fetchall()
        if len(productos) == 0:
            print("No se encontraron productos con ese criterio de búsqueda.")
        else:
            _mostrar_lista_productos(productos, "Resultados de la búsqueda")

    except sqlite3.Error as e:
        print(f"Ocurrió un error al buscar el producto: {e}")
        return None

    finally:
        conexion.close()

    return productos


def reporte_productos():
    """Muestra un reporte de productos que tengan una cantidad específica."""
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            print("Aún no hay productos registrados.")
            return

        cantidad = input("Mostrar productos con cantidad menor o igual a: ").strip()
        while not cantidad.isdigit():
            print("La cantidad no puede estar vacía y debe ser un número entero.")
            cantidad = input("Mostrar productos con cantidad menor o igual a: ").strip()
        cantidad = int(cantidad)

        sql = "SELECT * FROM productos WHERE cantidad <= ?"
        cursor.execute(sql,(cantidad,))
        productos = cursor.fetchall()

        if len(productos) == 0:
            print("No se encontraron productos con esa cantidad o menor.")
        else:
            _mostrar_lista_productos(productos, f"Reporte: Stock de productos con cantidad menor o igual a {cantidad}")

    except sqlite3.Error as e:
        print(f"Ocurrió un error al mostrar los productos: {e}")

    finally:
        conexion.close()
