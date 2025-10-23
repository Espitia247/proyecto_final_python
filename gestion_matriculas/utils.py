import os
import platform

def limpiar_pantalla():
    """Limpia la consola, compatible con Windows, Mac y Linux."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")