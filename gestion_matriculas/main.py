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
    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_crud("Estudiante")

        if opcion == "1":  # Crear
            # TODO (Daniel): Flujo de creación
            # 1. Pedir datos: nombre, carrera = ui.pedir_datos_estudiante()
            # 2. Crear el objeto: nuevo_est = est.crear_estudiante(lista_estudiantes, nombre, carrera)
            # 3. Añadir a la lista: lista_estudiantes.append(nuevo_est)
            # 4. Guardar en CSV: est.guardar_estudiantes(lista_estudiantes)
            # 5. Mostrar éxito: ui.mostrar_mensaje("Estudiante creado con éxito")
            pass

        elif opcion == "2":  # Ver todos
            # TODO (Daniel): Flujo de visualización
            # 1. Mostrar tabla: ui.mostrar_tabla_estudiantes(lista_estudiantes)
            pass

        elif opcion == "3":  # Actualizar
            # TODO (Daniel): Flujo de actualización
            # 1. Pedir ID: id_est = ui.pedir_id("estudiante a actualizar")
            # 2. Buscar: estudiante_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)
            # 3. Si no existe: ui.mostrar_mensaje("Estudiante no encontrado", "error")
            # 4. Si existe:
            #    a. Pedir nuevos datos: n_nombre, n_carrera = ui.pedir_datos_estudiante()
            #    b. Actualizar: est.actualizar_estudiante(estudiante_obj, n_nombre, n_carrera)
            #    c. Guardar: est.guardar_estudiantes(lista_estudiantes)
            #    d. Mostrar éxito: ui.mostrar_mensaje("Estudiante actualizado")
            pass

        elif opcion == "4":  # Eliminar
            # TODO (Daniel): Flujo de eliminación
            # 1. Pedir ID: id_est = ui.pedir_id("estudiante a eliminar")
            # 2. Eliminar: exito = est.eliminar_estudiante(lista_estudiantes, id_est)
            # 3. Si exito:
            #    a. Guardar: est.guardar_estudiantes(lista_estudiantes)
            #    b. Mensaje: ui.mostrar_mensaje("Estudiante eliminado")
            # 4. Si no exito: ui.mostrar_mensaje("Estudiante no encontrado", "error")
            pass

        elif opcion == "5":  # Buscar
            # TODO (Daniel): Flujo de búsqueda
            # 1. Pedir ID: id_est = ui.pedir_id("estudiante a buscar")
            # 2. Buscar: estudiante_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)
            # 3. Si existe: ui.mostrar_tabla_estudiantes([estudiante_obj]) # Mostrar tabla con un solo item
            # 4. Si no existe: ui.mostrar_mensaje("Estudiante no encontrado", "error")
            pass

        elif opcion == "6":  # Volver
            break

        input("\nPresione Enter para continuar...")


def gestionar_cursos():
    """Bucle del submenú de gestión de cursos."""
    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_crud("Curso")

        # TODO (Daniel): Implementar los flujos 1-6 para Cursos
        # Es idéntico al de gestionar_estudiantes, pero llamando
        # a las funciones de ui.pedir_datos_curso() y cur.*

        if opcion == "6":
            break

        input("\nPresione Enter para continuar...")


def gestionar_matriculas():
    """Bucle del submenú de gestión de matrículas."""
    global lista_matriculas  # Indicar que modificaremos la lista global

    while True:
        utils.limpiar_pantalla()
        opcion = ui.mostrar_menu_matriculas()

        if opcion == "1":  # Matricular estudiante
            # TODO (Daniel): Flujo de matriculación
            # 1. Pedir datos: id_est, ids_cursos, periodo = ui.pedir_datos_matricula()
            # 2. (Validación) Verificar que id_est existe en lista_estudiantes
            # 3. (Validación) Verificar que todos los ids_cursos existen en lista_cursos
            # 4. Si todo OK:
            #    a. Crear: nueva_mat = mat.matricular_estudiante(lista_matriculas, id_est, ids_cursos, periodo)
            #    b. Añadir: lista_matriculas.append(nueva_mat)
            #    c. Guardar: mat.guardar_matriculas(lista_matriculas)
            #    d. Mensaje: ui.mostrar_mensaje("Matrícula registrada")
            # 5. Si algo falla: ui.mostrar_mensaje("Error, ID de estudiante o curso no válido", "error")
            pass

        elif opcion == "2":  # Ver cursos de un estudiante
            # TODO (Daniel): Flujo de visualización
            # 1. Pedir ID: id_est = ui.pedir_id("estudiante")
            # 2. Buscar estudiante: est_obj = est.buscar_estudiante_por_id(lista_estudiantes, id_est)
            # 3. Si no existe: ui.mostrar_mensaje("Estudiante no encontrado", "error")
            # 4. Si existe:
            #    a. Obtener cursos: cursos_est = mat.obtener_cursos_por_estudiante(id_est, lista_matriculas, lista_cursos)
            #    b. (Reto) Calcular créditos: total_cred = mat.calcular_total_creditos(id_est, lista_matriculas, lista_cursos)
            #    c. Mostrar: ui.mostrar_cursos_matriculados(est_obj, cursos_est, total_cred)
            pass

        elif opcion == "3":  # Ver estudiantes en un curso
            # TODO (Daniel): Flujo de visualización
            # 1. Pedir ID: id_curso = ui.pedir_id("curso")
            # 2. Buscar curso: curso_obj = cur.buscar_curso_por_id(lista_cursos, id_curso)
            # 3. Si no existe: ui.mostrar_mensaje("Curso no encontrado", "error")
            # 4. Si existe:
            #    a. Obtener estudiantes: est_curso = mat.obtener_estudiantes_por_curso(id_curso, lista_matriculas, lista_estudiantes)
            #    b. Mostrar: ui.mostrar_estudiantes_en_curso(curso_obj, est_curso)
            pass

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