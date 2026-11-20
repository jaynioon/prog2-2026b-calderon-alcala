"""Módulo de la clase principal del sistema escolar (tipo SIIAU).

Implementa de forma estricta el contrato requerido:
- registrar(objeto)
- asignar(identificador, clave)
- listar()
- guardar(sistema, ruta) / guardar(ruta)
- cargar(sistema, ruta) / cargar(ruta)

Cumple con composición (Bitácora), encapsulamiento, desacoplamiento y
polimorfismo estricto sin condicionales de tipo.
"""

from typing import Any

import almacen
from almacen import Bitacora
from modelo import Alumno, Docente, Materia, Persona


class Sistema:
    """Controlador central de la gestión escolar con delegación por composición."""

    def __init__(self) -> None:
        """Inicializa las estructuras internas de registros y la bitácora."""
        self._registros: dict[str, Persona] = {}
        self._materias: dict[str, Materia] = {}
        self._bitacora: Bitacora = Bitacora()

    @property
    def registros(self) -> dict[str, Persona]:
        """Obtiene un diccionario de solo lectura con las personas registradas."""
        return dict(self._registros)

    @property
    def materias(self) -> dict[str, Materia]:
        """Obtiene un diccionario de solo lectura con las materias registradas."""
        return dict(self._materias)

    @property
    def bitacora(self) -> Bitacora:
        """Obtiene la instancia de la bitácora del sistema (solo lectura)."""
        return self._bitacora

    def registrar(self, objeto: Any) -> None:
        """Da de alta una persona (Alumno, Docente) o un contenedor (Materia).

        Firma del contrato: registrar(objeto). No utiliza input() y valida
        los datos antes de aceptar la inserción.

        Args:
            objeto: Instancia de Alumno, Docente o Materia a registrar.

        Raises:
            ValueError: Si el objeto es de tipo no soportado o su identificador
                ya existe en el sistema.
        """
        if isinstance(objeto, Persona):
            codigo = objeto.codigo
            if codigo in self._registros:
                mensaje = f"El código '{codigo}' ya existe en el sistema."
                self._bitacora.registrar_evento("RECHAZO", mensaje)
                raise ValueError(mensaje)

            self._registros[codigo] = objeto
            self._bitacora.registrar_evento(
                "ALTA",
                f"Persona registrada: {codigo} - {objeto.nombre}"
            )

        elif isinstance(objeto, Materia):
            clave = objeto.clave
            if clave in self._materias:
                mensaje = f"La materia con clave '{clave}' ya existe en el sistema."
                self._bitacora.registrar_evento("RECHAZO", mensaje)
                raise ValueError(mensaje)

            self._materias[clave] = objeto
            self._bitacora.registrar_evento(
                "ALTA",
                f"Materia registrada: {clave} - {objeto.nombre} (Cupo: {objeto.cupo_maximo})"
            )

        else:
            tipo_recibido = type(objeto).__name__
            mensaje = (
                f"Tipo de objeto inválido para registrar: '{tipo_recibido}'. "
                "Se esperaba Alumno, Docente o Materia."
            )
            self._bitacora.registrar_evento("RECHAZO", mensaje)
            raise ValueError(mensaje)

    def registrar_materia(self, materia: Materia) -> None:
        """Método semántico del Hito 1 para registrar una materia.

        Delega directamente en el método registrar del contrato.

        Args:
            materia: Instancia de Materia a registrar.
        """
        self.registrar(materia)

    def asignar(self, identificador: str | int, clave: str) -> None:
        """Inscribe a una persona registrada dentro de una materia indicada.

        Firma del contrato: asignar(identificador, clave). No utiliza input().

        Args:
            identificador: Código escolar de 9 dígitos de la persona.
            clave: Clave alfanumérica de la materia destino.

        Raises:
            ValueError: Si la materia no existe, la persona no está registrada,
                la persona ya está inscrita en la materia o el cupo se ha agotado.
        """
        clave_limpia = str(clave).strip() if clave is not None else ""
        id_limpio = str(identificador).strip() if identificador is not None else ""

        if clave_limpia not in self._materias:
            mensaje = f"La clave del contenedor (Materia) no es válida o no existe: '{clave}'."
            self._bitacora.registrar_evento("RECHAZO", mensaje)
            raise ValueError(mensaje)

        if id_limpio not in self._registros:
            mensaje = f"La persona con identificador '{identificador}' no se encuentra registrada en el sistema."
            self._bitacora.registrar_evento("RECHAZO", mensaje)
            raise ValueError(mensaje)

        materia = self._materias[clave_limpia]
        persona = self._registros[id_limpio]

        try:
            materia.inscribir(persona)
        except ValueError as err:
            self._bitacora.registrar_evento("RECHAZO", str(err))
            raise

        self._bitacora.registrar_evento(
            "ASIGNACION",
            f"Asignado '{persona.nombre}' ({persona.codigo}) a la materia '{materia.nombre}' ({materia.clave})."
        )

    def listar(self) -> None:
        """Imprime todos los registros del sistema con polimorfismo estricto.

        Firma del contrato: listar(). Recorre las entidades e invoca describir()
        sin emplear if, type() ni isinstance() para consultar el tipo del objeto.
        """
        todos_los_elementos = list(self._registros.values()) + list(self._materias.values())
        if not todos_los_elementos:
            print("El sistema no tiene elementos registrados actualmente.")
            return

        for elemento in todos_los_elementos:
            print(elemento.describir())

    def guardar(self, ruta: str = "datos.json") -> None:
        """Guarda el estado del sistema delegando en el módulo almacen.

        Permite invocarse como método del contrato en la clase principal.

        Args:
            ruta: Ruta del archivo JSON destino.
        """
        almacen.guardar(self, ruta)

    def cargar(self, ruta: str = "datos.json") -> None:
        """Carga el estado del sistema delegando en el módulo almacen.

        Permite invocarse como método del contrato en la clase principal.

        Args:
            ruta: Ruta del archivo JSON a recuperar.
        """
        almacen.cargar(self, ruta)

    def limpiar(self) -> None:
        """Reinicia el estado del sistema a colecciones vacías."""
        self._registros.clear()
        self._materias.clear()
        self._bitacora.limpiar()

    def obtener_datos_serializables(self) -> dict[str, Any]:
        """Extrae el estado del sistema mediante métodos públicos de las entidades.

        Garantiza desacoplamiento sin acceder a atributos privados de otras clases.

        Returns:
            dict[str, Any]: Estructura lista para serialización JSON.
        """
        return {
            "personas": [p.to_dict() for p in self._registros.values()],
            "materias": [m.to_dict() for m in self._materias.values()],
            "bitacora": self._bitacora.to_list(),
        }
