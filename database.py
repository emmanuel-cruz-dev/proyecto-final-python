import sqlite3

def crear_base_datos():
    """Crea la base de datos 'inventario.db'."""

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    """)

    print("Tabla 'productos' creada exitosamente.")

    conexion.commit()
    conexion.close()


def obtener_conexion():
    """Obtiene la conexión a la base de datos."""
    return sqlite3.connect("inventario.db")
