"""
Módulo de Servicios (servicios.py)

Contiene la lógica de negocio principal de la aplicación.
Este módulo actúa como intermediario entre la Interfaz de Usuario (ui.py)
y los módulos de acceso a datos (estudiantes.py, cursos.py, matriculas.py).

Funciones en este módulo:
- Realizan validaciones (ej. campos no vacíos, IDs existentes).
- Orquestan las operaciones (ej. crear, actualizar, matricular).
- NO importan 'ui' ni interactúan directamente con la consola.
- Devuelven diccionarios de respuesta para que 'main.py' se los pase a 'ui.py'.
"""
from typing import List, Dict, Any, Optional
# Importar los módulos de datos
import gestion_matriculas.estudiantes as est
import gestion_matriculas.cursos as cur
import gestion_matriculas.matriculas as mat
import gestion_matriculas.carreras as car


# --- Servicios de Estudiantes ---

def srv_registrar_estudiante(lista_est: List[Dict], lista_car: List[Dict], nombre: str, id_carrera: Optional[str]) -> Dict[str, str]:
    """
    Servicio para validar y crear un nuevo estudiante.
    Valida que el id_carrera exista.
    """
    if not nombre or not id_carrera:
        return {"tipo": "error", "mensaje": "Nombre y Carrera son obligatorios."}

    if not car.buscar_carrera_por_id(lista_car, id_carrera):
        return {"tipo": "error", "mensaje": f"El ID de carrera '{id_carrera}' no es válido."}

    for est_existente in lista_est:
        if est_existente["nombre"].strip().lower() == nombre.strip().lower():
            return {"tipo": "error", "mensaje": f"Ya existe un estudiante con el nombre '{nombre}'."}

    nuevo_est = est.crear_estudiante(lista_est, nombre, id_carrera)
    lista_est.append(nuevo_est)
    return {"tipo": "exito", "mensaje": f"Estudiante '{nombre}' creado con ID {nuevo_est['id_estudiante']}"}


def srv_actualizar_estudiante(lista_est: List[Dict], lista_car: List[Dict], id_est: str, n_nombre: Optional[str], n_id_carrera: Optional[str]) -> Dict[str, str]:
    """
    Servicio para validar y actualizar un estudiante.
    """
    if not n_nombre and not n_id_carrera:
        return {"tipo": "info", "mensaje": "No se ingresaron datos para actualizar."}

    estudiante_obj = est.buscar_estudiante_por_id(lista_est, id_est)
    if not estudiante_obj:
        return {"tipo": "error", "mensaje": f"Estudiante con ID {id_est} no encontrado."}

    if n_id_carrera and not car.buscar_carrera_por_id(lista_car, n_id_carrera):
        return {"tipo": "error", "mensaje": f"El ID de carrera '{n_id_carrera}' no es válido. No se actualizó la carrera."}

    est.actualizar_estudiante(estudiante_obj, n_nombre, n_id_carrera)
    return {"tipo": "exito", "mensaje": f"Estudiante {id_est} actualizado con éxito."}


def srv_eliminar_estudiante(lista_est: List[Dict], lista_mat: List[Dict], id_est: str) -> Dict[str, str]:
    """
    Servicio para validar y eliminar un estudiante.
    VALIDACIÓN: No permite eliminar si tiene matrículas.
    """
    for matricula in lista_mat:
        if matricula.get("id_estudiante") == id_est:
            return {"tipo": "error", "mensaje": f"No se puede eliminar. Estudiante {id_est} tiene matrículas registradas."}

    exito = est.eliminar_estudiante(lista_est, id_est)
    if exito:
        return {"tipo": "exito", "mensaje": f"Estudiante con ID {id_est} eliminado."}
    else:
        return {"tipo": "error", "mensaje": f"Estudiante con ID {id_est} no encontrado."}

# --- Servicios de Cursos ---

def srv_registrar_curso(lista_cur: List[Dict], nombre: str, creditos: Optional[int]) -> Dict[str, str]:
    """
    Servicio para validar y crear un nuevo curso.
    """
    if not nombre or creditos is None:
        return {"tipo": "error", "mensaje": "Nombre y créditos son obligatorios."}
    if creditos < 0:
        return {"tipo": "error", "mensaje": "Los créditos no pueden ser negativos."}

    nuevo_cur = cur.crear_curso(lista_cur, nombre, creditos)
    lista_cur.append(nuevo_cur)
    return {"tipo": "exito", "mensaje": f"Curso '{nombre}' creado con ID {nuevo_cur['id_curso']}"}


def srv_actualizar_curso(lista_cur: List[Dict], id_cur: str, n_nombre: Optional[str], n_creditos: Optional[int]) -> Dict[str, str]:
    """
    Servicio para validar y actualizar un curso.
    """
    if not n_nombre and n_creditos is None:
        return {"tipo": "info", "mensaje": "No se ingresaron datos para actualizar."}

    curso_obj = cur.buscar_curso_por_id(lista_cur, id_cur)
    if not curso_obj:
        return {"tipo": "error", "mensaje": f"Curso con ID {id_cur} no encontrado."}

    cur.actualizar_curso(curso_obj, n_nombre, n_creditos)
    return {"tipo": "exito", "mensaje": f"Curso {id_cur} actualizado con éxito."}


