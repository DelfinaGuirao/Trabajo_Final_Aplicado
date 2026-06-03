"""
utilidades.py
=============
Funciones auxiliares de uso general en el proyecto.

Incluye:
- Limpieza de pantalla
- Impresión de banner y separadores
- Otras utilidades de presentación
"""




def imprimir_banner(): 
    """Imprime el banner de bienvenida del sistema."""
    print(""" BIENVENIDOS AL EXPLORADOR DE PERSONALIDADES DE MBTI. Es de uso\
          educativo y exploratorio unicamente. Presentado por estudientes de la UdeSa\
    """)


def imprimir_separador(largo: int = 55): #imprime una línea de guiones en la consola para separar visualmente secciones de texto.
    """
    Imprime una línea separadora horizontal.

    Parámetros:
        largo (int): Cantidad de caracteres de la línea.
    """
    print("─" * largo) # Repetir __ la cantidad de veces que indique el largo


def formatear_porcentaje(valor, decimales: int = 1):
    #recibe un número y lo convierte en texto con el símbolo %
    """
    Formatea un número como porcentaje con símbolo.

    Parámetros:
        valor (float): Valor numérico.
        decimales (int): Decimales a mostrar.

    Retorna:
        str: Texto con formato (ej: '72.5%').
    """
    numero= round(valor, decimales)
    return f"{numero:.{decimales}f}%"

#round() es una función que viene incluida en Python y sirve para redondear números.
