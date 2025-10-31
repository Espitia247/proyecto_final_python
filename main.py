"""
Módulo Principal (main.py)

Este es el punto de entrada de la aplicación.
Actúa como el "controlador" principal:
1. Carga los datos al iniciar.
2. Muestra el menú principal (usando 'ui').
3. Llama a los submenús de gestión.
4. Pasa los datos (listas) entre las funciones.
5. Llama a los 'servicios' para ejecutar la lógica.
6. Llama a los módulos de datos para guardar cambios.

NUEVO: Los bucles de gestión ahora comprueban si las funciones de UI
devuelven 'None' (señal de cancelación) y actúan en consecuencia.
"""
# Importar los módulos del proyecto
import gestion_matriculas.estudiantes as est
import gestion_matriculas.cursos as cur
import gestion_matriculas.matriculas as mat
import gestion_matriculas.carreras as car
import gestion_matriculas.ui as ui
import gestion_matriculas.utils as utils
import gestion_matriculas.servicios as srv
from typing import List, Dict, Any


def gestionar_estudiantes(lista_estudiantes: List[Dict[str, Any]], lista_carreras: List[Dict[str, Any]], lista_matriculas: List[Dict[str, Any]]):
    """Bucle del submenú de gestión de estudiantes."""
    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_crud("Estudiante")

        if opcion == "1":  # Crear
            datos_estudiante = ui.pedir_datos_estudiante(lista_carreras, actualizando=False)
            if datos_estudiante is None:
                ui.mostrar_mensaje("Creación de estudiante cancelada.", "info")
                continue

            nombre, id_carrera = datos_estudiante
            resultado = srv.srv_registrar_estudiante(lista_estudiantes, lista_carreras, nombre, id_carrera)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                est.guardar_estudiantes(lista_estudiantes)

        elif opcion == "2":  # Ver todos
            ui.mostrar_tabla_estudiantes(lista_estudiantes, lista_carreras)

        elif opcion == "3":  # Actualizar
            id_est = ui.seleccionar_estudiante(lista_estudiantes, lista_carreras, "actualizar", permitir_cancelar=True)
            if not id_est:
                continue

            estudiante_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)
            if not estudiante_obj:
                ui.mostrar_mensaje(f"Error: Estudiante {id_est} no se encontró (ID inválido).", "error")
                continue

            ui.mostrar_mensaje(f"Actualizando a: {estudiante_obj['nombre']}", "info")
            datos_nuevos = ui.pedir_datos_estudiante(lista_carreras, actualizando=True)
            if datos_nuevos is None:
                ui.mostrar_mensaje("Actualización cancelada.", "info")
                continue

            n_nombre, n_id_carrera = datos_nuevos
            resultado = srv.srv_actualizar_estudiante(lista_estudiantes, lista_carreras, id_est, n_nombre, n_id_carrera)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                est.guardar_estudiantes(lista_estudiantes)

        elif opcion == "4":  # Eliminar
            id_est = ui.seleccionar_estudiante(lista_estudiantes, lista_carreras, "eliminar", permitir_cancelar=True)
            if not id_est:
                continue

            resultado = srv.srv_eliminar_estudiante(lista_estudiantes, lista_matriculas, id_est)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                est.guardar_estudiantes(lista_estudiantes)

        elif opcion == "5":  # Buscar
            id_est = ui.seleccionar_estudiante(lista_estudiantes, lista_carreras, "buscar", permitir_cancelar=True)
            if not id_est:
                continue

            estudiante_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)
            if estudiante_obj:
                ui.mostrar_tabla_estudiantes([estudiante_obj], lista_carreras)
            else:
                ui.mostrar_mensaje(f"Estudiante con ID {id_est} no encontrado.", "error")

        elif opcion == "6":  # Volver
            break

        input("\nPresione Enter para continuar...")


