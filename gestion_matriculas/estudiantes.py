"""
Módulo de Estudiantes (estudiantes.py)

Define la estructura de datos para 'Estudiante' y contiene
todas las funciones CRUD (Crear, Leer, Actualizar, Eliminar)
para interactuar con la fuente de datos (estudiantes.csv).
Utiliza 'id_carrera' como clave foránea a 'carreras.csv'.
"""
import csv
from typing import List, Dict, Optional, Any

# Constante para el nombre del archivo
FILE_PATH = "data/estudiantes.csv"
FILE_HEADERS = ["id_estudiante", "nombre", "id_carrera"]


def cargar_estudiantes() -> List[Dict[str, Any]]:
    """
    Carga los estudiantes desde el archivo CSV.
    Maneja FileNotFoundError si el archivo no existe.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios de estudiantes.
    """
    try:
        with open(FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error inesperado al cargar estudiantes: {e}")
        return []


def guardar_estudiantes(estudiantes: List[Dict[str, Any]]) -> None:
    """
    Guarda la lista completa de estudiantes en el archivo CSV.
    Sobrescribe el archivo si existe.

    Args:
        estudiantes (List[Dict[str, Any]]): La lista de estudiantes a guardar.
    """
    try:
        with open(FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FILE_HEADERS)
            writer.writeheader()
            if estudiantes:
                estudiantes_a_guardar = []
                for est in estudiantes:
                    est_filtrado = {
                        "id_estudiante": est.get("id_estudiante"),
                        "nombre": est.get("nombre"),
                        "id_carrera": est.get("id_carrera")
                    }
                    estudiantes_a_guardar.append(est_filtrado)
                writer.writerows(estudiantes_a_guardar)
    except IOError as e:
        print(f"Error al guardar estudiantes en el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al guardar estudiantes: {e}")


def buscar_estudiante_por_id(estudiantes: List[Dict[str, Any]], id_estudiante: str) -> Optional[Dict[str, Any]]:
    """
    Busca un estudiante por su ID.

    Args:
        estudiantes (List[Dict[str, Any]]): La lista de estudiantes.
        id_estudiante (str): El ID del estudiante a buscar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario del estudiante o None si no se encuentra.
    """
    for estudiante in estudiantes:
        if estudiante["id_estudiante"] == id_estudiante:
            return estudiante
    return None


def _generar_nuevo_id_estudiante(estudiantes: List[Dict[str, Any]]) -> str:
    """
    Genera un ID de estudiante único y robusto (ej. E001, E002).
    Se basa en el ID máximo existente para evitar colisiones.
    """
    if not estudiantes:
        return "E001"

    try:
        ids_numericos = [int(est["id_estudiante"].replace("E", "")) for est in estudiantes if est["id_estudiante"].startswith("E")]
        if not ids_numericos:
            return f"E{str(len(estudiantes) + 1).zfill(3)}"

        max_id = max(ids_numericos)
        nuevo_id_num = max_id + 1
        return f"E{str(nuevo_id_num).zfill(3)}"
    except (ValueError, TypeError) as e:
        print(f"Advertencia: Error al generar ID, posible ID malformado: {e}")
        nuevo_id_num = len(estudiantes) + 1
        return f"E{str(nuevo_id_num).zfill(3)}"


def crear_estudiante(estudiantes: List[Dict[str, Any]], nombre: str, id_carrera: str) -> Dict[str, Any]:
    """
    Crea un nuevo diccionario de estudiante.
    Utiliza una función interna para generar un ID robusto.

    Args:
        estudiantes (List[Dict[str, Any]]): La lista actual (para generar ID).
        nombre (str): Nombre del estudiante.
        id_carrera (str): ID de la carrera del estudiante.

    Returns:
        Dict[str, Any]: El nuevo estudiante.
    """
    nuevo_id = _generar_nuevo_id_estudiante(estudiantes)

    nuevo_est = {
        "id_estudiante": nuevo_id,
        "nombre": nombre,
        "id_carrera": id_carrera
    }
    return nuevo_est


def actualizar_estudiante(estudiante: Dict[str, Any], nombre: Optional[str], id_carrera: Optional[str]) -> None:
    """
    Actualiza los datos de un diccionario de estudiante (pasado por referencia).
    Solo actualiza los campos que no son None o vacíos.

    Args:
        estudiante (Dict[str, Any]): El diccionario del estudiante a modificar.
        nombre (Optional[str]): El nuevo nombre.
        id_carrera (Optional[str]): El nuevo ID de carrera.
    """
    if nombre:
        estudiante["nombre"] = nombre
    if id_carrera:
        estudiante["id_carrera"] = id_carrera


def eliminar_estudiante(estudiantes: List[Dict[str, Any]], id_estudiante: str) -> bool:
    """
    Elimina un estudiante de la lista basado en su ID.

    Args:
        estudiantes (List[Dict[str, Any]]): La lista de estudiantes.
        id_estudiante (str): El ID del estudiante a eliminar.

    Returns:
        bool: True si se eliminó, False si no se encontró.
    """
    estudiante_a_eliminar = buscar_estudiante_por_id(estudiantes, id_estudiante)

    if estudiante_a_eliminar:
        estudiantes.remove(estudiante_a_eliminar)
        return True

    return False