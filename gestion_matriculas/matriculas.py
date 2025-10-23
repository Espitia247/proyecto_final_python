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


def matricular_estudiante(
        matriculas: List[Dict[str, Any]],
        id_estudiante: str,
        lista_ids_cursos: List[str],
        periodo: str
) -> Dict[str, Any]:
    """
    Crea un nuevo registro de matrícula.
    Genera un ID de matrícula único.

    Args:
        matriculas (List[Dict[str, Any]]): La lista actual de matrículas.
        id_estudiante (str): El ID del estudiante a matricular.
        lista_ids_cursos (List[str]): Lista de IDs de cursos a matricular.
        periodo (str): Periodo académico (ej. "2025-01").

    Returns:
        Dict[str, Any]: El nuevo objeto de matrícula.
    """
    if not matriculas:
        nuevo_id_num = 1
    else:
        try:
            ultimo_id = matriculas[-1]["id_matricula"]
            nuevo_id_num = int(ultimo_id.replace("M", "")) + 1
        except Exception:
            nuevo_id_num = len(matriculas) + 1

    nuevo_id = f"M{str(nuevo_id_num).zfill(4)}"

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
    ids_cursos_estudiante = set()  # Usamos un set para evitar duplicados

    # 1. Buscar en matriculas_db las matrículas que coincidan con id_estudiante.
    for matricula in matriculas_db:
        if matricula["id_estudiante"] == id_estudiante:
            # 2. Recolectar todos los 'id_cursos'
            ids_cursos_estudiante.update(matricula["id_cursos"])

    cursos_encontrados = []
    # 3. Buscar en cursos_db los cursos completos que coincidan con esos IDs.
    for id_curso in ids_cursos_estudiante:
        for curso in cursos_db:
            if curso["id_curso"] == id_curso:
                cursos_encontrados.append(curso)
                break  # Pasamos al siguiente id_curso

    # 4. Retornar la lista de diccionarios de cursos completos.
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

    # 1. Iterar sobre matriculas_db.
    for matricula in matriculas_db:
        # 2. Si 'id_curso' está en la lista 'id_cursos' de una matrícula:
        if id_curso in matricula["id_cursos"]:
            # Guardar el 'id_estudiante' de esa matrícula.
            ids_estudiantes_curso.add(matricula["id_estudiante"])

    estudiantes_encontrados = []
    # 3. Buscar en estudiantes_db los estudiantes completos
    for id_est in ids_estudiantes_curso:
        for estudiante in estudiantes_db:
            if estudiante["id_estudiante"] == id_est:
                estudiantes_encontrados.append(estudiante)
                break

    # 4. Retornar la lista de diccionarios de estudiantes completos.
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

    # 1. Encontrar la matrícula MÁS RECIENTE del estudiante.
    #    (Asumimos que la última en la lista es la más reciente para ese estudiante)
    for matricula in reversed(matriculas_db):
        if matricula["id_estudiante"] == id_estudiante:
            matricula_reciente = matricula
            break

    if not matricula_reciente:
        return 0  # El estudiante no tiene matrículas

    # 2. Obtener la lista 'id_cursos' de esa matrícula.
    ids_cursos_matriculados = matricula_reciente["id_cursos"]
    total_creditos = 0

    # 3. Iterar sobre esa lista de IDs.
    for id_cur in ids_cursos_matriculados:
        # 4. Por cada ID, buscar el curso en cursos_db.
        for curso in cursos_db:
            if curso["id_curso"] == id_cur:
                # 5. Sumar el valor de 'creditos'
                total_creditos += curso.get("creditos", 0)  # .get() por seguridad
                break

    # 6. Retornar la suma total.
    return total_creditos