from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from typing import List, Dict, Any, Tuple

# Inicializar la consola de Rich
console = Console()


def mostrar_menu_principal() -> str:
    """Muestra el menú principal y solicita una opción."""
    console.print(Panel(
        "[bold cyan]Sistema de Gestión de Matrículas Académicas[/bold cyan]\n"
        "1. Gestión de Estudiantes\n"
        "2. Gestión de Cursos\n"
        "3. Gestión de Matrículas\n"
        "4. Salir",
        title="Menú Principal",
        border_style="blue"
    ))
    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3", "4"], default="4")
    return opcion


def mostrar_menu_crud(entidad: str) -> str:
    """Muestra el menú CRUD genérico para una entidad (Estudiante o Curso)."""
    console.print(Panel(
        f"1. Crear {entidad}\n"
        f"2. Ver todos los {entidad}s\n"
        f"3. Actualizar {entidad}\n"
        f"4. Eliminar {entidad}\n"
        f"5. Buscar {entidad}\n"
        f"6. Volver al menú principal",
        title=f"Gestión de {entidad}s",
        border_style="green"
    ))
    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3", "4", "5", "6"], default="6")
    return opcion


def mostrar_menu_matriculas() -> str:
    """Muestra el menú específico de matrículas."""
    console.print(Panel(
        "1. Matricular estudiante en cursos\n"
        "2. Ver cursos de un estudiante\n"
        "3. Ver estudiantes en un curso\n"
        "4. Volver al menú principal",
        title="Gestión de Matrículas",
        border_style="yellow"
    ))
    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3", "4"], default="4")
    return opcion


def mostrar_tabla_estudiantes(estudiantes: List[Dict[str, Any]]) -> None:
    """Muestra una tabla 'rich' con la lista de estudiantes."""
    # TODO (Daniel): Implementar la tabla
    # 1. Crear un objeto Table(title="Lista de Estudiantes")
    # 2. Añadir columnas: table.add_column("ID"), table.add_column("Nombre"), table.add_column("Carrera")
    # 3. Iterar sobre la lista 'estudiantes':
    #    table.add_row(est['id_estudiante'], est['nombre'], est['carrera'])
    # 4. console.print(table)
    pass


def mostrar_tabla_cursos(cursos: List[Dict[str, Any]]) -> None:
    """Muestra una tabla 'rich' con la lista de cursos."""
    # TODO (Daniel): Implementar la tabla
    # Similar a la de estudiantes, pero con "ID Curso", "Nombre Curso", "Créditos"
    # ¡Recuerda convertir 'creditos' a str() para la tabla! -> str(curso['creditos'])
    pass


def mostrar_cursos_matriculados(estudiante: Dict[str, Any], cursos: List[Dict[str, Any]],
                                creditos_totales: int) -> None:
    """Muestra los cursos de un estudiante y el total de créditos (Reto Final)."""
    # TODO (Daniel): Implementar
    # 1. Crear una tabla 'Table' para los cursos (ID, Nombre, Créditos)
    # 2. Llenar la tabla con la lista 'cursos'
    # 3. Crear un 'Panel' que muestre la tabla y el total de créditos.
    #    Ej: Panel(
    #        f"[bold]Estudiante:[/bold] {estudiante['nombre']}\n"
    #        f"[bold]Carrera:[/bold] {estudiante['carrera']}\n\n"
    #        table,  # <-- La tabla va aquí adentro
    #        f"\n[bold]Total Créditos Matriculados:[/bold] {creditos_totales}",
    #        title="Cursos Matriculados"
    #    )
    # 4. Imprimir el panel.
    pass


def mostrar_estudiantes_en_curso(curso: Dict[str, Any], estudiantes: List[Dict[str, Any]]) -> None:
    """Muestra los estudiantes inscritos en un curso."""
    # TODO (Daniel): Implementar
    # Similar al anterior.
    # 1. Crear tabla de estudiantes (ID, Nombre, Carrera)
    # 2. Llenar la tabla
    # 3. Crear Panel que muestre el nombre del curso y la tabla de estudiantes.
    pass


def mostrar_mensaje(mensaje: str, tipo: str = "info") -> None:
    """Muestra un mensaje de éxito (verde) o error (rojo)."""
    if tipo == "error":
        console.print(Panel(f"[bold red]{mensaje}[/bold red]", title="Error", border_style="red"))
    else:
        console.print(Panel(f"[bold green]{mensaje}[/bold green]", title="Éxito", border_style="green"))


# --- Funciones para pedir datos ---

def pedir_datos_estudiante() -> Tuple[str, str]:
    """Pide nombre y carrera para un nuevo estudiante."""
    nombre = Prompt.ask("[bold]Ingrese nombre del estudiante[/bold]")
    carrera = Prompt.ask("[bold]Ingrese carrera del estudiante[/bold]")
    return nombre, carrera


def pedir_datos_curso() -> Tuple[str, int]:
    """Pide nombre y créditos para un nuevo curso."""
    nombre_curso = Prompt.ask("[bold]Ingrese nombre del curso[/bold]")
    # IntPrompt valida que sea un número
    creditos = IntPrompt.ask("[bold]Ingrese créditos del curso[/bold]")
    return nombre_curso, creditos


def pedir_id(entidad: str) -> str:
    """Pide un ID genérico."""
    return Prompt.ask(f"[bold]Ingrese el ID del {entidad}[/bold]")


def pedir_datos_matricula() -> Tuple[str, List[str], str]:
    """Pide los datos para una nueva matrícula."""
    id_estudiante = Prompt.ask("[bold]ID del estudiante a matricular[/bold]")
    periodo = Prompt.ask("[bold]Periodo académico (Ej. 2025-01)[/bold]")

    cursos_str = Prompt.ask("[bold]IDs de los cursos (separados por coma, Ej. C001,C002)[/bold]")
    # Convertimos el string "C001,C002" en una lista ["C001", "C002"]
    lista_ids_cursos = [id.strip() for id in cursos_str.split(',')]

    return id_estudiante, lista_ids_cursos, periodo