def srv_eliminar_curso(lista_cur: List[Dict], lista_mat: List[Dict], id_cur: str) -> Dict[str, str]:
    """
    Servicio para validar y eliminar un curso.
    VALIDACIÓN: No permite eliminar si está en una matrícula.
    """
    for matricula in lista_mat:
        if id_cur in matricula.get("id_cursos", []):
            return {"tipo": "error", "mensaje": f"No se puede eliminar. Curso {id_cur} está en matrículas registradas."}

    exito = cur.eliminar_curso(lista_cur, id_cur)
    if exito:
        return {"tipo": "exito", "mensaje": f"Curso con ID {id_cur} eliminado."}
    else:
        return {"tipo": "error", "mensaje": f"Curso con ID {id_cur} no encontrado."}

# --- Servicios de Carreras ---

def srv_registrar_carrera(lista_car: List[Dict], nombre: str) -> Dict[str, str]:
    """
    Servicio para validar y crear una nueva carrera.
    """
    if not nombre:
        return {"tipo": "error", "mensaje": "El nombre de la carrera no puede estar vacío."}

    for car_existente in lista_car:
        if car_existente["nombre_carrera"].strip().lower() == nombre.strip().lower():
            return {"tipo": "error", "mensaje": f"Ya existe una carrera con el nombre '{nombre}'."}

    nueva_car = car.crear_carrera(lista_car, nombre)
    lista_car.append(nueva_car)
    return {"tipo": "exito", "mensaje": f"Carrera '{nombre}' creada con ID {nueva_car['id_carrera']}"}


def srv_actualizar_carrera(lista_car: List[Dict], id_car: str, n_nombre: Optional[str]) -> Dict[str, str]:
    """
    Servicio para validar y actualizar una carrera.
    """
    if not n_nombre:
        return {"tipo": "info", "mensaje": "No se ingresó un nombre para actualizar."}

    carrera_obj = car.buscar_carrera_por_id(lista_car, id_car)
    if not carrera_obj:
        return {"tipo": "error", "mensaje": f"Carrera con ID {id_car} no encontrada."}

    car.actualizar_carrera(carrera_obj, n_nombre)
    return {"tipo": "exito", "mensaje": f"Carrera {id_car} actualizada con éxito."}


def srv_eliminar_carrera(lista_car: List[Dict], lista_est: List[Dict], id_car: str) -> Dict[str, str]:
    """
    Servicio para validar y eliminar una carrera.
    VALIDACIÓN: No permite eliminar si tiene estudiantes.
    """
    for estudiante in lista_est:
        if estudiante.get("id_carrera") == id_car:
            return {"tipo": "error", "mensaje": f"No se puede eliminar. Carrera {id_car} tiene estudiantes asignados."}

    exito = car.eliminar_carrera(lista_car, id_car)
    if exito:
        return {"tipo": "exito", "mensaje": f"Carrera con ID {id_car} eliminada."}
    else:
        return {"tipo": "error", "mensaje": f"Carrera con ID {id_car} no encontrada."}


# --- Servicios de Matrículas ---

def srv_matricular_estudiante(
    id_est: str,
    ids_cursos: List[str],
    periodo: str,
    lista_est: List[Dict],
    lista_cur: List[Dict],
    lista_mat: List[Dict]
) -> Dict[str, str]:
    """
    Servicio para validar y crear una nueva matrícula.
    """
    if not id_est or not ids_cursos or not periodo:
        return {"tipo": "error", "mensaje": "Faltan datos (ID Estudiante, Cursos o Periodo)."}

    est_obj = est.buscar_estudiante_por_id(lista_est, id_est)
    if not est_obj:
        return {"tipo": "error", "mensaje": f"ID de estudiante {id_est} no existe."}

    cursos_validos = []
    cursos_invalidos = []
    for id_c in ids_cursos:
        cur_obj = cur.buscar_curso_por_id(lista_cur, id_c)
        if cur_obj:
            cursos_validos.append(id_c)
        else:
            cursos_invalidos.append(id_c)

    if not cursos_validos:
        msg_invalidos = f"IDs inválidos: {', '.join(cursos_invalidos)}" if cursos_invalidos else ""
        return {"tipo": "error", "mensaje": f"No se proporcionaron cursos válidos. {msg_invalidos}"}

    nueva_mat = mat.matricular_estudiante(lista_mat, id_est, cursos_validos, periodo)
    lista_mat.append(nueva_mat)

    msg_exito = f"Estudiante {est_obj['nombre']} matriculado en {len(cursos_validos)} curso(s)."
    if cursos_invalidos:
        msg_exito += f" (IDs ignorados por no existir: {', '.join(cursos_invalidos)})"

    return {"tipo": "exito", "mensaje": msg_exito}