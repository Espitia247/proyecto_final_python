"""
Módulo de Utilidades (utils.py)

Contiene funciones auxiliares de propósito general para la aplicación,
como la limpieza de la pantalla de la consola.
"""
import os
import platform


def limpiar_pantalla():
    """
    Limpia la consola, compatible con Windows, Mac y Linux.

    Utiliza 'cls' para Windows y 'clear' para otros sistemas operativos.
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")