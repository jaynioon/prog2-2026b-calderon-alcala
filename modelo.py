"""Módulo de modelos de dominio para el sistema escolar tipo SIIAU.

Define la jerarquía de herencia para personas (Persona, Alumno, Docente) y
el contenedor con cupo limitado (Materia), aplicando encapsulamiento estricto,
validación de datos y polimorfismo en los métodos de descripción.
"""


def _validar_texto_no_vacio(valor: str, nombre_campo: str) -> str:
    """Valida que un campo de texto no sea nulo, vacío ni contenga solo espacios.

    Args:
        valor: Cadena de texto a validar.
        nombre_campo: Nombre descriptivo del campo para el mensaje de error.

    Returns:
        str: Cadena limpia sin espacios en los extremos.

    Raises:
        ValueError: Si el valor no es cadena o está vacío.
    """
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{nombre_campo}' es obligatorio y no puede estar vacío.")
    return valor.strip()


def _validar_codigo_nueve_digitos(codigo: str | int) -> str:
    """Valida que un código escolar conste de exactamente 9 dígitos numéricos.

    Args:
        codigo: Código a validar como cadena o entero.

    Returns:
        str: Representación en cadena del código de 9 dígitos.

    Raises:
        ValueError: Si el código no tiene exactamente 9 dígitos numéricos.
    """
    if isinstance(codigo, bool) or not isinstance(codigo, (str, int)):
        raise ValueError("El código debe tener exactamente 9 dígitos numéricos.")

    codigo_str = str(codigo).strip()
    if not (codigo_str.isdigit() and len(codigo_str) == 9):
        raise ValueError(
            f"El código debe tener exactamente 9 dígitos numéricos (valor recibido: '{codigo}')."
        )
    return codigo_str


class Persona:
    """Clase base que representa a un miembro de la comunidad universitaria.

    Aplica encapsulamiento de atributos internos y define la base del
    polimorfismo mediante el método describir.
    """

    def __init__(self, codigo: str | int, nombre: str) -> None:
        """Inicializa una nueva persona validando código y nombre.

        Args:
            codigo: Identificador único de 9 dígitos.
            nombre: Nombre completo de la persona.

        Raises:
            ValueError: Si el código o el nombre no cumplen con el formato requerido.
        """
        self._codigo: str = _validar_codigo_nueve_digitos(codigo)
        self._nombre: str = _validar_texto_no_vacio(nombre, "nombre")

    @property
    def codigo(self) -> str:
        """Obtiene el código escolar de la persona (solo lectura)."""
        return self._codigo

    @property
    def nombre(self) -> str:
        """Obtiene el nombre de la persona (solo lectura)."""
        return self._nombre

    def describir(self) -> str:
        """Genera una descripción textual base de la persona.

        Returns:
            str: Cadena con el código y nombre formateados.
        """
        return f"Código: {self._codigo} | Nombre: {self._nombre}"

    def describirse(self) -> str:
        """Alias de compatibilidad con el diseño original del Hito 1."""
        return self.describir()

    def to_dict(self) -> dict:
        """Serializa la entidad a un diccionario público.

        Returns:
            dict: Representación serializable de la entidad.
        """
        return {
            "tipo": "Persona",
            "codigo": self._codigo,
            "nombre": self._nombre,
        }


