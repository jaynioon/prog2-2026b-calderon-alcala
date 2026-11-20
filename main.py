"""Demostración integral y prueba ejecutable del sistema escolar (tipo SIIAU).

Ejecuta el ciclo de vida completo del sistema:
1. Prueba de arranque limpio con archivo inexistente.
2. Altas válidas de Alumnos, Docentes y Materias mediante el contrato.
3. Casos de prueba de rechazo en altas (validaciones de código, campos vacíos, duplicados y tipos).
4. Asignaciones válidas al contenedor con cupo.
5. Casos de prueba de rechazo en asignaciones (materias inexistentes, no registrados, duplicados y cupo lleno).
6. Listado polimórfico estricto.
7. Persistencia completa (guardar y recargar en nueva instancia).
8. Prueba de arranque limpio ante archivo dañado/corrupto.

Todas las excepciones son capturadas e informadas sin interrumpir la ejecución
con tracebacks no controlados.
"""

import os
import almacen
from modelo import Alumno, Docente, Materia
from sistema import Sistema


def probar_caso_invalido(titulo: str, accion) -> None:
    """Ejecuta una acción que se espera sea rechazada y muestra el resultado controlado.

    Args:
        titulo: Breve descripción de la prueba negativa.
        accion: Función o lambda a ejecutar.
    """
    print(f"  [Caso de prueba] {titulo}")
    try:
        accion()
        print("    --> ERROR INESPERADO: La validación no rechazó la operación.")
    except ValueError as err:
        print(f"    --> ÉXITO: Rechazo correcto con ValueError -> \"{err}\"")
    except Exception as err:
        print(f"    --> ERROR: Se esperaba ValueError pero ocurrió {type(err).__name__}: {err}")


