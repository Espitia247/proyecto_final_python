import csv
from typing import List, Dict, Optional, Any

# Constante para el nombre del archivo
FILE_PATH = "data/estudiantes.csv"


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
            fieldnames = ["id_estudiante", "nombre", "carrera"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            if estudiantes:
                writer.writerows(estudiantes)
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


def crear_estudiante(estudiantes: List[Dict[str, Any]], nombre: str, carrera: str) -> Dict[str, Any]:
    """
    Crea un nuevo diccionario de estudiante.
    Genera un ID único (ej. E001, E002).

    Args:
        estudiantes (List[Dict[str, Any]]): La lista actual (para generar ID).
        nombre (str): Nombre del estudiante.
        carrera (str): Carrera del estudiante.

    Returns:
        Dict[str, Any]: El nuevo estudiante.
    """
    # Generar un nuevo ID.
    # Si hay estudiantes, toma el ID del último, quita la 'E' y suma 1.
    if not estudiantes:
        nuevo_id_num = 1
    else:
        try:
            ultimo_id = estudiantes[-1]["id_estudiante"]
            nuevo_id_num = int(ultimo_id.replace("E", "")) + 1
        except Exception:
            # Fallback por si los IDs están corruptos
            nuevo_id_num = len(estudiantes) + 1

    nuevo_id_formateado = f"E{str(nuevo_id_num).zfill(3)}"

    nuevo_est = {
        "id_estudiante": nuevo_id_formateado,
        "nombre": nombre,
        "carrera": carrera
    }
    return nuevo_est


def actualizar_estudiante(estudiante: Dict[str, Any], nombre: str, carrera: str) -> None:
    """
    Actualiza los datos de un diccionario de estudiante (pasado por referencia).

    Args:
        estudiante (Dict[str, Any]): El diccionario del estudiante a modificar.
        nombre (str): El nuevo nombre.
        carrera (str): La nueva carrera.
    """
    # Los diccionarios se pasan por referencia, así que se actualiza el original.
    if nombre:
        estudiante["nombre"] = nombre
    if carrera:
        estudiante["carrera"] = carrera


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