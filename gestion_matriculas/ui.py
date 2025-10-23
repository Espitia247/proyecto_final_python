from rich.console import Console
from rich.table import Table
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
        border_style="blue",
        width=60
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
        border_style="green",
        width=60
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
        border_style="yellow",
        width=60
    ))
    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3", "4"], default="4")
    return opcion


def mostrar_tabla_estudiantes(estudiantes: List[Dict[str, Any]]) -> None:
    """Muestra una tabla 'rich' con la lista de estudiantes."""
    if not estudiantes:
        mostrar_mensaje("No hay estudiantes para mostrar.", "info")
        return

    table = Table(title="Lista de Estudiantes", border_style="magenta", show_header=True, header_style="bold magenta")
    table.add_column("ID Estudiante", style="dim", width=12)
    table.add_column("Nombre", min_width=20)
    table.add_column("Carrera", min_width=20)

    for est in estudiantes:
        table.add_row(est['id_estudiante'], est['nombre'], est['carrera'])

    console.print(table)


def mostrar_tabla_cursos(cursos: List[Dict[str, Any]]) -> None:
    """Muestra una tabla 'rich' con la lista de cursos."""
    if not cursos:
        mostrar_mensaje("No hay cursos para mostrar.", "info")
        return

    table = Table(title="Lista de Cursos", border_style="cyan", show_header=True, header_style="bold cyan")
    table.add_column("ID Curso", style="dim", width=12)
    table.add_column("Nombre del Curso", min_width=20)
    table.add_column("Créditos", justify="right")

    for curso in cursos:
        # Convertir créditos a str para la tabla
        table.add_row(curso['id_curso'], curso['nombre_curso'], str(curso['creditos']))

    console.print(table)


def mostrar_cursos_matriculados(estudiante: Dict[str, Any], cursos: List[Dict[str, Any]],
                                creditos_totales: int) -> None:
    """Muestra los cursos de un estudiante y el total de créditos (Reto Final)."""
    table = Table(title="Cursos", show_header=True, header_style="bold cyan")
    table.add_column("ID Curso", style="dim", width=12)
    table.add_column("Nombre del Curso", min_width=20)
    table.add_column("Créditos", justify="right")

    if not cursos:
        table.add_row("[dim]Sin cursos matriculados[/dim]", "", "")
    else:
        for curso in cursos:
            table.add_row(curso['id_curso'], curso['nombre_curso'], str(curso['creditos']))

    panel_content = (
        f"[bold]Estudiante:[/bold] {estudiante['nombre']}\n"
        f"[bold]Carrera:[/bold] {estudiante['carrera']}\n\n"
    )

    console.print(Panel(
        panel_content,
        title=f"Cursos Matriculados - {estudiante['id_estudiante']}",
        border_style="green",
        width=60
    ))
    console.print(table)
    console.print(f"\n[bold green]Total Créditos Matriculados (último periodo):[/bold green] {creditos_totales}\n")


def mostrar_estudiantes_en_curso(curso: Dict[str, Any], estudiantes: List[Dict[str, Any]]) -> None:
    """Muestra los estudiantes inscritos en un curso."""
    table = Table(title="Estudiantes Inscritos", show_header=True, header_style="bold magenta")
    table.add_column("ID Estudiante", style="dim", width=12)
    table.add_column("Nombre", min_width=20)
    table.add_column("Carrera", min_width=20)

    if not estudiantes:
        table.add_row("[dim]Sin estudiantes inscritos[/dim]", "", "")
    else:
        for est in estudiantes:
            table.add_row(est['id_estudiante'], est['nombre'], est['carrera'])

    panel_content = (
        f"[bold]Curso:[/bold] {curso['nombre_curso']}\n"
        f"[bold]Créditos:[/bold] {curso['creditos']}\n\n"
    )

    console.print(Panel(
        panel_content,
        title=f"Lista de Estudiantes - {curso['id_curso']}",
        border_style="green",
        width=60
    ))
    console.print(table)


def mostrar_mensaje(mensaje: str, tipo: str = "info") -> None:
    """Muestra un mensaje de éxito (verde), error (rojo) o info (amarillo)."""
    if tipo == "error":
        console.print(Panel(f"[bold red]{mensaje}[/bold red]", title="Error", border_style="red", width=60))
    elif tipo == "info":
        console.print(Panel(f"[bold yellow]{mensaje}[/bold yellow]", title="Aviso", border_style="yellow", width=60))
    else:  # "exito"
        console.print(Panel(f"[bold green]{mensaje}[/bold green]", title="Éxito", border_style="green", width=60))


# --- Funciones para pedir datos ---

def pedir_datos_estudiante(actualizando: bool = False) -> Tuple[str, str]:
    """Pide nombre y carrera. Si actualiza, permite dejar en blanco."""
    aviso = " (Presione Enter para no cambiar)" if actualizando else ""
    nombre = Prompt.ask(f"[bold]Ingrese nombre del estudiante[/bold]{aviso}")
    carrera = Prompt.ask(f"[bold]Ingrese carrera del estudiante[/bold]{aviso}")
    return nombre, carrera


def pedir_datos_curso(actualizando: bool = False) -> Tuple[str, int]:
    """Pide nombre y créditos. Si actualiza, permite dejar en blanco."""
    aviso = " (Presione Enter para no cambiar)" if actualizando else ""
    nombre_curso = Prompt.ask(f"[bold]Ingrese nombre del curso[/bold]{aviso}")

    if actualizando:
        # Permite dejar en blanco, en cuyo caso retornamos -1
        creditos_str = Prompt.ask(f"[bold]Ingrese créditos del curso[/bold]{aviso}", default="-1")
        try:
            creditos = int(creditos_str)
        except ValueError:
            creditos = -1  # Señal para no actualizar
    else:
        # Si está creando, obliga a que sea un número válido >= 0
        creditos = IntPrompt.ask("[bold]Ingrese créditos del curso[/bold]", default="0")
        while creditos < 0:
            mostrar_mensaje("Los créditos deben ser 0 o más.", "error")
            creditos = IntPrompt.ask("[bold]Ingrese créditos del curso[/bold]", default="0")

    return nombre_curso, creditos


def pedir_id(entidad: str) -> str:
    """Pide un ID genérico."""
    return Prompt.ask(f"[bold]Ingrese el ID del {entidad}[/bold]").strip().upper()


def pedir_datos_matricula() -> Tuple[str, List[str], str]:
    """Pide los datos para una nueva matrícula."""
    id_estudiante = Prompt.ask("[bold]ID del estudiante a matricular[/bold]").strip().upper()
    periodo = Prompt.ask("[bold]Periodo académico (Ej. 2025-01)[/bold]", default="2025-01")

    cursos_str = Prompt.ask("[bold]IDs de los cursos (separados por coma, Ej. C001,C002)[/bold]")
    # Convertimos el string "C001, C002" en una lista ["C001", "C002"]
    lista_ids_cursos = [id.strip().upper() for id in cursos_str.split(',') if id.strip()]

    return id_estudiante, lista_ids_cursos, periodo