def gestionar_cursos(lista_cursos: List[Dict[str, Any]], lista_matriculas: List[Dict[str, Any]]):
    """Bucle del submenú de gestión de cursos."""
    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_crud("Curso")

        if opcion == "1":  # Crear
            datos_curso = ui.pedir_datos_curso()
            if datos_curso is None:
                ui.mostrar_mensaje("Creación de curso cancelada.", "info")
                continue

            nombre, creditos = datos_curso
            resultado = srv.srv_registrar_curso(lista_cursos, nombre, creditos)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                cur.guardar_cursos(lista_cursos)

        elif opcion == "2":  # Ver todos
            ui.mostrar_tabla_cursos(lista_cursos)

        elif opcion == "3":  # Actualizar
            id_cur = ui.seleccionar_curso(lista_cursos, "actualizar", permitir_cancelar=True)
            if not id_cur:
                continue

            curso_obj = cur.buscar_curso_por_id(lista_cursos, id_cur)
            if not curso_obj:
                ui.mostrar_mensaje(f"Error: Curso {id_cur} no encontrado.", "error")
                continue

            ui.mostrar_mensaje(f"Actualizando a: {curso_obj['nombre_curso']}", "info")
            datos_nuevos = ui.pedir_datos_curso(actualizando=True)
            if datos_nuevos is None:
                ui.mostrar_mensaje("Actualización cancelada.", "info")
                continue

            n_nombre, n_creditos = datos_nuevos
            resultado = srv.srv_actualizar_curso(lista_cursos, id_cur, n_nombre, n_creditos)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                cur.guardar_cursos(lista_cursos)

        elif opcion == "4":  # Eliminar
            id_cur = ui.seleccionar_curso(lista_cursos, "eliminar", permitir_cancelar=True)
            if not id_cur:
                continue

            resultado = srv.srv_eliminar_curso(lista_cursos, lista_matriculas, id_cur)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                cur.guardar_cursos(lista_cursos)

        elif opcion == "5":  # Buscar
            id_cur = ui.seleccionar_curso(lista_cursos, "buscar", permitir_cancelar=True)
            if not id_cur:
                continue

            curso_obj = cur.buscar_curso_por_id(lista_cursos, id_cur)
            if curso_obj:
                ui.mostrar_tabla_cursos([curso_obj])
            else:
                ui.mostrar_mensaje(f"Curso con ID {id_cur} no encontrado.", "error")

        elif opcion == "6":  # Volver
            break

        input("\nPresione Enter para continuar...")


def gestionar_carreras(lista_carreras: List[Dict[str, Any]], lista_estudiantes: List[Dict[str, Any]]):
    """Bucle del submenú de gestión de carreras."""
    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_crud("Carrera")

        if opcion == "1":  # Crear
            datos_carrera = ui.pedir_datos_carrera()
            if datos_carrera is None:
                ui.mostrar_mensaje("Creación de carrera cancelada.", "info")
                continue

            (nombre_carrera,) = datos_carrera
            resultado = srv.srv_registrar_carrera(lista_carreras, nombre_carrera)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                car.guardar_carreras(lista_carreras)

        elif opcion == "2":  # Ver todos
            ui.mostrar_tabla_carreras(lista_carreras)

        elif opcion == "3":  # Actualizar
            id_car = ui.seleccionar_carrera(lista_carreras, "actualizar", permitir_cancelar=True)
            if not id_car:
                continue

            carrera_obj = car.buscar_carrera_por_id(lista_carreras, id_car)
            if not carrera_obj:
                 ui.mostrar_mensaje(f"Error: Carrera {id_car} no encontrada.", "error")
                 continue

            ui.mostrar_mensaje(f"Actualizando a: {carrera_obj['nombre_carrera']}", "info")
            datos_nuevos = ui.pedir_datos_carrera(actualizando=True)
            if datos_nuevos is None:
                ui.mostrar_mensaje("Actualización cancelada.", "info")
                continue

            (n_nombre,) = datos_nuevos
            resultado = srv.srv_actualizar_carrera(lista_carreras, id_car, n_nombre)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                car.guardar_carreras(lista_carreras)

        elif opcion == "4":  # Eliminar
            id_car = ui.seleccionar_carrera(lista_carreras, "eliminar", permitir_cancelar=True)
            if not id_car:
                continue

            resultado = srv.srv_eliminar_carrera(lista_carreras, lista_estudiantes, id_car)
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                car.guardar_carreras(lista_carreras)

        elif opcion == "5":  # Buscar
            id_car = ui.seleccionar_carrera(lista_carreras, "buscar", permitir_cancelar=True)
            if not id_car:
                continue

            carrera_obj = car.buscar_carrera_por_id(lista_carreras, id_car)
            if carrera_obj:
                ui.mostrar_tabla_carreras([carrera_obj])
            else:
                ui.mostrar_mensaje(f"Carrera con ID {id_car} no encontrada.", "error")

        elif opcion == "6":  # Volver
            break

        input("\nPresione Enter para continuar...")


