# Importar los módulos del proyecto
import gestion_matriculas.estudiantes as est
import gestion_matriculas.cursos as cur
import gestion_matriculas.matriculas as mat
import gestion_matriculas.ui as ui
import gestion_matriculas.utils as utils

# Variables globales para almacenar los datos en memoria
lista_estudiantes = []
lista_cursos = []
lista_matriculas = []


def gestionar_estudiantes():
    """Bucle del submenú de gestión de estudiantes."""
    global lista_estudiantes  # Necesario para modificar la lista global

    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_crud("Estudiante")

        if opcion == "1":  # Crear
            nombre, carrera = ui.pedir_datos_estudiante()
            if not nombre or not carrera:
                ui.mostrar_mensaje("Nombre y carrera no pueden estar vacíos.", "error")
            else:
                nuevo_est = est.crear_estudiante(lista_estudiantes, nombre, carrera)
                lista_estudiantes.append(nuevo_est)
                est.guardar_estudiantes(lista_estudiantes)
                ui.mostrar_mensaje(f"Estudiante '{nombre}' creado con ID {nuevo_est['id_estudiante']}", "exito")

        elif opcion == "2":  # Ver todos
            ui.mostrar_tabla_estudiantes(lista_estudiantes)

        elif opcion == "3":  # Actualizar
            id_est = ui.pedir_id("estudiante a actualizar")
            estudiante_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)

            if not estudiante_obj:
                ui.mostrar_mensaje(f"Estudiante con ID {id_est} no encontrado.", "error")
            else:
                ui.mostrar_mensaje(f"Actualizando a: {estudiante_obj['nombre']}", "info")
                n_nombre, n_carrera = ui.pedir_datos_estudiante(actualizando=True)

                if not n_nombre and not n_carrera:
                    ui.mostrar_mensaje("No se ingresaron datos para actualizar.", "info")
                else:
                    est.actualizar_estudiante(estudiante_obj, n_nombre, n_carrera)
                    est.guardar_estudiantes(lista_estudiantes)
                    ui.mostrar_mensaje("Estudiante actualizado con éxito.", "exito")

        elif opcion == "44":  # Eliminar
            id_est = ui.pedir_id("estudiante a eliminar")
            exito = est.eliminar_estudiante(lista_estudiantes, id_est)

            if exito:
                est.guardar_estudiantes(lista_estudiantes)
                ui.mostrar_mensaje(f"Estudiante con ID {id_est} eliminado.", "exito")
            else:
                ui.mostrar_mensaje(f"Estudiante con ID {id_est} no encontrado.", "error")

        elif opcion == "5":  # Buscar
            id_est = ui.pedir_id("estudiante a buscar")
            estudiante_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)

            if estudiante_obj:
                ui.mostrar_tabla_estudiantes([estudiante_obj])  # Mostrar tabla con un solo item
            else:
                ui.mostrar_mensaje(f"Estudiante con ID {id_est} no encontrado.", "error")

        elif opcion == "6":  # Volver
            break

        input("\nPresione Enter para continuar...")


def gestionar_cursos():
    """Bucle del submenú de gestión de cursos."""
    global lista_cursos  # Necesario para modificar la lista global

    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_crud("Curso")

        if opcion == "1":  # Crear
            nombre, creditos = ui.pedir_datos_curso()
            if not nombre:
                ui.mostrar_mensaje("El nombre del curso no puede estar vacío.", "error")
            else:
                nuevo_cur = cur.crear_curso(lista_cursos, nombre, creditos)
                lista_cursos.append(nuevo_cur)
                cur.guardar_cursos(lista_cursos)
                ui.mostrar_mensaje(f"Curso '{nombre}' creado con ID {nuevo_cur['id_curso']}", "exito")

        elif opcion == "2":  # Ver todos
            ui.mostrar_tabla_cursos(lista_cursos)

        elif opcion == "3":  # Actualizar
            id_cur = ui.pedir_id("curso a actualizar")
            curso_obj = cur.buscar_curso_por_id(lista_cursos, id_cur)

            if not curso_obj:
                ui.mostrar_mensaje(f"Curso con ID {id_cur} no encontrado.", "error")
            else:
                ui.mostrar_mensaje(f"Actualizando a: {curso_obj['nombre_curso']}", "info")
                n_nombre, n_creditos = ui.pedir_datos_curso(actualizando=True)

                if not n_nombre and n_creditos < 0:
                    ui.mostrar_mensaje("No se ingresaron datos para actualizar.", "info")
                else:
                    cur.actualizar_curso(curso_obj, n_nombre, n_creditos)
                    cur.guardar_cursos(lista_cursos)
                    ui.mostrar_mensaje("Curso actualizado con éxito.", "exito")

        elif opcion == "4":  # Eliminar
            id_cur = ui.pedir_id("curso a eliminar")
            exito = cur.eliminar_curso(lista_cursos, id_cur)

            if exito:
                cur.guardar_cursos(lista_cursos)
                ui.mostrar_mensaje(f"Curso con ID {id_cur} eliminado.", "exito")
            else:
                ui.mostrar_mensaje(f"Curso con ID {id_cur} no encontrado.", "error")

        elif opcion == "5":  # Buscar
            id_cur = ui.pedir_id("curso a buscar")
            curso_obj = cur.buscar_curso_por_id(lista_cursos, id_cur)

            if curso_obj:
                ui.mostrar_tabla_cursos([curso_obj])
            else:
                ui.mostrar_mensaje(f"Curso con ID {id_cur} no encontrado.", "error")

        elif opcion == "6":  # Volver
            break

        input("\nPresione Enter para continuar...")


