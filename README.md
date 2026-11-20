Karol Violeta Alcala Serratos
# Proyecto Integrador de Programación II — Hito 2

**Centro Universitario de Guadalajara | Universidad de Guadalajara — Ciclo 2026B**  
**Profesora:** Martha Ulloa Ramírez  
**Opción Elegida:** Opción A — Sistema Escolar (tipo SIIAU)  
**Nombre del Repositorio Público:** `prog2-2026b-calderon-alcala`

---

## 1. Integrantes del Equipo

* **Jairo Alberto Calderon Davalos** (Código: 222834835)
* **Karol Violeta Alcala Serratos** (Código: 222751719)

---

## 2. Qué hace el sistema

El proyecto implementa una plataforma de gestión académica tipo SIIAU orientada a objetos en Python. El sistema permite dar de alta dos tipos de personas universitarias (**Alumnos** y **Docentes**) que comparten una clase base común (**Persona**), así como dar de alta materias académicas (**Materia**) con cupo límite restringido. 

El sistema gestiona la asignación (inscripción) de personas a materias asegurando que se cumplan todas las reglas de negocio: no duplicidad de códigos, validación de formato numérico de 9 dígitos, campos obligatorios no vacíos, verificación de cupo máximo disponible y prevención de doble inscripción en una misma asignatura. Además, cuenta con auditoría de operaciones por composición (**Bitácora**) y persistencia de datos en JSON con política de **arranque limpio** ante archivos inexistentes o dañados.

---

## 3. Cómo se ejecuta

El proyecto no requiere dependencias externas; funciona con Python estándar (versión 3.10 o superior).

Para ejecutar la demostración completa y comprobar todas las pruebas de validación, polimorfismo y persistencia:

```bash
python main.py
```

---

## 4. Estructura y explicación de cada archivo

La solución se organizó con alta cohesión y bajo acoplamiento en archivos sueltos en la raíz:

* **`modelo.py`**: Contiene las clases de dominio. Define la jerarquía de herencia (`Persona` como clase base, `Alumno` y `Docente` como clases derivadas extendiendo `describir()` obligatoriamente con `super().describir()`) y el contenedor con cupo (`Materia`). Implementa encapsulamiento estricto (atributos internos prefijados con `_`, expuestos con `@property` de solo lectura) y métodos públicos de serialización (`to_dict` y `from_dict`).
* **`almacen.py`**: Módulo responsable de la bitácora y la persistencia en disco. Define la clase `Bitacora` (utilizada por composición dentro de `Sistema` para registrar altas, asignaciones, rechazos y persistencia) y las funciones con firma exacta del contrato: `guardar(sistema, ruta)` y `cargar(sistema, ruta)`. Implementa el arranque limpio capturando errores de archivo ausente o corrupto.
* **`sistema.py`**: Define la clase principal `Sistema`, la cual orquesta la lógica de negocio cumpliendo de forma estricta los 5 métodos del contrato unificado (`registrar`, `asignar`, `listar`, `guardar`, `cargar`). No utiliza `input()` y delega el listado de forma polimórfica sin recurrir a comprobaciones de tipo (`if`, `type()` o `isinstance()`).
* **`main.py`**: Script ejecutable de demostración y pruebas de aceptación. Evalúa arranque limpio ante archivo inexistente, altas válidas, todos los casos de rechazo previstos (atrapando `ValueError` sin detener el programa con tracebacks rojos), asignaciones válidas, rechazos por cupo o duplicidad, listado polimórfico, persistencia completa y recuperación ante archivos JSON corruptos.

---

## 5. Ejemplo de uso del contrato

El sistema se puede controlar e integrar importando sus clases y llamando exclusivamente a los métodos del contrato:

```python
from modelo import Alumno, Docente, Materia
from sistema import Sistema

# 1. Instanciar el sistema principal
sistema = Sistema()

# 2. Registrar entidades (Personas y Contenedor)
alumno = Alumno("220000001", "Ana Gomez", "Licenciatura en Informatica")
docente = Docente("110000001", "Dr. Fernando Ruiz", "Ciencias Computacionales")
materia = Materia("I5886", "Programacion II", 2)

sistema.registrar(alumno)
sistema.registrar(docente)
sistema.registrar(materia)

# 3. Asignar personas al contenedor con cupo
sistema.asignar("220000001", "I5886")
sistema.asignar("110000001", "I5886")

# 4. Listar de forma polimórfica (invoca describir() en cada objeto)
sistema.listar()

# 5. Persistencia mediante el contrato
sistema.guardar("datos_escolares.json")

# 6. Carga en una nueva instancia limpia
sistema_nuevo = Sistema()
sistema_nuevo.cargar("datos_escolares.json")
sistema_nuevo.listar()
```

---

## 6. Tabla de validaciones y manejo de errores

