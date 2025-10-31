"""
Módulo de Interfaz de Usuario (ui.py)

Utiliza la librería 'rich' para renderizar todos los componentes
visuales de la aplicación en la consola.

NUEVO: En cualquier formulario de entrada de texto, el usuario
puede escribir 'q!' para cancelar la operación y volver al menú.
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from typing import List, Dict, Any, Tuple, Optional

# Inicializar la consola de Rich
console = Console()

# --- CONSTANTE DE CANCELACIÓN ---
CANCEL_KEYWORD = "q!"
CANCEL_MESSAGE = f"Tip: Escriba [bold yellow]{CANCEL_KEYWORD}[/bold yellow] en cualquier campo para cancelar."


def mostrar_menu_principal() -> str:
    """Muestra el menú principal y solicita una opción."""
    console.print(Panel(
        "[bold cyan]Sistema de Gestión de Matrículas Académicas[/bold cyan]\n"
        "1. Gestión de Estudiantes\n"
        "2. Gestión de Cursos\n"
        "3. Gestión de Carreras\n"
        "4. Gestión de Matrículas\n"
        "5. Salir",
        title="Menú Principal",
        border_style="blue",
        width=60
    ))
    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3", "4", "5"], default="5")
    return opcion


def mostrar_menu_crud(entidad: str) -> str:
    """Muestra el menú CRUD genérico para una entidad (Estudiante, Curso o Carrera)."""
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


# --- Funciones de Mostrar Tablas ---

def _resolver_nombre_carrera(id_carrera: Optional[str], lista_carreras: List[Dict[str, Any]]) -> str:
    """Función helper para buscar el nombre de una carrera por su ID."""
    if not id_carrera:
        return "[N/A]"
    for carrera in lista_carreras:
        if carrera["id_carrera"] == id_carrera:
            return carrera["nombre_carrera"]
    return "[Carrera Desconocida]"


def mostrar_tabla_estudiantes(estudiantes: List[Dict[str, Any]], lista_carreras: List[Dict[str, Any]]) -> None:
    """
    Muestra una tabla 'rich' con la lista de estudiantes.
    Resuelve el 'id_carrera' para mostrar el nombre de la carrera.
    """
    if not estudiantes:
        mostrar_mensaje("No hay estudiantes para mostrar.", "info")
        return

    table = Table(title="Lista de Estudiantes", border_style="magenta", show_header=True, header_style="bold magenta")
    table.add_column("ID Estudiante", style="dim", width=12)
    table.add_column("Nombre", min_width=20)
    table.add_column("Carrera", min_width=20)

    for est in estudiantes:
        nombre_carrera = _resolver_nombre_carrera(est.get('id_carrera'), lista_carreras)
        table.add_row(est['id_estudiante'], est['nombre'], nombre_carrera)

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
        table.add_row(curso['id_curso'], curso['nombre_curso'], str(curso.get('creditos', 0)))

    console.print(table)


def mostrar_tabla_carreras(carreras: List[Dict[str, Any]]) -> None:
    """Muestra una tabla 'rich' con la lista de carreras."""
    if not carreras:
        mostrar_mensaje("No hay carreras para mostrar.", "info")
        return

    table = Table(title="Lista de Carreras", border_style="blue", show_header=True, header_style="bold blue")
    table.add_column("ID Carrera", style="dim", width=12)
    table.add_column("Nombre de la Carrera", min_width=20)

    for carrera in carreras:
        table.add_row(carrera['id_carrera'], carrera['nombre_carrera'])

    console.print(table)


def mostrar_cursos_matriculados(estudiante: Dict[str, Any], cursos: List[Dict[str, Any]],
                                creditos_totales: int, lista_carreras: List[Dict[str, Any]]) -> None:
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

    nombre_carrera = _resolver_nombre_carrera(estudiante.get('id_carrera'), lista_carreras)
    panel_content = (
        f"[bold]Estudiante:[/bold] {estudiante['nombre']}\n"
        f"[bold]Carrera:[/bold] {nombre_carrera}\n\n"
    )

    console.print(Panel(
        panel_content,
        title=f"Cursos Matriculados - {estudiante['id_estudiante']}",
        border_style="green",
        width=60
    ))
    console.print(table)
    console.print(f"\n[bold green]Total Créditos Matriculados (último periodo):[/bold green] {creditos_totales}\n")


def mostrar_estudiantes_en_curso(curso: Dict[str, Any], estudiantes: List[Dict[str, Any]],
                                 lista_carreras: List[Dict[str, Any]]) -> None:
    """
    Muestra los estudiantes inscritos en un curso.
    Resuelve el 'id_carrera' para mostrar el nombre.
    """
    table = Table(title="Estudiantes Inscritos", show_header=True, header_style="bold magenta")
    table.add_column("ID Estudiante", style="dim", width=12)
    table.add_column("Nombre", min_width=20)
    table.add_column("Carrera", min_width=20)

    if not estudiantes:
        table.add_row("[dim]Sin estudiantes inscritos[/dim]", "", "")
    else:
        for est in estudiantes:
            nombre_carrera = _resolver_nombre_carrera(est.get('id_carrera'), lista_carreras)
            table.add_row(est['id_estudiante'], est['nombre'], nombre_carrera)

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


# --- Funciones de Pedir Datos (ACTUALIZADAS con 'q!' para cancelar) ---

def _seleccionar_carrera_lista(lista_carreras: List[Dict[str, Any]], aviso: str) -> Optional[str]:
    """
    HELPER: Muestra la lista de carreras y pide seleccionar una.
    Retorna el ID, None si se deja en blanco (actualizando), o 'CANCEL' si se cancela.
    """
    console.print("\n[bold]Seleccione una carrera:[/bold]")
    if not lista_carreras:
        mostrar_mensaje("No hay carreras creadas. Por favor, cree una carrera primero.", "error")
        return "CANCEL"  # No se puede continuar sin carreras

    opciones_carreras = {}
    table = Table(border_style="dim")
    table.add_column("Opción", style="bold yellow")
    table.add_column("ID Carrera", style="dim")
    table.add_column("Nombre de la Carrera")

    for i, carrera in enumerate(lista_carreras, 1):
        opcion_str = str(i)
        table.add_row(opcion_str, carrera['id_carrera'], carrera['nombre_carrera'])
        opciones_carreras[opcion_str] = carrera['id_carrera']

    console.print(table)
    if aviso:
        console.print(f"[dim]{aviso}[/dim]")

    while True:
        opcion_elegida = Prompt.ask(f"[bold]Seleccione una opción[/bold]", default="")

        if opcion_elegida.strip().lower() == CANCEL_KEYWORD:
            return "CANCEL"  # Señal de cancelación

        if opcion_elegida == "" and aviso:
            return None  # Señal para "no cambiar"

        if opcion_elegida in opciones_carreras:
            return opciones_carreras[opcion_elegida]  # Retorna el ID 'CAR001'
        else:
            mostrar_mensaje(f"Opción '{opcion_elegida}' no válida.", "error")


def pedir_datos_estudiante(lista_carreras: List[Dict[str, Any]], actualizando: bool = False) -> Optional[
    Tuple[str, Optional[str]]]:
    """
    Pide nombre y permite SELECCIONAR una carrera.
    Retorna None si el usuario cancela la operación.

    Returns:
        Optional[Tuple[str, Optional[str]]]: (nombre, id_carrera_seleccionada) o None
    """
    console.print(Panel(CANCEL_MESSAGE, border_style="dim", width=60))

    aviso_nombre = " (Presione Enter para no cambiar)" if actualizando else ""
    nombre = Prompt.ask(f"[bold]Ingrese nombre del estudiante[/bold]{aviso_nombre}").strip()
    if nombre.lower() == CANCEL_KEYWORD:
        return None

    aviso_carrera = " (Presione Enter para no cambiar la carrera)" if actualizando else ""
    id_carrera_seleccionada = _seleccionar_carrera_lista(lista_carreras, aviso_carrera)

    if id_carrera_seleccionada == "CANCEL":
        return None  # Cancelación propagada desde el helper

    # Si se está creando y no se seleccionó carrera (porque no hay)
    if not actualizando and id_carrera_seleccionada is None:
        return None  # Cancelar la creación

    return nombre, id_carrera_seleccionada


def pedir_datos_curso(actualizando: bool = False) -> Optional[Tuple[str, Optional[int]]]:
    """
    Pide nombre y créditos. Retorna None si el usuario cancela.
    Se reemplazó IntPrompt para permitir la cancelación.
    """
    console.print(Panel(CANCEL_MESSAGE, border_style="dim", width=60))
    aviso = " (Presione Enter para no cambiar)" if actualizando else ""

    # 1. Pedir Nombre
    nombre_curso = Prompt.ask(f"[bold]Ingrese nombre del curso[/bold]{aviso}").strip()
    if nombre_curso.lower() == CANCEL_KEYWORD:
        return None

    # 2. Pedir Créditos
    creditos: Optional[int] = None
    if actualizando:
        # Permite dejar en blanco, en cuyo caso es None
        while True:
            creditos_str = Prompt.ask(f"[bold]Ingrese créditos del curso[/bold]{aviso}", default="")
            if creditos_str.lower() == CANCEL_KEYWORD:
                return None
            if creditos_str == "":
                creditos = None  # Señal para "no actualizar"
                break
            try:
                creditos = int(creditos_str)
                if creditos < 0:
                    mostrar_mensaje("Los créditos deben ser 0 o más.", "error")
                else:
                    break  # Válido
            except ValueError:
                mostrar_mensaje("Entrada no válida. Debe ser un número.", "error")
    else:
        # Creando: obliga a que sea un número válido >= 0
        while True:
            creditos_str = Prompt.ask("[bold]Ingrese créditos del curso[/bold]", default="0")
            if creditos_str.lower() == CANCEL_KEYWORD:
                return None
            try:
                creditos = int(creditos_str)
                if creditos < 0:
                    mostrar_mensaje("Los créditos deben ser 0 o más.", "error")
                else:
                    break  # Válido
            except ValueError:
                mostrar_mensaje("Entrada no válida. Debe ser un número.", "error")

    return nombre_curso, creditos


def pedir_datos_carrera(actualizando: bool = False) -> Optional[Tuple[str]]:
    """
    Pide los datos para una carrera. Retorna None si el usuario cancela.
    """
    console.print(Panel(CANCEL_MESSAGE, border_style="dim", width=60))
    aviso = " (Presione Enter para no cambiar)" if actualizando else ""

    nombre_carrera = Prompt.ask(f"[bold]Ingrese nombre de la carrera[/bold]{aviso}").strip()
    if nombre_carrera.lower() == CANCEL_KEYWORD:
        return None

    return (nombre_carrera,)


# --- Funciones de Selección (Usadas por Actualizar, Eliminar, Buscar) ---

def seleccionar_estudiante(
        lista_estudiantes: List[Dict[str, Any]],
        lista_carreras: List[Dict[str, Any]],
        accion: str,
        permitir_cancelar: bool = True
) -> Optional[str]:
    """
    Muestra la lista de estudiantes y pide seleccionar uno.
    Devuelve el ID del estudiante seleccionado o None si cancela.
    """
    if not lista_estudiantes:
        mostrar_mensaje("No hay estudiantes para seleccionar.", "info")
        return None

    console.print(f"\n[bold]Seleccione un estudiante para {accion}:[/bold]")

    opciones_map = {}
    table = Table(border_style="dim", width=80)
    table.add_column("Opción", style="bold yellow", width=8)
    table.add_column("ID Estudiante", style="dim", width=12)
    table.add_column("Nombre", min_width=20)
    table.add_column("Carrera", min_width=20)

    for i, est in enumerate(lista_estudiantes, 1):
        opcion_str = str(i)
        nombre_carrera = _resolver_nombre_carrera(est.get('id_carrera'), lista_carreras)
        table.add_row(opcion_str, est['id_estudiante'], est['nombre'], nombre_carrera)
        opciones_map[opcion_str] = est['id_estudiante']

    if permitir_cancelar:
        table.add_row("0", "Cancelar", "", "Volver al menú")
        opciones_map["0"] = None

    console.print(table)

    while True:
        opcion_elegida = Prompt.ask("[bold]Seleccione una opción[/bold]", default="0" if permitir_cancelar else "1")
        if opcion_elegida in opciones_map:
            return opciones_map[opcion_elegida]
        else:
            mostrar_mensaje(f"Opción '{opcion_elegida}' no válida.", "error")


def seleccionar_curso(
        lista_cursos: List[Dict[str, Any]],
        accion: str,
        permitir_cancelar: bool = True
) -> Optional[str]:
    """
    Muestra la lista de cursos y pide seleccionar uno.
    Devuelve el ID del curso seleccionado o None si cancela.
    """
    if not lista_cursos:
        mostrar_mensaje("No hay cursos para seleccionar.", "info")
        return None

    console.print(f"\n[bold]Seleccione un curso para {accion}:[/bold]")

    opciones_map = {}
    table = Table(border_style="dim", width=80)
    table.add_column("Opción", style="bold yellow", width=8)
    table.add_column("ID Curso", style="dim", width=12)
    table.add_column("Nombre del Curso", min_width=20)
    table.add_column("Créditos", justify="right")

    for i, curso in enumerate(lista_cursos, 1):
        opcion_str = str(i)
        table.add_row(opcion_str, curso['id_curso'], curso['nombre_curso'], str(curso.get('creditos', 0)))
        opciones_map[opcion_str] = curso['id_curso']

    if permitir_cancelar:
        table.add_row("0", "Cancelar", "", "Volver al menú")
        opciones_map["0"] = None

    console.print(table)

    while True:
        opcion_elegida = Prompt.ask("[bold]Seleccione una opción[/bold]", default="0" if permitir_cancelar else "1")
        if opcion_elegida in opciones_map:
            return opciones_map[opcion_elegida]
        else:
            mostrar_mensaje(f"Opción '{opcion_elegida}' no válida.", "error")


def seleccionar_carrera(
        lista_carreras: List[Dict[str, Any]],
        accion: str,
        permitir_cancelar: bool = True
) -> Optional[str]:
    """
    Muestra la lista de carreras y pide seleccionar una.
    Devuelve el ID de la carrera seleccionada o None si cancela.
    """
    if not lista_carreras:
        mostrar_mensaje("No hay carreras para seleccionar.", "info")
        return None

    console.print(f"\n[bold]Seleccione una carrera para {accion}:[/bold]")

    opciones_map = {}
    table = Table(border_style="dim", width=80)
    table.add_column("Opción", style="bold yellow", width=8)
    table.add_column("ID Carrera", style="dim", width=12)
    table.add_column("Nombre de la Carrera", min_width=20)

    for i, carrera in enumerate(lista_carreras, 1):
        opcion_str = str(i)
        table.add_row(opcion_str, carrera['id_carrera'], carrera['nombre_carrera'])
        opciones_map[opcion_str] = carrera['id_carrera']

    if permitir_cancelar:
        table.add_row("0", "Cancelar", "", "Volver al menú")
        opciones_map["0"] = None

    console.print(table)

    while True:
        opcion_elegida = Prompt.ask("[bold]Seleccione una opción[/bold]", default="0" if permitir_cancelar else "1")
        if opcion_elegida in opciones_map:
            return opciones_map[opcion_elegida]
        else:
            mostrar_mensaje(f"Opción '{opcion_elegida}' no válida.", "error")


def pedir_datos_matricula(
        lista_estudiantes: List[Dict[str, Any]],
        lista_carreras: List[Dict[str, Any]],
        lista_cursos: List[Dict[str, Any]]
) -> Tuple[Optional[str], List[str], Optional[str]]:
    """
    FUNCIÓN ACTUALIZADA: Guía al usuario paso a paso para la matrícula.
    Permite cancelar con 'q!' en el campo de 'periodo'.

    Returns:
        Tuple[Optional[str], List[str], Optional[str]]: (id_estudiante, lista_ids_cursos, periodo)
        Devuelve (None, [], None) si el usuario cancela en CUALQUIER paso.
    """
    # 1. Seleccionar Estudiante
    id_estudiante = seleccionar_estudiante(lista_estudiantes, lista_carreras, "matricular", permitir_cancelar=True)
    if not id_estudiante:
        return None, [], None  # Cancelar toda la operación

    # 2. Seleccionar Cursos (multi-selección)
    console.print("\n[bold]Seleccione los cursos a matricular (uno por uno):[/bold]")

    if not lista_cursos:
        mostrar_mensaje("No hay cursos creados para matricular.", "error")
        return None, [], None

    cursos_seleccionados_ids = []
    opciones_map = {}
    table = Table(border_style="dim", width=80)
    table.add_column("Opción", style="bold yellow", width=8)
    table.add_column("ID Curso", style="dim", width=12)
    table.add_column("Nombre del Curso", min_width=20)
    table.add_column("Créditos", justify="right")

    for i, curso in enumerate(lista_cursos, 1):
        opcion_str = str(i)
        table.add_row(opcion_str, curso['id_curso'], curso['nombre_curso'], str(curso.get('creditos', 0)))
        opciones_map[opcion_str] = curso['id_curso']

    table.add_row("0", "LISTO", "Terminar selección de cursos", "")
    opciones_map["0"] = "LISTO"
    console.print(table)

    while True:
        opcion_elegida = Prompt.ask("[bold]Seleccione un curso (o '0' para terminar)[/bold]", default="0")

        if opcion_elegida == "0":
            break

        if opcion_elegida in opciones_map:
            curso_id_seleccionado = opciones_map[opcion_elegida]
            if curso_id_seleccionado in cursos_seleccionados_ids:
                mostrar_mensaje(f"Curso {curso_id_seleccionado} ya fue agregado.", "info")
            else:
                cursos_seleccionados_ids.append(curso_id_seleccionado)
                mostrar_mensaje(f"Curso {curso_id_seleccionado} agregado.", "exito")
        else:
            mostrar_mensaje(f"Opción '{opcion_elegida}' no válida.", "error")

    if not cursos_seleccionados_ids:
        mostrar_mensaje("No se seleccionó ningún curso. Matrícula cancelada.", "info")
        return None, [], None

    # 3. Pedir Periodo
    console.print(Panel(CANCEL_MESSAGE, border_style="dim", width=60))
    periodo = Prompt.ask("[bold]Periodo académico (Ej. 2025-01)[/bold]", default="2025-01").strip()
    if not periodo or periodo.lower() == CANCEL_KEYWORD:
        mostrar_mensaje("El periodo no puede estar vacío. Matrícula cancelada.", "error")
        return None, [], None

    return id_estudiante, cursos_seleccionados_ids, periodo