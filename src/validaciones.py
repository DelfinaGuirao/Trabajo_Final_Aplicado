"""
validaciones.py
===============
Módulo de validación de entradas del usuario.

Responsabilidades:
- Validar datos demográficos (edad, género)
- Validar respuestas del test (escala Likert 1-5)
- Proveer mensajes de error claros
- Usar try/except para manejo robusto de errores
"""


def validar_edad(entrada: str) -> int:
    """
    Valida que la edad sea un número entero entre 14 y 99.

    Parameters:
        entrada (str): Texto ingresado por el usuario.

    Returns:
        int: Edad válida, o 0 si la entrada no es válida.
    """
    try:
        edad = int(entrada.strip())
        if 14 <= edad <= 99:
            return edad
        else:
            print(" Edad fuera de rango. Se omitirá este dato.")
            return 0
    except ValueError:
        print(" Entrada inválida para edad. Se omitirá este dato.")
        return 0


def validar_genero(entrada: str) -> str:
    """
    Valida el género ingresado por el usuario.
    Acepta: M, F, Otro (insensible a mayúsculas).

    Parameters:
        entrada (str): Texto ingresado por el usuario.

    Returns:
        str: Género normalizado ('M', 'F', 'Otro') o 'No especificado'.
    """
    opciones_validas = {
        'm': 'M', 'masculino': 'M', 'hombre': 'M',
        'f': 'F', 'femenino': 'F', 'mujer': 'F',
        'otro': 'Otro', 'other': 'Otro', 'x': 'Otro'}
    
    entrada_normalizada = entrada.strip().lower()
    
    if entrada_normalizada in opciones_validas: #verifica si entrada es válida
        return opciones_validas[entrada_normalizada]
    
    print(" Opción no reconocida. Se registrará como 'No especificado'.")
    return "No especificado"


def validar_respuesta(entrada: str) -> int:
    """
    Valida que la respuesta sea un número entero entre 1 y 5.
    Reintenta hasta obtener una respuesta válida.

    Parameters:
        entrada (str): Texto ingresado por el usuario.

    Returns:
        int: Respuesta válida entre 1 y 5.
    """
    while True: #bucle infinito hasta obtener respuesta válida.
        try:
            valor = int(entrada.strip())
            if 1 <= valor <= 5:
                return valor
            else:
                print(" Por favor ingresá un número entre 1 y 5.")
        except ValueError:
            print(" Entrada inválida. Ingresá solo un número del 1 al 5.")
        
        entrada = input("  Tu respuesta (1-5): ")


def validar_rango(valor: float, minimo: float, maximo: float, nombre: str = "valor") -> float:
    """
    Verifica que un valor numérico esté dentro de un rango válido.

    Parameters:
        valor (float): Valor a validar.
        minimo (float): Límite inferior permitido.
        maximo (float): Límite superior permitido.
        nombre (str): Nombre descriptivo del valor (para mensajes de error).

    Returns:
        float: El valor si es válido.

    Raises:
        ValueError: Si el valor está fuera del rango.
    """
    if not (minimo <= valor <= maximo):
        raise ValueError(
            f"El {nombre} ({valor}) está fuera del rango permitido [{minimo}, {maximo}]."
        )
    return valor
