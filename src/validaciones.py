"""
Módulo de validación de entradas del usuario.

Responsabilidades:
- Validar datos demográficos (edad, género)
- Validar respuestas del test (escala Likert 1-5)
- Proveer mensajes de error claros
- Usar try/except para manejo robusto de errores
"""


def validar_edad(): 
    """
    Valida que la edad sea un número entero entre 14 y 99.

    Returns:
        int: Edad válida, o 0 si la entrada no es válida.
    """
    while True:
        entrada = input("¿Cuántos años tenés? (14-99): ")
        try:
            edad = int(entrada.strip())
            if 14 <= edad <= 99:
                return edad
            else:
                print(" Edad fuera de rango. Intentalo de nuevo.")
        except ValueError:
            print(" Entrada inválida. Ingresá un número.")


def validar_genero (): 
    """
    Valida el género ingresado por el usuario.
    Acepta: M, F, Otro (insensible a mayúsculas).

    Returns:
        str: Género normalizado ('M', 'F', 'Otro') o 'No especificado'.
    """ 
    opciones_validas = {
        'm': 'M', 'masculino': 'M', 'hombre': 'M',
        'f': 'F', 'femenino': 'F', 'mujer': 'F',
        'otro': 'Otro', 'other': 'Otro', 'x': 'Otro'}

    while True:
        entrada = input("¿Con qué género te identificás? [M/F/Otro]: ")
        entrada_normalizada = entrada.strip().lower()

        if entrada_normalizada in opciones_validas:
            return opciones_validas[entrada_normalizada]

        print(" Opción no válida. Intentá de nuevo.")


def validar_respuesta():
    """
    Valida que la respuesta sea un número entero entre 1 y 5.
    Reintenta hasta obtener una respuesta válida.

    Returns:
        int: Respuesta válida entre 1 y 5.
    """ 
    while True: 
        entrada = input("Tu respuesta (1-5): ")

        try:
            valor = int(entrada.strip())

            if 1 <= valor <= 5:
                return valor
            else:
                print(" Por favor ingresá un número entre 1 y 5.")

        except ValueError:
            print(" Entrada inválida. Ingresá solo números del 1 al 5.")

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
