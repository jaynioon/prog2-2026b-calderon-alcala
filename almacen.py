"""Módulo de persistencia y bitácora de eventos del sistema escolar.

Contiene la clase Bitacora para delegación por composición y las funciones
principales de persistencia con la firma exacta del contrato:
guardar(sistema, ruta) y cargar(sistema, ruta), implementando la política
de arranque limpio ante archivos ausentes o dañados.
"""

from datetime import datetime
import json
import os
from typing import Any

from modelo import Alumno, Docente, Materia


class Bitacora:
    """Gestiona el registro cronológico de eventos del sistema (composición)."""

    def __init__(self) -> None:
        """Inicializa una bitácora vacía con su lista interna de eventos."""
        self._eventos: list[dict[str, str]] = []

    @property
    def eventos(self) -> tuple[dict[str, str], ...]:
        """Obtiene una tupla de solo lectura con los eventos registrados."""
        return tuple(self._eventos)

    def registrar_evento(self, accion: str, detalle: str) -> None:
        """Agrega un evento a la bitácora con marca de tiempo.

        Args:
            accion: Categoría del evento (ALTA, ASIGNACION, RECHAZO, PERSISTENCIA).
            detalle: Mensaje explicativo de lo ocurrido.
        """
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = {
            "fecha": marca_tiempo,
            "accion": accion.upper(),
            "detalle": detalle,
        }
        self._eventos.append(evento)

    def limpiar(self) -> None:
        """Reinicia la lista de eventos dejándola vacía."""
        self._eventos.clear()

    def to_list(self) -> list[dict[str, str]]:
        """Serializa los eventos a una lista para almacenamiento persistente.

        Returns:
            list[dict[str, str]]: Copia de la lista de eventos.
        """
        return [dict(e) for e in self._eventos]

    def cargar_eventos(self, lista_eventos: list[dict[str, Any]]) -> None:
        """Carga una lista de eventos previos a la bitácora.

        Args:
            lista_eventos: Lista de diccionarios con eventos históricos.
        """
        self._eventos.clear()
        for item in lista_eventos:
            if isinstance(item, dict) and "accion" in item and "detalle" in item:
                self._eventos.append({
                    "fecha": str(item.get("fecha", "")),
                    "accion": str(item.get("accion", "")),
                    "detalle": str(item.get("detalle", "")),
                })


def guardar(sistema: Any, ruta: str) -> None:
    """Escribe todo el estado del sistema en un archivo de almacenamiento.

    Firma exacta del contrato: guardar(sistema, ruta).

    Args:
        sistema: Instancia del sistema escolar a persistir.
        ruta: Ruta del archivo donde se guardará la información en JSON.
    """
    datos = sistema.obtener_datos_serializables()
    ruta_absoluta = os.path.abspath(ruta)
    directorio = os.path.dirname(ruta_absoluta)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    with open(ruta_absoluta, mode="w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    sistema.bitacora.registrar_evento(
        "PERSISTENCIA",
        f"Datos guardados exitosamente en '{ruta}'."
    )


def cargar(sistema: Any, ruta: str) -> None:
    """Recupera el estado del sistema desde un archivo de almacenamiento.

    Firma exacta del contrato: cargar(sistema, ruta).
    Implementa política de arranque limpio: si el archivo no existe, fue
    borrado o está dañado/corrupto, inicializa el sistema con registros vacíos
    sin provocar un error en tiempo de ejecución.

    Args:
        sistema: Instancia del sistema escolar donde se restaurará la información.
        ruta: Ruta del archivo JSON a leer.
    """
    ruta_absoluta = os.path.abspath(ruta)

    if not os.path.exists(ruta_absoluta):
        sistema.limpiar()
        sistema.bitacora.registrar_evento(
            "PERSISTENCIA",
            f"Arranque limpio: el archivo '{ruta}' no existe. Sistema inicializado vacío."
        )
        print(f"[Aviso] Archivo '{ruta}' no encontrado. Se inicia el sistema con registros vacíos.")
        return

    try:
        with open(ruta_absoluta, mode="r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            raise ValueError("El formato raíz del archivo de datos no es un diccionario válido.")

        sistema.limpiar()

        # Reconstruir personas
        for item in datos.get("personas", []):
            tipo = item.get("tipo")
            if tipo == "Alumno":
                alumno = Alumno.from_dict(item)
                sistema.registrar(alumno)
            elif tipo == "Docente":
                docente = Docente.from_dict(item)
                sistema.registrar(docente)

        # Reconstruir materias
        materias_datos = datos.get("materias", [])
        for m_item in materias_datos:
            materia = Materia.from_dict(m_item)
            sistema.registrar(materia)

        # Reconstruir asignaciones
        for m_item in materias_datos:
            clave = m_item.get("clave")
            for cod in m_item.get("inscritos", []):
                try:
                    sistema.asignar(cod, clave)
                except ValueError as err:
                    # Registrado si hubiera inconsistencia previa en el archivo
                    sistema.bitacora.registrar_evento("RECHAZO", f"Error al restaurar asignación: {err}")

        # Reconstruir bitácora
        eventos_previos = datos.get("bitacora", [])
        if isinstance(eventos_previos, list):
            sistema.bitacora.cargar_eventos(eventos_previos)

        sistema.bitacora.registrar_evento(
            "PERSISTENCIA",
            f"Datos cargados exitosamente desde '{ruta}'."
        )

    except (json.JSONDecodeError, KeyError, ValueError, OSError) as error:
        sistema.limpiar()
        sistema.bitacora.registrar_evento(
            "PERSISTENCIA",
            f"Arranque limpio tras error de lectura en '{ruta}': {error}. Sistema reiniciado vacío."
        )
        print(
            f"[Aviso] El archivo '{ruta}' está dañado o tiene formato inválido ({error}). "
            "Se inicia el sistema con registros vacíos."
        )
