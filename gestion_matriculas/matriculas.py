"""
Módulo de Matrículas (matriculas.py)

Define la estructura de datos para 'Matricula' y contiene
todas las funciones CRUD (Crear, Leer) para interactuar
con la fuente de datos (matriculas.json).

También contiene la lógica de negocio para las relaciones:
- Buscar cursos por estudiante.
- Buscar estudiantes por curso.
- Calcular créditos de un estudiante.
"""
import json
from typing import List, Dict, Any, Optional

# Constante para el nombre del archivo
FILE_PATH = "data/matriculas.json"


def cargar_matriculas() -> List[Dict[str, Any]]:
    """
    Carga las matrículas desde el archivo JSON.
    Maneja FileNotFoundError y JSONDecodeError.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios de matrículas.
    """
    try:
        with open(FILE_PATH, mode='r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error: El archivo de matrículas está corrupto. Se usará una lista vacía.")
        return []
    except Exception as e:
        print(f"Error inesperado al cargar matrículas: {e}")
        return []


def guardar_matriculas(matriculas: List[Dict[str, Any]]) -> None:
    """
    Guarda la lista completa de matrículas en el archivo JSON.

    Args:
        matriculas (List[Dict[str, Any]]): La lista de matrículas a guardar.
    """
    try:
        with open(FILE_PATH, mode='w', encoding='utf-8') as file:
            json.dump(matriculas, file, indent=4)
    except IOError as e:
        print(f"Error al guardar matrículas en el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al guardar matrículas: {e}")


def _generar_nuevo_id_matricula(matriculas: List[Dict[str, Any]]) -> str:
    """
    Genera un ID de matrícula único y robusto (ej. M0001, M0002).
    Se basa en el ID máximo existente para evitar colisiones.
    """
    if not matriculas:
        return "M0001"

    try:
        ids_numericos = [int(mat["id_matricula"].replace("M", "")) for mat in matriculas if
                         mat["id_matricula"].startswith("M")]
        if not ids_numericos:
            return f"M{str(len(matriculas) + 1).zfill(4)}"

        max_id = max(ids_numericos)
        nuevo_id_num = max_id + 1
        return f"M{str(nuevo_id_num).zfill(4)}"
    except (ValueError, TypeError) as e:
        print(f"Advertencia: Error al generar ID, posible ID malformado: {e}")
        nuevo_id_num = len(matriculas) + 1
        return f"M{str(nuevo_id_num).zfill(4)}"


def matricular_estudiante(
        matriculas: List[Dict[str, Any]],
        id_estudiante: str,
        lista_ids_cursos: List[str],
        periodo: str
) -> Dict[str, Any]:
    """
    Crea un nuevo registro de matrícula.
    Genera un ID de matrícula único y robusto.

    Args:
        matriculas (List[Dict[str, Any]]): La lista actual de matrículas.
        id_estudiante (str): El ID del estudiante a matricular.
        lista_ids_cursos (List[str]): Lista de IDs de cursos a matricular.
        periodo (str): Periodo académico (ej. "2025-01").

    Returns:
        Dict[str, Any]: El nuevo objeto de matrícula.
    """
    nuevo_id = _generar_nuevo_id_matricula(matriculas)

    nueva_matricula = {
        "id_matricula": nuevo_id,
        "id_estudiante": id_estudiante,
        "id_cursos": lista_ids_cursos,
        "periodo_academico": periodo
    }
    return nueva_matricula


def obtener_cursos_por_estudiante(
        id_estudiante: str,
        matriculas_db: List[Dict[str, Any]],
        cursos_db: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Encuentra todos los cursos en los que está matriculado un estudiante.
    (Funcionalidad: Ver la lista de cursos en los que está matriculado un estudiante)

    Args:
        id_estudiante (str): El ID del estudiante.
        matriculas_db (List[Dict[str, Any]]): La BD de matrículas.
        cursos_db (List[Dict[str, Any]]): La BD de cursos.

    Returns:
        List[Dict[str, Any]]: Una lista de diccionarios de los cursos encontrados.
    """
    ids_cursos_estudiante = set()

    for matricula in matriculas_db:
        if matricula["id_estudiante"] == id_estudiante:
            ids_cursos_estudiante.update(matricula["id_cursos"])

    cursos_encontrados = []
    for id_curso in ids_cursos_estudiante:
        curso_obj = next((curso for curso in cursos_db if curso["id_curso"] == id_curso), None)
        if curso_obj:
            cursos_encontrados.append(curso_obj)

    return cursos_encontrados


def obtener_estudiantes_por_curso(
        id_curso: str,
        matriculas_db: List[Dict[str, Any]],
        estudiantes_db: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Encuentra todos los estudiantes inscritos en un curso específico.
    (Funcionalidad: Ver la lista de estudiantes inscritos en un curso específico)

    Args:
        id_curso (str): El ID del curso.
        matriculas_db (List[Dict[str, Any]]): La BD de matrículas.
        estudiantes_db (List[Dict[str, Any]]): La BD de estudiantes.

    Returns:
        List[Dict[str, Any]]: Una lista de diccionarios de los estudiantes encontrados.
    """
    ids_estudiantes_curso = set()

    for matricula in matriculas_db:
        if id_curso in matricula["id_cursos"]:
            ids_estudiantes_curso.add(matricula["id_estudiante"])

    estudiantes_encontrados = []
    for id_est in ids_estudiantes_curso:
        est_obj = next((est for est in estudiantes_db if est["id_estudiante"] == id_est), None)
        if est_obj:
            estudiantes_encontrados.append(est_obj)

    return estudiantes_encontrados


def calcular_total_creditos(
        id_estudiante: str,
        matriculas_db: List[Dict[str, Any]],
        cursos_db: List[Dict[str, Any]]
) -> int:
    """
    Calcula el total de créditos matriculados por un estudiante en su matrícula más reciente.
    (Funcionalidad: Reto Final)

    Args:
        id_estudiante (str): El ID del estudiante.
        matriculas_db (List[Dict[str, Any]]): La BD de matrículas.
        cursos_db (List[Dict[str, Any]]): La BD de cursos.

    Returns:
        int: El total de créditos.
    """
    matricula_reciente = None

    for matricula in reversed(matriculas_db):
        if matricula["id_estudiante"] == id_estudiante:
            matricula_reciente = matricula
            break

    if not matricula_reciente:
        return 0

    ids_cursos_matriculados = matricula_reciente["id_cursos"]
    total_creditos = 0

    for id_cur in ids_cursos_matriculados:
        curso_obj = next((curso for curso in cursos_db if curso["id_curso"] == id_cur), None)

        if curso_obj:
            total_creditos += curso_obj.get("creditos", 0)

    return total_creditos