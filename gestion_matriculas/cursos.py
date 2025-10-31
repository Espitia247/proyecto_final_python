"""
Módulo de Cursos (cursos.py)

Define la estructura de datos para 'Curso' y contiene
todas las funciones CRUD (Crear, Leer, Actualizar, Eliminar)
para interactuar con la fuente de datos (cursos.csv).
"""
import csv
from typing import List, Dict, Optional, Any

# Constante para el nombre del archivo
FILE_PATH = "data/cursos.csv"
FILE_HEADERS = ["id_curso", "nombre_curso", "creditos"]


def cargar_cursos() -> List[Dict[str, Any]]:
    """
    Carga los cursos desde el archivo CSV.
    Maneja FileNotFoundError si el archivo no existe.
    Convierte 'creditos' a entero.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios de cursos.
    """
    cursos = []
    try:
        with open(FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row['creditos'] = int(row['creditos'])
                except (ValueError, TypeError):
                    print(f"Advertencia: 'creditos' no válido para {row.get('id_curso')}. Se usará 0.")
                    row['creditos'] = 0
                cursos.append(row)
            return cursos
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error inesperado al cargar cursos: {e}")
        return []


def guardar_cursos(cursos: List[Dict[str, Any]]) -> None:
    """
    Guarda la lista completa de cursos en el archivo CSV.
    Sobrescribe el archivo si existe.

    Args:
        cursos (List[Dict[str, Any]]): La lista de cursos a guardar.
    """
    try:
        with open(FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FILE_HEADERS)
            writer.writeheader()
            if cursos:
                cursos_a_guardar = []
                for curso in cursos:
                    curso_filtrado = {
                        "id_curso": curso.get("id_curso"),
                        "nombre_curso": curso.get("nombre_curso"),
                        "creditos": curso.get("creditos", 0)
                    }
                    cursos_a_guardar.append(curso_filtrado)
                writer.writerows(cursos_a_guardar)
    except IOError as e:
        print(f"Error al guardar cursos en el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al guardar cursos: {e}")


def buscar_curso_por_id(cursos: List[Dict[str, Any]], id_curso: str) -> Optional[Dict[str, Any]]:
    """
    Busca un curso por su ID.

    Args:
        cursos (List[Dict[str, Any]]): La lista de cursos.
        id_curso (str): El ID del curso a buscar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del curso o None si no se encuentra.
    """
    for curso in cursos:
        if curso["id_curso"] == id_curso:
            return curso
    return None


def _generar_nuevo_id_curso(cursos: List[Dict[str, Any]]) -> str:
    """
    Genera un ID de curso único y robusto (ej. C001, C002).
    Se basa en el ID máximo existente para evitar colisiones.
    """
    if not cursos:
        return "C001"

    try:
        ids_numericos = [int(curso["id_curso"].replace("C", "")) for curso in cursos if curso["id_curso"].startswith("C")]
        if not ids_numericos:
            return f"C{str(len(cursos) + 1).zfill(3)}"

        max_id = max(ids_numericos)
        nuevo_id_num = max_id + 1
        return f"C{str(nuevo_id_num).zfill(3)}"
    except (ValueError, TypeError) as e:
        print(f"Advertencia: Error al generar ID, posible ID malformado: {e}")
        nuevo_id_num = len(cursos) + 1
        return f"C{str(nuevo_id_num).zfill(3)}"


def crear_curso(cursos: List[Dict[str, Any]], nombre_curso: str, creditos: int) -> Dict[str, Any]:
    """
    Crea un nuevo diccionario de curso.
    Utiliza una función interna para generar un ID robusto.

    Args:
        cursos (List[Dict[str, Any]]): La lista actual (para generar ID).
        nombre_curso (str): Nombre del curso.
        creditos (int): Número de créditos.

    Returns:
        Dict[str, Any]: El nuevo curso.
    """
    nuevo_id = _generar_nuevo_id_curso(cursos)

    nuevo_curso = {
        "id_curso": nuevo_id,
        "nombre_curso": nombre_curso,
        "creditos": creditos
    }
    return nuevo_curso


def actualizar_curso(curso: Dict[str, Any], nombre_curso: Optional[str], creditos: Optional[int]) -> None:
    """
    Actualiza los datos de un diccionario de curso (pasado por referencia).
    Solo actualiza los campos que no son None.

    Args:
        curso (Dict[str, Any]): El diccionario del curso a modificar.
        nombre_curso (Optional[str]): El nuevo nombre (o None para no cambiar).
        creditos (Optional[int]): El nuevo N° de créditos (o None para no cambiar).
    """
    if nombre_curso is not None and nombre_curso != "":
        curso["nombre_curso"] = nombre_curso

    if creditos is not None and creditos >= 0:
        curso["creditos"] = creditos


def eliminar_curso(cursos: List[Dict[str, Any]], id_curso: str) -> bool:
    """
    Elimina un curso de la lista basado en su ID.

    Args:
        cursos (List[Dict[str, Any]]): La lista de cursos.
        id_curso (str): El ID del curso a eliminar.

    Returns:
        bool: True si se eliminó, False si no se encontró.
    """
    curso_a_eliminar = buscar_curso_por_id(cursos, id_curso)

    if curso_a_eliminar:
        cursos.remove(curso_a_eliminar)
        return True

    return False