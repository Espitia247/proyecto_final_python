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
        # Si el archivo no existe, retornamos una lista vacía
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
            if not estudiantes:
                # Si no hay estudiantes, solo escribimos las cabeceras
                fieldnames = ["id_estudiante", "nombre", "carrera"]
            else:
                fieldnames = estudiantes[0].keys()

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
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
    # TODO (Santiago): Implementar lógica de búsqueda
    # Iterar sobre la lista 'estudiantes'
    # Si encuentras un diccionario donde 'id_estudiante' coincida,
    # retorna ese diccionario.
    # Si terminas el bucle sin encontrarlo, retorna None.
    pass


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
    # TODO (Santiago): Implementar lógica de creación
    # 1. Generar un nuevo ID. Pista: puede ser len(estudiantes) + 1
    #    Formatea el ID como "E" + str(nuevo_id).zfill(3) -> E001
    # 2. Crear el diccionario:
    #    nuevo_est = {
    #        "id_estudiante": nuevo_id_formateado,
    #        "nombre": nombre,
    #        "carrera": carrera
    #    }
    # 3. Retornar nuevo_est
    pass


def actualizar_estudiante(estudiante: Dict[str, Any], nombre: str, carrera: str) -> None:
    """
    Actualiza los datos de un diccionario de estudiante (pasado por referencia).

    Args:
        estudiante (Dict[str, Any]): El diccionario del estudiante a modificar.
        nombre (str): El nuevo nombre.
        carrera (str): La nueva carrera.
    """
    # TODO (Santiago): Implementar lógica de actualización
    # Pista: Los diccionarios se pasan por referencia en Python,
    # así que solo necesitas modificar el que te llega como argumento.
    # estudiante["nombre"] = nombre
    # estudiante["carrera"] = carrera
    pass


def eliminar_estudiante(estudiantes: List[Dict[str, Any]], id_estudiante: str) -> bool:
    """
    Elimina un estudiante de la lista basado en su ID.

    Args:
        estudiantes (List[Dict[str, Any]]): La lista de estudiantes.
        id_estudiante (str): El ID del estudiante a eliminar.

    Returns:
        bool: True si se eliminó, False si no se encontró.
    """
    # TODO (Santiago): Implementar lógica de eliminación
    # 1. Llama a buscar_estudiante_por_id() para encontrar al estudiante.
    # 2. Si lo encuentras (no es None):
    #    Usa el método .remove() de la lista para quitarlo.
    #    Ej: estudiantes.remove(estudiante_encontrado)
    #    Retorna True
    # 3. Si no lo encuentras (es None):
    #    Retorna False
    pass