def gestionar_matriculas():
    """Bucle del submenú de gestión de matrículas."""
    global lista_matriculas  # Indicar que modificaremos la lista global

    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_matriculas()

        if opcion == "1":  # Matricular estudiante
            id_est, ids_cursos, periodo = ui.pedir_datos_matricula()

            # 2. (Validación) Verificar que id_est existe
            est_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)
            if not est_obj:
                ui.mostrar_mensaje(f"ID de estudiante {id_est} no existe.", "error")
                input("\nPresione Enter para continuar...")
                continue  # Volver al menú de matrículas

            # 3. (Validación) Verificar que todos los ids_cursos existen
            cursos_validos = []
            cursos_invalidos = []
            for id_c in ids_cursos:
                cur_obj = cur.buscar_curso_por_id(lista_cursos, id_c)
                if cur_obj:
                    cursos_validos.append(id_c)
                else:
                    cursos_invalidos.append(id_c)

            if cursos_invalidos:
                ui.mostrar_mensaje(f"IDs de curso no válidos: {', '.join(cursos_invalidos)}", "error")
                if not cursos_validos:
                    input("\nPresione Enter para continuar...")
                    continue  # Volver al menú

            if not cursos_validos:
                ui.mostrar_mensaje("No se proporcionaron cursos válidos.", "error")
                input("\nPresione Enter para continuar...")
                continue

            # 4. Si todo OK:
            nueva_mat = mat.matricular_estudiante(lista_matriculas, id_est, cursos_validos, periodo)
            lista_matriculas.append(nueva_mat)
            mat.guardar_matriculas(lista_matriculas)
            ui.mostrar_mensaje(f"Estudiante {est_obj['nombre']} matriculado en {len(cursos_validos)} curso(s).",
                               "exito")

        elif opcion == "2":  # Ver cursos de un estudiante
            id_est = ui.pedir_id("estudiante")
            est_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)

            if not est_obj:
                ui.mostrar_mensaje(f"Estudiante con ID {id_est} no encontrado.", "error")
            else:
                # Obtener cursos
                cursos_est = mat.obtener_cursos_por_estudiante(id_est, lista_matriculas, lista_cursos)
                # (Reto) Calcular créditos
                total_cred = mat.calcular_total_creditos(id_est, lista_matriculas, lista_cursos)
                # Mostrar
                ui.mostrar_cursos_matriculados(est_obj, cursos_est, total_cred)

        elif opcion == "3":  # Ver estudiantes en un curso
            id_curso = ui.pedir_id("curso")
            curso_obj = cur.buscar_curso_por_id(lista_cursos, id_curso)

            if not curso_obj:
                ui.mostrar_mensaje(f"Curso con ID {id_curso} no encontrado.", "error")
            else:
                # Obtener estudiantes
                est_curso = mat.obtener_estudiantes_por_curso(id_curso, lista_matriculas, lista_estudiantes)
                # Mostrar
                ui.mostrar_estudiantes_en_curso(curso_obj, est_curso)

        elif opcion == "4":  # Volver
            break

        input("\nPresione Enter para continuar...")


def main():
    """Función principal que ejecuta la aplicación."""
    global lista_estudiantes, lista_cursos, lista_matriculas

    # Cargar datos al iniciar
    try:
        lista_estudiantes = est.cargar_estudiantes()
        lista_cursos = cur.cargar_cursos()
        lista_matriculas = mat.cargar_matriculas()
        ui.mostrar_mensaje("Datos cargados correctamente", "info")
    except Exception as e:
        ui.mostrar_mensaje(f"Error fatal al cargar datos: {e}", "error")
        return  # Salir si no se pueden cargar los datos

    input("Presione Enter para iniciar...")

    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_principal()

        if opcion == "1":
            gestionar_estudiantes()

        elif opcion == "2":
            gestionar_cursos()

        elif opcion == "3":
            gestionar_matriculas()

        elif opcion == "4":
            ui.mostrar_mensaje("¡Hasta luego!", "info")
            break


if __name__ == "__main__":
    main()