"""
Módulo de Carreras (carreras.py)

Define la estructura de datos para 'Carrera' y contiene
todas las funciones CRUD (Crear, Leer, Actualizar, Eliminar)
para interactuar con la fuente de datos (carreras.csv).
"""
import csv
from typing import List, Dict, Optional, Any

# Constante para el nombre del archivo
FILE_PATH = "data/carreras.csv"
FILE_HEADERS = ["id_carrera", "nombre_carrera"]


def cargar_carreras() -> List[Dict[str, Any]]:
    """
    Carga las carreras desde el archivo CSV.
    Maneja FileNotFoundError si el archivo no existe.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios de carreras.
    """
    try:
        with open(FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error inesperado al cargar carreras: {e}")
        return []


def guardar_carreras(carreras: List[Dict[str, Any]]) -> None:
    """
    Guarda la lista completa de carreras en el archivo CSV.
    Sobrescribe el archivo si existe.

    Args:
        carreras (List[Dict[str, Any]]): La lista de carreras a guardar.
    """
    try:
        with open(FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FILE_HEADERS)
            writer.writeheader()
            if carreras:
                writer.writerows(carreras)
    except IOError as e:
        print(f"Error al guardar carreras en el archivo: {e}")
    except Exception as e:
        print(f"Error inesperado al guardar carreras: {e}")


def buscar_carrera_por_id(carreras: List[Dict[str, Any]], id_carrera: str) -> Optional[Dict[str, Any]]:
    """
    Busca una carrera por su ID.

    Args:
        carreras (List[Dict[str, Any]]): La lista de carreras.
        id_carrera (str): El ID de la carrera a buscar.

    Returns:
        Optional[Dict[str, Any]]: El diccionario de la carrera o None si no se encuentra.
    """
    for carrera in carreras:
        if carrera["id_carrera"] == id_carrera:
            return carrera
    return None


def _generar_nuevo_id_carrera(carreras: List[Dict[str, Any]]) -> str:
    """
    Genera un ID de carrera único y robusto (ej. CAR001, CAR002).
    Se basa en el ID máximo existente para evitar colisiones.
    """
    if not carreras:
        return "CAR001"

    try:
        ids_numericos = [int(c["id_carrera"].replace("CAR", "")) for c in carreras if c["id_carrera"].startswith("CAR")]
        if not ids_numericos:
            return f"CAR{str(len(carreras) + 1).zfill(3)}"

        max_id = max(ids_numericos)
        nuevo_id_num = max_id + 1
        return f"CAR{str(nuevo_id_num).zfill(3)}"
    except (ValueError, TypeError) as e:
        print(f"Advertencia: Error al generar ID de carrera: {e}")
        nuevo_id_num = len(carreras) + 1
        return f"CAR{str(nuevo_id_num).zfill(3)}"


def crear_carrera(carreras: List[Dict[str, Any]], nombre_carrera: str) -> Dict[str, Any]:
    """
    Crea un nuevo diccionario de carrera.

    Args:
        carreras (List[Dict[str, Any]]): La lista actual (para generar ID).
        nombre_carrera (str): Nombre de la carrera.

    Returns:
        Dict[str, Any]: La nueva carrera.
    """
    nuevo_id = _generar_nuevo_id_carrera(carreras)
    nueva_carrera = {
        "id_carrera": nuevo_id,
        "nombre_carrera": nombre_carrera
    }
    return nueva_carrera


def actualizar_carrera(carrera: Dict[str, Any], nombre_carrera: Optional[str]) -> None:
    """
    Actualiza el nombre de una carrera.

    Args:
        carrera (Dict[str, Any]): El diccionario de la carrera a modificar.
        nombre_carrera (Optional[str]): El nuevo nombre (o None para no cambiar).
    """
    if nombre_carrera:
        carrera["nombre_carrera"] = nombre_carrera


def eliminar_carrera(carreras: List[Dict[str, Any]], id_carrera: str) -> bool:
    """
    Elimina una carrera de la lista basado en su ID.

    Args:
        carreras (List[Dict[str, Any]]): La lista de carreras.
        id_carrera (str): El ID de la carrera a eliminar.

    Returns:
        bool: True si se eliminó, False si no se encontró.
    """
    carrera_a_eliminar = buscar_carrera_por_id(carreras, id_carrera)

    if carrera_a_eliminar:
        carreras.remove(carrera_a_eliminar)
        return True

    return False