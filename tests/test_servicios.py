"""
Pruebas para el Módulo de Servicios (servicios.py)

Estas pruebas validan la lógica de negocio principal:
- Casos de éxito (ej. registrar algo).
- Casos de error por validación (ej. datos faltantes).
- Casos de error por lógica (ej. ID no encontrado, duplicados).
- Casos de error de integridad (ej. no eliminar si está en uso).
"""
import pytest
# Importamos el módulo de servicios
from gestion_matriculas import servicios as srv


# --- Pruebas de Servicios de Estudiantes ---

def test_srv_registrar_estudiante_exito(estudiantes_mock, carreras_mock):
    """Prueba que un estudiante se pueda registrar correctamente."""
    lista_est = estudiantes_mock
    lista_car = carreras_mock

    resultado = srv.srv_registrar_estudiante(lista_est, lista_car, "Nuevo Alumno", "CAR001")

    assert resultado["tipo"] == "exito"
    assert len(lista_est) == 3  # 2 del mock + 1 nuevo
    assert lista_est[-1]["nombre"] == "Nuevo Alumno"


def test_srv_registrar_estudiante_duplicado(estudiantes_mock, carreras_mock):
    """Prueba que no se pueda registrar un estudiante con un nombre duplicado."""
    resultado = srv.srv_registrar_estudiante(estudiantes_mock, carreras_mock, "Santiago Espitia", "CAR001")

    assert resultado["tipo"] == "error"
    assert "Ya existe un estudiante" in resultado["mensaje"]
    assert len(estudiantes_mock) == 2  # No debe cambiar


def test_srv_registrar_estudiante_carrera_invalida(estudiantes_mock, carreras_mock):
    """Prueba que no se pueda registrar un estudiante con un ID de carrera inválido."""
    resultado = srv.srv_registrar_estudiante(estudiantes_mock, carreras_mock, "Test", "CAR999")

    assert resultado["tipo"] == "error"
    assert "ID de carrera 'CAR999' no es válido" in resultado["mensaje"]
    assert len(estudiantes_mock) == 2


def test_srv_actualizar_estudiante_exito(estudiantes_mock, carreras_mock):
    """Prueba que se pueda actualizar el nombre y carrera de un estudiante."""
    resultado = srv.srv_actualizar_estudiante(estudiantes_mock, carreras_mock, "E001", "Santiago R.", "CAR002")

    assert resultado["tipo"] == "exito"
    assert estudiantes_mock[0]["nombre"] == "Santiago R."
    assert estudiantes_mock[0]["id_carrera"] == "CAR002"


def test_srv_actualizar_estudiante_no_encontrado(estudiantes_mock, carreras_mock):
    """Prueba que falle si el ID del estudiante no existe."""
    resultado = srv.srv_actualizar_estudiante(estudiantes_mock, carreras_mock, "E999", "Test", "CAR001")
    assert resultado["tipo"] == "error"


def test_srv_eliminar_estudiante_con_matricula(estudiantes_mock, matriculas_mock):
    """Prueba que NO se pueda eliminar un estudiante si tiene matrículas."""
    # E001 tiene una matrícula en el mock
    resultado = srv.srv_eliminar_estudiante(estudiantes_mock, matriculas_mock, "E001")

    assert resultado["tipo"] == "error"
    assert "tiene matrículas registradas" in resultado["mensaje"]
    assert len(estudiantes_mock) == 2  # No se eliminó


def test_srv_eliminar_estudiante_exito(estudiantes_mock, matriculas_mock):
    """Prueba que SÍ se pueda eliminar un estudiante sin matrículas."""
    # Agregamos un estudiante "E003" que no está en matrículas
    estudiantes_mock.append({"id_estudiante": "E003", "nombre": "Test", "id_carrera": "CAR001"})
    assert len(estudiantes_mock) == 3

    resultado = srv.srv_eliminar_estudiante(estudiantes_mock, matriculas_mock, "E003")

    assert resultado["tipo"] == "exito"
    assert len(estudiantes_mock) == 2  # Se eliminó


# --- Pruebas de Servicios de Cursos ---

