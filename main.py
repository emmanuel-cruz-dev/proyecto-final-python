# Entrega final - Python
# Curso Python - Talento Tech
# Alumno: Emmanuel Cruz

from menu import mostrar_menu
from productos import agregar_producto, consultar_productos, actualizar_producto, eliminar_producto, buscar_producto, reporte_productos
from database import crear_base_datos

crear_base_datos()

opcion = 0

while opcion != 7:
    mostrar_menu()

    input_opcion = input("Seleccione una opción: ").strip()
    if input_opcion.isdigit():
        opcion = int(input_opcion)
    else:
        print("Opción no válida. Ingrese un número del 1 al 7.")
        continue

    if opcion == 1:
        agregar_producto()
    elif opcion == 2:
        consultar_productos()
    elif opcion == 3:
        actualizar_producto()
    elif opcion == 4:
        eliminar_producto()
    elif opcion == 5:
        buscar_producto()
    elif opcion == 6:
        reporte_productos()
    elif opcion == 7:
        print("Saliendo del sistema, hasta luego.")
    else:
        print("Opción no válida. Ingrese un número del 1 al 7.")

print("Fin del programa.")
