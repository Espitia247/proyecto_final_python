"""
Pruebas para la Lógica de Datos (estudiantes.py, cursos.py, etc.)

Estas pruebas validan la lógica de bajo nivel, como la generación
de IDs, las funciones de búsqueda y los cálculos de relaciones.
"""
import pytest
# Importamos los módulos que vamos a probar
from gestion_matriculas import estudiantes, cursos, carreras, matriculas


# --- Pruebas de Generación de ID ---

def test_generar_id_estudiante_vacio():
    """Prueba que el primer ID de estudiante sea 'E001'."""
    assert estudiantes._generar_nuevo_id_estudiante([]) == "E001"


def test_generar_id_estudiante_con_datos(estudiantes_mock):
    """Prueba que el siguiente ID se base en el máximo existente."""
    # El ID máximo en el mock es E002, espera E003
    assert estudiantes._generar_nuevo_id_estudiante(estudiantes_mock) == "E003"


def test_generar_id_curso_vacio():
    """Prueba que el primer ID de curso sea 'C001'."""
    assert cursos._generar_nuevo_id_curso([]) == "C001"


def test_generar_id_curso_con_datos(cursos_mock):
    """Prueba que el siguiente ID se base en el máximo existente."""
    # El ID máximo en el mock es C003, espera C004
    assert cursos._generar_nuevo_id_curso(cursos_mock) == "C004"


def test_generar_id_carrera_vacio():
    """Prueba que el primer ID de carrera sea 'CAR001'."""
    assert carreras._generar_nuevo_id_carrera([]) == "CAR001"


def test_generar_id_carrera_con_datos(carreras_mock):
    """Prueba que el siguiente ID se base en el máximo existente."""
    # El ID máximo en el mock es CAR002, espera CAR003
    assert carreras._generar_nuevo_id_carrera(carreras_mock) == "CAR003"


def test_generar_id_matricula_vacio():
    """Prueba que el primer ID de matrícula sea 'M0001'."""
    assert matriculas._generar_nuevo_id_matricula([]) == "M0001"


def test_generar_id_matricula_con_datos(matriculas_mock):
    """Prueba que el siguiente ID se base en el máximo existente."""
    # El ID máximo en el mock es M0002, espera M0003
    assert matriculas._generar_nuevo_id_matricula(matriculas_mock) == "M0003"


# --- Pruebas de Búsqueda y Lógica Relacional (en matriculas.py) ---

def test_obtener_cursos_por_estudiante(matriculas_mock, cursos_mock):
    """Prueba que se devuelvan los cursos correctos para un estudiante."""
    # Probar para E001
    cursos_encontrados = matriculas.obtener_cursos_por_estudiante("E001", matriculas_mock, cursos_mock)

    # Debe encontrar C001 y C002
    assert len(cursos_encontrados) == 2
    ids_encontrados = {curso['id_curso'] for curso in cursos_encontrados}
    assert "C001" in ids_encontrados
    assert "C002" in ids_encontrados


def test_obtener_estudiantes_por_curso(matriculas_mock, estudiantes_mock):
    """Prueba que se devuelvan los estudiantes correctos para un curso."""
    # Probar para C002 (debe estar E001 y E002)
    est_encontrados = matriculas.obtener_estudiantes_por_curso("C002", matriculas_mock, estudiantes_mock)

    assert len(est_encontrados) == 2
    ids_encontrados = {est['id_estudiante'] for est in est_encontrados}
    assert "E001" in ids_encontrados
    assert "E002" in ids_encontrados


def test_calcular_total_creditos(matriculas_mock, cursos_mock):
    """Prueba que la suma de créditos sea correcta."""
    # Probar para E001, que tiene C001 (3cr) y C002 (4cr)
    total_creditos = matriculas.calcular_total_creditos("E001", matriculas_mock, cursos_mock)
    assert total_creditos == 7  # 3 + 4


def test_calcular_total_creditos_otro_estudiante(matriculas_mock, cursos_mock):
    """Prueba la suma para el segundo estudiante."""
    # Probar para E002, que tiene C002 (4cr) y C003 (2cr)
    total_creditos = matriculas.calcular_total_creditos("E002", matriculas_mock, cursos_mock)
    assert total_creditos == 6  # 4 + 2


def test_calcular_total_creditos_estudiante_sin_matricula(matriculas_mock, cursos_mock):
    """Prueba que devuelva 0 si el estudiante no tiene matrícula."""
    total_creditos = matriculas.calcular_total_creditos("E999", matriculas_mock, cursos_mock)
    assert total_creditos == 0