def main() -> None:
    """Función principal que orquesta todas las pruebas de aceptación."""
    print("=" * 75)
    print("DEMOSTRACIÓN DEL SISTEMA ESCOLAR (PROYECTO INTEGRADOR - HITO 2)")
    print("=" * 75)

    ruta_datos = "datos_prueba.json"
    ruta_corrupta = "datos_corruptos.json"

    # Limpieza previa de entorno si existían archivos residuales
    for r in (ruta_datos, ruta_corrupta):
        if os.path.exists(r):
            try:
                os.remove(r)
            except OSError:
                pass

    sistema = Sistema()

    # -------------------------------------------------------------------------
    # 1. Prueba de Arranque Limpio (Archivo ausente)
    # -------------------------------------------------------------------------
    print("\n--- 1. PRUEBA DE ARRANQUE LIMPIO (ARCHIVO AUSENTE) ---")
    print(f"Intentando cargar desde archivo inexistente: '{ruta_datos}'...")
    almacen.cargar(sistema, ruta_datos)
    print(f"Registros en sistema tras arranque limpio: {len(sistema.registros)}")
    print(f"Materias en sistema tras arranque limpio: {len(sistema.materias)}")

    # -------------------------------------------------------------------------
    # 2. Altas Válidas
    # -------------------------------------------------------------------------
    print("\n--- 2. ALTAS VÁLIDAS MEDIANTE EL CONTRATO registrar(objeto) ---")
    alumno1 = Alumno("220000001", "Ana Gomez", "Licenciatura en Informatica")
    alumno2 = Alumno("220000002", "Bernardo Lopez", "Ingenieria en Computacion")
    alumno3 = Alumno("220000003", "Carlos Perez", "Ingenieria Biomedica")
    docente1 = Docente("110000001", "Dr. Fernando Ruiz", "Ciencias Computacionales")

    # Registrar el contenedor también por registrar(objeto)
    materia_prog = Materia("I5886", "Programacion II", 2)
    materia_bd = Materia("I5887", "Bases de Datos", 1)

    for item in (alumno1, alumno2, alumno3, docente1, materia_prog, materia_bd):
        sistema.registrar(item)
        print(f"  Registrado exitosamente: {item.describir()}")

    # -------------------------------------------------------------------------
    # 3. Casos de Rechazo al Dar de Alta
    # -------------------------------------------------------------------------
    print("\n--- 3. CASOS DE RECHAZO AL DAR DE ALTA (VALIDACIONES) ---")

    probar_caso_invalido(
        "Código con menos de 9 dígitos ('12345')",
        lambda: Alumno("12345", "Diana Cruz", "Informatica")
    )
    probar_caso_invalido(
        "Código con más de 9 dígitos ('12345678901')",
        lambda: Alumno("12345678901", "Diana Cruz", "Informatica")
    )
    probar_caso_invalido(
        "Código con caracteres alfabéticos ('22000000A')",
        lambda: Alumno("22000000A", "Diana Cruz", "Informatica")
    )
    probar_caso_invalido(
        "Nombre vacío o solo espacios ('   ')",
        lambda: Alumno("220000004", "   ", "Informatica")
    )
    probar_caso_invalido(
        "Carrera vacía en Alumno ('')",
        lambda: Alumno("220000004", "Elena Mora", "")
    )
    probar_caso_invalido(
        "Departamento vacío en Docente ('   ')",
        lambda: Docente("110000002", "Dra. Laura Vega", "   ")
    )
    probar_caso_invalido(
        "Materia con cupo menor o igual a cero (0)",
        lambda: Materia("I5888", "Redes de Computadoras", 0)
    )
    probar_caso_invalido(
        "Código de persona duplicado en el sistema ('220000001')",
        lambda: sistema.registrar(Alumno("220000001", "Ana Gomez Duplicada", "Informatica"))
    )
    probar_caso_invalido(
        "Clave de materia duplicada en el sistema ('I5886')",
        lambda: sistema.registrar(Materia("I5886", "Programacion Duplicada", 5))
    )
    probar_caso_invalido(
        "Registrar un objeto de tipo no soportado (cadena 'Texto Invalido')",
        lambda: sistema.registrar("Texto Invalido")
    )

    # -------------------------------------------------------------------------
    # 4. Asignaciones Válidas
    # -------------------------------------------------------------------------
    print("\n--- 4. ASIGNACIONES VÁLIDAS MEDIANTE asignar(identificador, clave) ---")
    sistema.asignar("220000001", "I5886")
    print("  Asignada 'Ana Gomez' a 'Programacion II' (Cupo 1/2).")

    sistema.asignar("220000002", "I5886")
    print("  Asignado 'Bernardo Lopez' a 'Programacion II' (Cupo 2/2 - Lleno).")

    sistema.asignar("110000001", "I5887")
    print("  Asignado 'Dr. Fernando Ruiz' a 'Bases de Datos' (Cupo 1/1 - Lleno).")

    # -------------------------------------------------------------------------
    # 5. Casos de Rechazo al Asignar
    # -------------------------------------------------------------------------
    print("\n--- 5. CASOS DE RECHAZO AL ASIGNAR (VALIDACIONES) ---")

    probar_caso_invalido(
        "Asignar a una materia que no existe ('MAT999')",
        lambda: sistema.asignar("220000001", "MAT999")
    )
    probar_caso_invalido(
        "Asignar a una persona que no existe ('999999999')",
        lambda: sistema.asignar("999999999", "I5886")
    )
    probar_caso_invalido(
        "Asignar dos veces a la misma persona en la misma materia ('220000001' en 'I5886')",
        lambda: sistema.asignar("220000001", "I5886")
    )
    probar_caso_invalido(
        "Asignar a una materia con cupo agotado ('220000003' en 'I5886', cupo 2/2)",
        lambda: sistema.asignar("220000003", "I5886")
    )

    # -------------------------------------------------------------------------
    # 6. Listado con Polimorfismo Estricto
    # -------------------------------------------------------------------------
    print("\n--- 6. LISTADO DE REGISTROS (POLIMORFISMO ESTRICTO CON describir()) ---")
    sistema.listar()

    # -------------------------------------------------------------------------
    # 7. Persistencia y Reconstrucción
    # -------------------------------------------------------------------------
    print("\n--- 7. PERSISTENCIA: GUARDAR Y RECUPERAR ---")
    print(f"Guardando datos en '{ruta_datos}'...")
    almacen.guardar(sistema, ruta_datos)
    print("Guardado exitoso.")

    print("\nCreando nueva instancia limpia de Sistema y cargando datos...")
    sistema_recuperado = Sistema()
    almacen.cargar(sistema_recuperado, ruta_datos)

    print("Listando el nuevo sistema restaurado desde el archivo:")
    sistema_recuperado.listar()

    print("\nVerificando asignaciones recuperadas:")
    mat_recuperada = sistema_recuperado.materias["I5886"]
    print(f"  Materia '{mat_recuperada.nombre}' tiene {len(mat_recuperada.inscritos)} inscritos:")
    for ins in mat_recuperada.inscritos:
        print(f"    - {ins.describir()}")

    # -------------------------------------------------------------------------
    # 8. Prueba de Arranque Limpio con Archivo Dañado/Corrupto
    # -------------------------------------------------------------------------
    print("\n--- 8. PRUEBA DE ARRANQUE LIMPIO (ARCHIVO CORRUPTO) ---")
    with open(ruta_corrupta, mode="w", encoding="utf-8") as f_corrupto:
        f_corrupto.write("{ este no es un json valido : corrupto 12345 ")

    sistema_corrupto = Sistema()
    print(f"Intentando cargar desde archivo corrupto: '{ruta_corrupta}'...")
    almacen.cargar(sistema_corrupto, ruta_corrupta)
    print(f"Registros en sistema tras fallo de archivo: {len(sistema_corrupto.registros)}")
    print(f"Materias en sistema tras fallo de archivo: {len(sistema_corrupto.materias)}")
    print("El sistema no crasheó y quedó listo para operar vacío.")

    # Limpieza final de archivos de prueba
    for r in (ruta_datos, ruta_corrupta):
        if os.path.exists(r):
            try:
                os.remove(r)
            except OSError:
                pass

    print("\n" + "=" * 75)
    print("TODAS LAS PRUEBAS Y DEMOSTRACIONES CONCLUYERON CON ÉXITO.")
    print("=" * 75)


if __name__ == "__main__":
    main()