def test_srv_registrar_curso_exito(cursos_mock):
    """Prueba que un curso se pueda registrar correctamente."""
    resultado = srv.srv_registrar_curso(cursos_mock, "Nuevo Curso", 5)

    assert resultado["tipo"] == "exito"
    assert len(cursos_mock) == 4
    assert cursos_mock[-1]["nombre_curso"] == "Nuevo Curso"


def test_srv_registrar_curso_creditos_negativos(cursos_mock):
    """Prueba que no se acepten créditos negativos."""
    resultado = srv.srv_registrar_curso(cursos_mock, "Test", -1)

    assert resultado["tipo"] == "error"
    assert "créditos no pueden ser negativos" in resultado["mensaje"]
    assert len(cursos_mock) == 3


def test_srv_eliminar_curso_con_matricula(cursos_mock, matriculas_mock):
    """Prueba que NO se pueda eliminar un curso si está en una matrícula."""
    # C001 está en la matrícula de E001
    resultado = srv.srv_eliminar_curso(cursos_mock, matriculas_mock, "C001")

    assert resultado["tipo"] == "error"
    assert "está en matrículas registradas" in resultado["mensaje"]
    assert len(cursos_mock) == 3


# --- Pruebas de Servicios de Carreras ---

def test_srv_registrar_carrera_duplicada(carreras_mock):
    """Prueba que no se pueda registrar una carrera duplicada."""
    resultado = srv.srv_registrar_carrera(carreras_mock, "Ingenieria de Sistemas")
    assert resultado["tipo"] == "error"
    assert "Ya existe una carrera" in resultado["mensaje"]


def test_srv_eliminar_carrera_con_estudiantes(carreras_mock, estudiantes_mock):
    """Prueba que NO se pueda eliminar una carrera si tiene estudiantes."""
    # CAR001 tiene estudiantes en el mock
    resultado = srv.srv_eliminar_carrera(carreras_mock, estudiantes_mock, "CAR001")

    assert resultado["tipo"] == "error"
    assert "tiene estudiantes asignados" in resultado["mensaje"]
    assert len(carreras_mock) == 2


# --- Pruebas de Servicios de Matrículas ---

def test_srv_matricular_estudiante_exito(estudiantes_mock, cursos_mock, matriculas_mock):
    """Prueba una matrícula exitosa."""
    # E001 matriculándose en C003
    resultado = srv.srv_matricular_estudiante("E001", ["C003"], "2025-02", estudiantes_mock, cursos_mock,
                                              matriculas_mock)

    assert resultado["tipo"] == "exito"
    assert len(matriculas_mock) == 3
    assert matriculas_mock[-1]["id_estudiante"] == "E001"
    assert "C003" in matriculas_mock[-1]["id_cursos"]


def test_srv_matricular_estudiante_invalido(estudiantes_mock, cursos_mock, matriculas_mock):
    """Prueba que falle si el estudiante no existe."""
    resultado = srv.srv_matricular_estudiante("E999", ["C003"], "2025-02", estudiantes_mock, cursos_mock,
                                              matriculas_mock)
    assert resultado["tipo"] == "error"
    assert "estudiante E999 no existe" in resultado["mensaje"]


def test_srv_matricular_curso_invalido(estudiantes_mock, cursos_mock, matriculas_mock):
    """Prueba que falle si NINGÚN curso es válido."""
    resultado = srv.srv_matricular_estudiante("E001", ["C999", "C888"], "2025-02", estudiantes_mock, cursos_mock,
                                              matriculas_mock)
    assert resultado["tipo"] == "error"
    assert "No se proporcionaron cursos válidos" in resultado["mensaje"]
    assert len(matriculas_mock) == 2  # No se creó la matrícula


def test_srv_matricular_cursos_mixtos(estudiantes_mock, cursos_mock, matriculas_mock):
    """Prueba que matricule los cursos válidos e ignore los inválidos."""
    # C003 es válido, C999 es inválido
    resultado = srv.srv_matricular_estudiante("E001", ["C003", "C999"], "2025-02", estudiantes_mock, cursos_mock,
                                              matriculas_mock)

    assert resultado["tipo"] == "exito"  # La operación fue un éxito
    assert "(IDs ignorados por no existir: C999)" in resultado["mensaje"]
    assert len(matriculas_mock) == 3  # Se creó la matrícula
    assert "C003" in matriculas_mock[-1]["id_cursos"]
    assert "C999" not in matriculas_mock[-1]["id_cursos"]