"""
Configuración de Fixtures de Pytest

Este archivo define los datos 'mock' (simulados) que se utilizarán
en todas las pruebas. Cada fixture proporciona una copia nueva
de los datos para cada test, asegurando que las pruebas no
interfieran entre sí.
"""
import pytest
from typing import List, Dict, Any

@pytest.fixture
def carreras_mock() -> List[Dict[str, Any]]:
    """Fixture que provee una lista de carreras de prueba."""
    # Retorna una copia para que cada test tenga datos limpios
    return [
        {"id_carrera": "CAR001", "nombre_carrera": "Analisis y Desarrollo de Software"},
        {"id_carrera": "CAR002", "nombre_carrera": "Ingenieria de Sistemas"}
    ].copy()

@pytest.fixture
def cursos_mock() -> List[Dict[str, Any]]:
    """Fixture que provee una lista de cursos de prueba."""
    return [
        {"id_curso": "C001", "nombre_curso": "Programacion Basica", "creditos": 3},
        {"id_curso": "C002", "nombre_curso": "Bases de Datos", "creditos": 4},
        {"id_curso": "C003", "nombre_curso": "Algebra Lineal", "creditos": 2}
    ].copy()

@pytest.fixture
def estudiantes_mock() -> List[Dict[str, Any]]:
    """Fixture que provee una lista de estudiantes de prueba."""
    return [
        {"id_estudiante": "E001", "nombre": "Santiago Espitia", "id_carrera": "CAR001"},
        {"id_estudiante": "E002", "nombre": "Mayerly", "id_carrera": "CAR001"}
    ].copy()

@pytest.fixture
def matriculas_mock() -> List[Dict[str, Any]]:
    """Fixture que provee una lista de matrículas de prueba."""
    return [
        {
            "id_matricula": "M0001",
            "id_estudiante": "E001",
            "id_cursos": ["C001", "C002"],
            "periodo_academico": "2025-01"
        },
        {
            "id_matricula": "M0002",
            "id_estudiante": "E002",
            "id_cursos": ["C002", "C003"],
            "periodo_academico": "2025-01"
        }
    ].copy()