class Alumno(Persona):
    """Representa a un estudiante inscrito en una carrera universitaria.

    Hereda de Persona y extiende su método de descripción con la carrera.
    """

    def __init__(self, codigo: str | int, nombre: str, carrera: str) -> None:
        """Inicializa un alumno validando datos base y carrera.

        Args:
            codigo: Código de 9 dígitos.
            nombre: Nombre del alumno.
            carrera: Nombre o sigla de la carrera académica.

        Raises:
            ValueError: Si algún dato es inválido o está vacío.
        """
        super().__init__(codigo, nombre)
        self._carrera: str = _validar_texto_no_vacio(carrera, "carrera")

    @property
    def carrera(self) -> str:
        """Obtiene la carrera del alumno (solo lectura)."""
        return self._carrera

    def describir(self) -> str:
        """Describe al alumno extendiendo la descripción de la clase base.

        Returns:
            str: Descripción completa del alumno utilizando super().describir().
        """
        return f"[Alumno] {super().describir()} | Carrera: {self._carrera}"

    def to_dict(self) -> dict:
        """Serializa los datos del alumno a un diccionario público.

        Returns:
            dict: Datos del alumno con su tipo específico.
        """
        return {
            "tipo": "Alumno",
            "codigo": self._codigo,
            "nombre": self._nombre,
            "carrera": self._carrera,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Alumno":
        """Reconstruye una instancia de Alumno desde un diccionario.

        Args:
            data: Diccionario con llaves 'codigo', 'nombre' y 'carrera'.

        Returns:
            Alumno: Nueva instancia reconstruida.
        """
        return cls(
            codigo=data["codigo"],
            nombre=data["nombre"],
            carrera=data["carrera"],
        )


class Docente(Persona):
    """Representa a un profesor asignado a un departamento académico.

    Hereda de Persona y extiende su método de descripción con el departamento.
    """

    def __init__(self, codigo: str | int, nombre: str, departamento: str) -> None:
        """Inicializa un docente validando datos base y departamento.

        Args:
            codigo: Código de 9 dígitos.
            nombre: Nombre del docente.
            departamento: Departamento académico al que pertenece.

        Raises:
            ValueError: Si algún dato es inválido o está vacío.
        """
        super().__init__(codigo, nombre)
        self._departamento: str = _validar_texto_no_vacio(departamento, "departamento")

    @property
    def departamento(self) -> str:
        """Obtiene el departamento académico del docente (solo lectura)."""
        return self._departamento

    def describir(self) -> str:
        """Describe al docente extendiendo la descripción de la clase base.

        Returns:
            str: Descripción completa del docente utilizando super().describir().
        """
        return f"[Docente] {super().describir()} | Departamento: {self._departamento}"

    def to_dict(self) -> dict:
        """Serializa los datos del docente a un diccionario público.

        Returns:
            dict: Datos del docente con su tipo específico.
        """
        return {
            "tipo": "Docente",
            "codigo": self._codigo,
            "nombre": self._nombre,
            "departamento": self._departamento,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Docente":
        """Reconstruye una instancia de Docente desde un diccionario.

        Args:
            data: Diccionario con llaves 'codigo', 'nombre' y 'departamento'.

        Returns:
            Docente: Nueva instancia reconstruida.
        """
        return cls(
            codigo=data["codigo"],
            nombre=data["nombre"],
            departamento=data["departamento"],
        )


class Materia:
    """Representa una materia universitaria con cupo límite para personas asignadas."""

    def __init__(self, clave: str, nombre: str, cupo_maximo: int) -> None:
        """Inicializa una materia validando clave, nombre y cupo.

        Args:
            clave: Clave única alfanumérica de la materia.
            nombre: Nombre de la asignatura.
            cupo_maximo: Capacidad máxima entera mayor a cero.

        Raises:
            ValueError: Si los datos son inválidos o el cupo no es entero positivo.
        """
        self._clave: str = _validar_texto_no_vacio(clave, "clave")
        self._nombre: str = _validar_texto_no_vacio(nombre, "nombre")

        if isinstance(cupo_maximo, bool) or not isinstance(cupo_maximo, int) or cupo_maximo <= 0:
            raise ValueError(
                f"El cupo máximo debe ser un número entero mayor que cero (recibido: {cupo_maximo})."
            )

        self._cupo_maximo: int = cupo_maximo
        self._inscritos: list[Persona] = []

    @property
    def clave(self) -> str:
        """Obtiene la clave de la materia (solo lectura)."""
        return self._clave

    @property
    def nombre(self) -> str:
        """Obtiene el nombre de la materia (solo lectura)."""
        return self._nombre

    @property
    def cupo_maximo(self) -> int:
        """Obtiene el cupo máximo permitido (solo lectura)."""
        return self._cupo_maximo

    @property
    def inscritos(self) -> tuple[Persona, ...]:
        """Obtiene una tupla inmutable con las personas inscritas (solo lectura)."""
        return tuple(self._inscritos)

    def hay_cupo(self) -> bool:
        """Verifica si la materia cuenta con cupo disponible para otra inscripción.

        Returns:
            bool: True si hay cupo disponible, False en caso contrario.
        """
        return len(self._inscritos) < self._cupo_maximo

    def inscribir(self, persona: Persona) -> None:
        """Inscribe a una persona validando pertenencia, duplicidad y cupo.

        Args:
            persona: Instancia de Persona (Alumno o Docente) a inscribir.

        Raises:
            ValueError: Si el objeto no es Persona, ya está inscrito o no hay cupo.
        """
        if not isinstance(persona, Persona):
            raise ValueError("Solo se pueden inscribir instancias derivadas de Persona.")

        if any(p.codigo == persona.codigo for p in self._inscritos):
            raise ValueError(
                f"La persona con código '{persona.codigo}' ya se encuentra asignada a esta clase."
            )

        if not self.hay_cupo():
            raise ValueError(
                f"La Materia '{self._clave}' ha alcanzado su cupo máximo ({self._cupo_maximo}) "
                "y no admite más registros."
            )

        self._inscritos.append(persona)

    def describir(self) -> str:
        """Genera una descripción textual del contenedor y su ocupación actual.

        Returns:
            str: Descripción formateada con clave, nombre y relación de cupo.
        """
        return (
            f"[Materia] Clave: {self._clave} | Nombre: {self._nombre} | "
            f"Ocupación: {len(self._inscritos)}/{self._cupo_maximo}"
        )

    def describirse(self) -> str:
        """Alias de compatibilidad con el diseño original del Hito 1."""
        return self.describir()

    def to_dict(self) -> dict:
        """Serializa la materia y la lista de códigos inscritos a un diccionario público.

        Returns:
            dict: Representación serializable sin exponer atributos privados.
        """
        return {
            "clave": self._clave,
            "nombre": self._nombre,
            "cupo_maximo": self._cupo_maximo,
            "inscritos": [p.codigo for p in self._inscritos],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Materia":
        """Reconstruye una instancia de Materia desde un diccionario.

        Args:
            data: Diccionario con llaves 'clave', 'nombre' y 'cupo_maximo'.

        Returns:
            Materia: Nueva instancia con lista de inscritos vacía (a poblar por el sistema).
        """
        return cls(
            clave=data["clave"],
            nombre=data["nombre"],
            cupo_maximo=data["cupo_maximo"],
        )
