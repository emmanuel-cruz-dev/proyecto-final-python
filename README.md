# Sistema de Gestión de Inventario

Aplicación de consola desarrollada en Python para la gestión de un inventario de productos, utilizando **SQLite** como motor de base de datos.

Proyecto final del curso **Iniciación a la Programación con Python** — Talento Tech.

## Descripción

El programa permite administrar un inventario de productos a través de un menú interactivo por terminal, ofreciendo operaciones de alta, consulta, actualización, eliminación, búsqueda y reportes sobre una base de datos SQLite (`inventario.db`), la cual se crea automáticamente al ejecutar la aplicación.

## Funcionalidades

- **Registrar producto**: agrega un nuevo producto al inventario (nombre, descripción, cantidad, precio y categoría), con validación de todos los datos ingresados.
- **Mostrar productos**: lista todos los productos registrados en la base de datos.
- **Actualizar producto**: modifica el precio y la cantidad de un producto existente a partir de su ID.
- **Eliminar producto**: elimina un producto del inventario a partir de su ID.
- **Búsqueda de productos**: permite buscar productos por nombre, categoría o ID.
- **Reporte de stock**: muestra los productos cuya cantidad es igual o inferior a un límite indicado por el usuario/a, útil para detectar productos con bajo stock.

## Estructura del proyecto

```
├── main.py         # Punto de entrada del programa, contiene el bucle del menú principal
├── database.py     # Creación de la base de datos y manejo de la conexión
├── menu.py         # Impresión del menú principal por consola
├── productos.py     # Lógica de negocio: CRUD y funciones auxiliares sobre productos
└── inventario.db    # Base de datos SQLite (se genera automáticamente, no incluida en el repositorio)
```

## Base de datos

La tabla `productos` tiene la siguiente estructura:

| Campo         | Tipo    | Restricciones             |
|---------------|---------|----------------------------|
| `id`          | INTEGER | Clave primaria, autoincremental |
| `nombre`      | TEXT    | No nulo                   |
| `descripcion` | TEXT    |                            |
| `cantidad`    | INTEGER | No nulo                   |
| `precio`      | REAL    | No nulo                   |
| `categoria`   | TEXT    |                            |

## Requisitos

- Python 3.x
- No requiere librerías externas (utiliza únicamente el módulo `sqlite3` de la biblioteca estándar)

## Ejecución

1. Clonar o descargar el repositorio.
2. Ejecutar el archivo principal:

```bash
python main.py
```

3. Al ejecutarse por primera vez, se creará automáticamente el archivo `inventario.db` con la tabla `productos`.
4. Navegar por las opciones del menú ingresando el número correspondiente.

## Autor

Emmanuel Cruz
