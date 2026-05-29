"""
utilidades.py
=============
Funciones auxiliares de uso general en el proyecto.

Incluye:
- Limpieza de pantalla
- Impresión de banner y separadores
- Otras utilidades de presentación
"""

import os
import platform


def limpiar_pantalla() -> None:
    """Limpia la pantalla de la terminal de forma multiplataforma."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def imprimir_banner() -> None:
    """Imprime el banner de bienvenida del sistema."""
    print("""
╔══════════════════════════════════════════════════════╗
║        🧠 EXPLORADOR DE AFINIDADES MBTI 🧠           ║
║                                                      ║
║     Proyecto Final — Universidad                     ║
║     Sistema Exploratorio e Interactivo               ║
║                                                      ║
║  ⚠ USO EDUCATIVO Y EXPLORATORIO ÚNICAMENTE          ║
╚══════════════════════════════════════════════════════╝
    """)


def imprimir_separador(largo: int = 55) -> None:
    """
    Imprime una línea separadora horizontal.

    Parámetros:
        largo (int): Cantidad de caracteres de la línea.
    """
    print("─" * largo)


def formatear_porcentaje(valor: float, decimales: int = 1) -> str:
    """
    Formatea un número como porcentaje con símbolo.

    Parámetros:
        valor (float): Valor numérico.
        decimales (int): Decimales a mostrar.

    Retorna:
        str: Texto con formato (ej: '72.5%').
    """
    return f"{round(valor, decimales):.{decimales}f}%"