Todas las validaciones rechazan datos erróneos lanzando excepciones de tipo `ValueError` con mensajes claros y descriptivos, evitando cualquier interrupción anormal del programa:

| Operación | Intento / Situación inválida | Regla aplicada | Excepción y Mensaje |
| :--- | :--- | :--- | :--- |
| **Alta** | Código con menos de 9 dígitos | Longitud exacta de 9 dígitos | `ValueError: El código debe tener exactamente 9 dígitos numéricos (valor recibido: '...').` |
| **Alta** | Código con más de 9 dígitos | Longitud exacta de 9 dígitos | `ValueError: El código debe tener exactamente 9 dígitos numéricos (valor recibido: '...').` |
| **Alta** | Código con letras o caracteres especiales | Debe ser puramente numérico | `ValueError: El código debe tener exactamente 9 dígitos numéricos (valor recibido: '...').` |
| **Alta** | Nombre vacío o solo espacios | Campo obligatorio no vacío | `ValueError: El campo 'nombre' es obligatorio y no puede estar vacío.` |
| **Alta** | Carrera o Departamento vacío | Campo obligatorio no vacío | `ValueError: El campo 'carrera'/'departamento' es obligatorio y no puede estar vacío.` |
| **Alta** | Cupo máximo menor o igual a cero | Debe ser entero positivo > 0 | `ValueError: El cupo máximo debe ser un número entero mayor que cero (recibido: ...).` |
| **Alta** | Código de persona ya registrado | No duplicidad de identificadores | `ValueError: El código '...' ya existe en el sistema.` |
| **Alta** | Clave de materia ya registrada | No duplicidad de claves | `ValueError: La materia con clave '...' ya existe en el sistema.` |
| **Alta** | Pasar objeto que no sea Alumno, Docente ni Materia | Tipo admitido por el sistema | `ValueError: Tipo de objeto inválido para registrar: '...'. Se esperaba Alumno, Docente o Materia.` |
| **Asignación** | Asignar a materia inexistente | El contenedor debe existir | `ValueError: La clave del contenedor (Materia) no es válida o no existe: '...'.` |
| **Asignación** | Asignar persona no registrada | El objeto debe estar en el sistema | `ValueError: La persona con identificador '...' no se encuentra registrada en el sistema.` |
| **Asignación** | Asignar dos veces a la misma persona en la misma materia | No se permite doble inscripción | `ValueError: La persona con código '...' ya se encuentra asignada a esta clase.` |
| **Asignación** | Asignar cuando ya no hay cupo disponible | No rebasar cupo máximo | `ValueError: La Materia '...' ha alcanzado su cupo máximo (...) y no admite más registros.` |
| **Carga** | Archivo no existe o fue borrado | Arranque limpio | Notificación informativa y reinicio de registros en vacío sin error de ejecución. |
| **Carga** | Archivo con JSON corrupto o roto | Arranque limpio | Notificación informativa y reinicio de registros en vacío sin interrumpir la ejecución. |

---

## 7. Qué cambió respecto al diseño del Hito 1 y por qué

> *Tal como lo solicita la Sección 6 (página 4) de la especificación oficial del proyecto integrador:*
>
> Durante la implementación del Hito 2 realizamos tres ajustes arquitectónicos respecto al diseño preliminar propuesto en el Hito 1:
> 1. **Estandarización del método polimórfico:** En el diagrama del Hito 1 habíamos nombrado al método como `describirse()`. Para alinearnos al 100% con el estándar del contrato unificado y la rúbrica de evaluación de la profesora, se renombró formalmente a `describir()`, asegurando que `Alumno` y `Docente` llamen obligatoriamente a `super().describir()`. Se mantuvo además `describirse()` como alias para garantizar total compatibilidad con el diagrama original.
> 2. **Refinamiento de la persistencia y la composición:** En el Hito 1 habíamos dibujado una clase `Almacen` contenida en `Sistema`. Para satisfacer con rigor el requisito de la Unidad 3 (composición) y el de la Unidad 4 (persistencia desacoplada), se creó la clase `Bitacora` para que `Sistema` *tenga una* bitácora y le delegue la auditoría cronológica de eventos (altas, asignaciones, rechazos y persistencia). Paralelamente, la persistencia en disco se implementó en `almacen.py` mediante las funciones libres requeridas por el contrato: `guardar(sistema, ruta)` y `cargar(sistema, ruta)`, con soporte completo de arranque limpio ante archivos faltantes o corruptos.
> 3. **Encapsulamiento estricto y serialización pública:** Se aseguraron todos los atributos internos con guion bajo (`_`) y propiedades `@property` de solo lectura, agregando métodos públicos de serialización (`to_dict` y `from_dict`) en las clases de modelo. Esto previene que los módulos de persistencia o el sistema accedan directamente a los atributos privados de las entidades, cumpliendo con la rúbrica de bajo acoplamiento.
## Integrantes
Jairo Calderon
