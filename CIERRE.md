# Documento de Cierre — Proyecto Integrador Programación II

## 1. Cambios respecto al diseño del Hito 1
Durante la etapa de programación (Hito 2 y Hito 3) mantuvimos la jerarquía principal de herencia (`Persona` como clase base y `Alumno` y `Docente` como subclases) así como la composición entre `Sistema` y `Bitacora`. Sin embargo, realizamos ajustes importantes para cumplir estrictamente con el contrato de evaluación y desacoplar el código:
* Se unificó el método de descripción polimórfica bajo el nombre `describir()` (conservando `describirse()` como alias de compatibilidad) para evitar cualquier condicional de tipo al listar.
* Se centralizó el alta de personas y materias dentro del método único `registrar(objeto)` del contrato, delegando `registrar_materia()` hacia él.
* Se añadieron métodos públicos de serialización (`to_dict()` y `from_dict()`) en las entidades para que `almacen.py` pudiera guardar y reconstruir el estado completo en JSON sin acceder a atributos privados de otras clases.

## 2. Lo más difícil del desarrollo
El mayor reto técnico fue diseñar las validaciones defensivas y la persistencia con arranque limpio sin romper el encapsulamiento. Garantizar que ningún dato inválido (códigos distintos a 9 dígitos, cadenas vacías con espacios, registros duplicados o materias con cupo agotado) detuviera el programa con un error no controlado exigió validar tanto en los constructores como en las operaciones de asignación, asegurando siempre el lanzamiento controlado de `ValueError`. Asimismo, sincronizar el trabajo en pareja mediante GitHub y resolver conflictos de fusión (`merge conflicts`) requirió disciplina al hacer `pull` y `push`.

## 3. Qué haríamos distinto
Si volviéramos a iniciar el proyecto, comenzaríamos a escribir las pruebas unitarias automatizadas (`pruebas.py`) desde el Hito 2 en paralelo con cada clase programada, en lugar de dejarlas hasta el final. También definiríamos desde el diagrama inicial los métodos de serialización pública para facilitar desde el principio la conexión entre el modelo y el módulo de almacenamiento.