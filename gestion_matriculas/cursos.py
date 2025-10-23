import csv
from typing import List, Dict, Optional, Any

# Constante para el nombre del archivo
FILE_PATH = "data/cursos.csv"


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
                    # Convertir créditos a entero
                    row['creditos'] = int(row['creditos'])
                except (ValueError, TypeError):
                    print(f"Advertencia: 'creditos' no válido para {row['id_curso']}. Se usará 0.")
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
            fieldnames = ["id_curso", "nombre_curso", "creditos"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            if cursos:
                writer.writerows(cursos)
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


def crear_curso(cursos: List[Dict[str, Any]], nombre_curso: str, creditos: int) -> Dict[str, Any]:
    """
    Crea un nuevo diccionario de curso.
    Genera un ID único (ej. C001, C002).

    Args:
        cursos (List[Dict[str, Any]]): La lista actual (para generar ID).
        nombre_curso (str): Nombre del curso.
        creditos (int): Número de créditos.

    Returns:
        Dict[str, Any]: El nuevo curso.
    """
    if not cursos:
        nuevo_id_num = 1
    else:
        try:
            ultimo_id = cursos[-1]["id_curso"]
            nuevo_id_num = int(ultimo_id.replace("C", "")) + 1
        except Exception:
            nuevo_id_num = len(cursos) + 1

    nuevo_id_formateado = f"C{str(nuevo_id_num).zfill(3)}"

    nuevo_curso = {
        "id_curso": nuevo_id_formateado,
        "nombre_curso": nombre_curso,
        "creditos": creditos
    }
    return nuevo_curso


def actualizar_curso(curso: Dict[str, Any], nombre_curso: str, creditos: int) -> None:
    """
    Actualiza los datos de un diccionario de curso (pasado por referencia).

    Args:
        curso (Dict[str, Any]): El diccionario del curso a modificar.
        nombre_curso (str): El nuevo nombre (o "" para no cambiar).
        creditos (int): El nuevo número de créditos (o -1 para no cambiar).
    """
    if nombre_curso:
        curso["nombre_curso"] = nombre_curso
    if creditos >= 0:  # Usamos -1 como señal para no actualizar
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