def gestionar_matriculas(
    lista_estudiantes: List[Dict[str, Any]],
    lista_cursos: List[Dict[str, Any]],
    lista_carreras: List[Dict[str, Any]],
    lista_matriculas: List[Dict[str, Any]]
):
    """Bucle del submenú de gestión de matrículas."""
    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_matriculas()

        if opcion == "1":  # Matricular estudiante
            id_est, ids_cursos, periodo = ui.pedir_datos_matricula(lista_estudiantes, lista_carreras, lista_cursos)

            # Esta comprobación ahora captura la cancelación de forma natural
            if not id_est or not ids_cursos or not periodo:
                ui.mostrar_mensaje("Matrícula cancelada.", "info")
                continue

            resultado = srv.srv_matricular_estudiante(
                id_est, ids_cursos, periodo,
                lista_estudiantes, lista_cursos, lista_matriculas
            )
            ui.mostrar_mensaje(resultado["mensaje"], resultado["tipo"])
            if resultado["tipo"] == "exito":
                mat.guardar_matriculas(lista_matriculas)

        elif opcion == "2":  # Ver cursos de un estudiante
            id_est = ui.seleccionar_estudiante(lista_estudiantes, lista_carreras, "consultar", permitir_cancelar=True)
            if not id_est:
                continue

            est_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)
            if not est_obj:
                ui.mostrar_mensaje(f"Estudiante con ID {id_est} no encontrado.", "error")
            else:
                cursos_est = mat.obtener_cursos_por_estudiante(id_est, lista_matriculas, lista_cursos)
                total_cred = mat.calcular_total_creditos(id_est, lista_matriculas, lista_cursos)
                ui.mostrar_cursos_matriculados(est_obj, cursos_est, total_cred, lista_carreras)

        elif opcion == "3":  # Ver estudiantes en un curso
            id_curso = ui.seleccionar_curso(lista_cursos, "consultar", permitir_cancelar=True)
            if not id_curso:
                continue

            curso_obj = cur.buscar_curso_por_id(lista_cursos, id_curso)
            if not curso_obj:
                ui.mostrar_mensaje(f"Curso con ID {id_curso} no encontrado.", "error")
            else:
                est_curso = mat.obtener_estudiantes_por_curso(id_curso, lista_matriculas, lista_estudiantes)
                ui.mostrar_estudiantes_en_curso(curso_obj, est_curso, lista_carreras)

        # BUG CORREGIDO: Se quitó el '.' de "4."
        elif opcion == "4":  # Volver
            break

        input("\nPresione Enter para continuar...")


def main():
    """Función principal que ejecuta la aplicación."""
    try:
        lista_estudiantes = est.cargar_estudiantes()
        lista_cursos = cur.cargar_cursos()
        lista_matriculas = mat.cargar_matriculas()
        lista_carreras = car.cargar_carreras()
        ui.mostrar_mensaje("Datos cargados correctamente", "info")
    except Exception as e:
        ui.mostrar_mensaje(f"Error fatal al cargar datos: {e}", "error")
        return

    input("Presione Enter para iniciar...")

    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_principal()

        if opcion == "1":
            gestionar_estudiantes(lista_estudiantes, lista_carreras, lista_matriculas)

        elif opcion == "2":
            gestionar_cursos(lista_cursos, lista_matriculas)

        elif opcion == "3":
            gestionar_carreras(lista_carreras, lista_estudiantes)

        elif opcion == "4":
            gestionar_matriculas(lista_estudiantes, lista_cursos, lista_carreras, lista_matriculas)

        elif opcion == "5":
            ui.mostrar_mensaje("¡Hasta luego!", "info")
            break


if __name__ == "__main__":
    main()