import json
from typing import List, Dict, Any

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
    # TODO (Daniel): Implementar lógica de creación de matrícula
    # 1. Generar un nuevo ID de matrícula. Ej: "M" + str(len(matriculas) + 1).zfill(4) -> M0001
    # 2. Crear el diccionario:
    #    nueva_matricula = {
    #        "id_matricula": nuevo_id,
    #        "id_estudiante": id_estudiante,
    #        "id_cursos": lista_ids_cursos,
    #        "periodo_academico": periodo
    #    }
    # 3. Retornar nueva_matricula
    pass


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
    # TODO (Daniel): Implementar lógica
    # 1. Buscar en matriculas_db las matrículas que coincidan con id_estudiante.
    #    (Puede haber varias matrículas de diferentes periodos).
    # 2. Recolectar todos los 'id_cursos' de esas matrículas en una sola lista de IDs.
    # 3. Buscar en cursos_db los cursos completos que coincidan con esos IDs.
    # 4. Retornar la lista de diccionarios de cursos completos.
    pass


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
    # TODO (Daniel): Implementar lógica
    # 1. Iterar sobre matriculas_db.
    # 2. Si 'id_curso' está en la lista 'id_cursos' de una matrícula:
    #    Guardar el 'id_estudiante' de esa matrícula.
    # 3. Buscar en estudiantes_db los estudiantes completos que coincidan con los IDs guardados.
    # 4. Retornar la lista de diccionarios de estudiantes completos.
    pass


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
    # TODO (Daniel): Implementar lógica del Reto Final
    # 1. Encontrar la matrícula MÁS RECIENTE del estudiante.
    #    (Puedes asumir que la última en la lista es la más reciente, o buscar por 'periodo_academico').
    # 2. Obtener la lista 'id_cursos' de esa matrícula.
    # 3. Iterar sobre esa lista de IDs.
    # 4. Por cada ID, buscar el curso en cursos_db.
    # 5. Sumar el valor de 'creditos' (¡Mayerly ya te lo da como 'int'!).
    # 6. Retornar la suma total.
    pass