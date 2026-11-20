"""Suite de pruebas automáticas del sistema escolar (Hito 3).

Cubre casos normales de operación, polimorfismo, encapsulamiento,
persistencia en JSON y arranque limpio ante archivos ausentes o dañados.
"""

import os
import unittest
import almacen
from modelo import Alumno, Docente, Materia
from sistema import Sistema


class TestSistemaEscolar(unittest.TestCase):
    """Pruebas unitarias para el sistema escolar tipo SIIAU."""

    def setUp(self) -> None:
        """Prepara un sistema limpio antes de cada prueba."""
        self.sistema = Sistema()
        self.archivo_test = "test_datos_temp.json"
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)

    def tearDown(self) -> None:
        """Elimina archivos temporales al terminar cada prueba."""
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)

    def test_01_registrar_alumno_y_docente_validos(self) -> None:
        """Verifica el alta correcta de Alumno y Docente con código de 9 dígitos."""
        alumno = Alumno("220000001", "Laura Méndez", "Ingeniería en Computación")
        docente = Docente("110000001", "Dr. Roberto Silva", "Ciencias Computacionales")

        self.sistema.registrar(alumno)
        self.sistema.registrar(docente)

        self.assertEqual(len(self.sistema.registros), 2)
        self.assertIn("220000001", self.sistema.registros)
        self.assertIn("110000001", self.sistema.registros)

    def test_02_asignar_persona_a_materia_con_cupo(self) -> None:
        """Verifica la inscripción correcta dentro del límite de cupo de una materia."""
        alumno = Alumno("220000002", "Miguel Torres", "Licenciatura en Informática")
        materia = Materia("I5886", "Programación II", 2)

        self.sistema.registrar(alumno)
        self.sistema.registrar(materia)
        self.sistema.asignar("220000002", "I5886")

        materia_guardada = self.sistema.materias["I5886"]
        self.assertEqual(len(materia_guardada.inscritos), 1)
        self.assertEqual(materia_guardada.inscritos[0].codigo, "220000002")

    def test_03_polimorfismo_describir_sin_condicionales(self) -> None:
        """Comprueba que Alumno y Docente se describen distinto mediante herencia."""
        alumno = Alumno("220000003", "Sofía Navarro", "Ingeniería Biomédica")
        docente = Docente("110000002", "Mtra. Elena Ortiz", "Electrónica")

        self.assertIn("[Alumno]", alumno.describir())
        self.assertIn("Ingeniería Biomédica", alumno.describir())
        self.assertIn("[Docente]", docente.describir())
        self.assertIn("Electrónica", docente.describir())

    def test_04_persistencia_guardar_y_cargar(self) -> None:
        """Verifica que la información y asignaciones sobreviven al guardar y recargar."""
        alumno = Alumno("220000004", "Diego Ríos", "Ingeniería en Computación")
        materia = Materia("I5887", "Bases de Datos", 3)

        self.sistema.registrar(alumno)
        self.sistema.registrar(materia)
        self.sistema.asignar("220000004", "I5887")

        almacen.guardar(self.sistema, self.archivo_test)

        nuevo_sistema = Sistema()
        almacen.cargar(nuevo_sistema, self.archivo_test)

        self.assertIn("220000004", nuevo_sistema.registros)
        self.assertIn("I5887", nuevo_sistema.materias)
        self.assertEqual(len(nuevo_sistema.materias["I5887"].inscritos), 1)

    def test_05_arranque_limpio_sin_archivo(self) -> None:
        """Verifica que el sistema arranca vacío sin fallar si el archivo no existe."""
        almacen.cargar(self.sistema, "archivo_inexistente_999.json")
        self.assertEqual(len(self.sistema.registros), 0)
        self.assertEqual(len(self.sistema.materias), 0)