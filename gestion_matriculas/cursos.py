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
                # TODO (Mayerly): Convertir créditos a entero
                # Usa un try-except por si el dato en el CSV está malo
                try:
                    row['creditos'] = int(row['creditos'])
                except ValueError:
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
            if not cursos:
                fieldnames = ["id_curso", "nombre_curso", "creditos"]
            else:
                fieldnames = cursos[0].keys()

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
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
    # TODO (Mayerly): Implementar lógica de búsqueda
    # Idéntico a la función de Santiago, pero para 'id_curso'.
    pass


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
    # TODO (Mayerly): Implementar lógica de creación
    # 1. Generar un nuevo ID. Ej: "C" + str(len(cursos) + 1).zfill(3) -> C001
    # 2. Crear el diccionario:
    #    nuevo_curso = {
    #        "id_curso": nuevo_id_formateado,
    #        "nombre_curso": nombre_curso,
    #        "creditos": creditos
    #    }
    # 3. Retornar nuevo_curso
    pass


def actualizar_curso(curso: Dict[str, Any], nombre_curso: str, creditos: int) -> None:
    """
    Actualiza los datos de un diccionario de curso (pasado por referencia).

    Args:
        curso (Dict[str, Any]): El diccionario del curso a modificar.
        nombre_curso (str): El nuevo nombre.
        creditos (int): El nuevo número de créditos.
    """
    # TODO (Mayerly): Implementar lógica de actualización
    # curso["nombre_curso"] = nombre_curso
    # curso["creditos"] = creditos
    pass


def eliminar_curso(cursos: List[Dict[str, Any]], id_curso: str) -> bool:
    """
    Elimina un curso de la lista basado en su ID.

    Args:
        cursos (List[Dict[str, Any]]): La lista de cursos.
        id_curso (str): El ID del curso a eliminar.

    Returns:
        bool: True si se eliminó, False si no se encontró.
    """
    # TODO (Mayerly): Implementar lógica de eliminación
    # 1. Llama a buscar_curso_por_id() para encontrar el curso.
    # 2. Si lo encuentras (no es None):
    #    cursos.remove(curso_encontrado)
    #    Retorna True
    # 3. Si no lo encuentras (es None):
    #    Retorna False
    pass