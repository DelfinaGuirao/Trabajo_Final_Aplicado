"""
Módulo que transforma respuestas en puntajes MBTI y calcula afinidades.

Lógica del archivo:
    Cada pregunta tiene una "dirección" (polo al que apunta una respuesta alta).
    La conversión de escala Likert (1-5) a puntos es:
        5 → +2  (Muy de acuerdo --> mucho hacia el polo indicado)
        4 → +1  (De acuerdo)
        3 →  0  (Neutral)
        2 → -1  (En desacuerdo --> hacia el polo opuesto)
        1 → -2  (Muy en desacuerdo -->  mucho hacia el polo opuesto)

Cálculo de afinidad porcentual:
    Se transforma el puntaje neto de cada dimension a una escala porcentual de 0% a 100%.
    - Un 50% significa que hay neutralidad  entre ambos polos.
    - Por encima del 50% hay afinidad al primer polo (E, S, T, J).
    - Por debajo del 50% hay afinidad al segundo polo (I, N, F, P).
"""


CONVERSION_LIKERT = {
    5: +2,
    4: +1,
    3:  0,
    2: -1,
    1: -2}

DIMENSIONES = ['EI', 'SN', 'TF', 'JP']


def calcular_scores(preguntas, respuestas):
    """
    Convierte las respuestas en puntajes brutos por dimensión.

    Cada puntaje positivo indica afinidad al primer polo (E, S, T, J).
    Cada puntaje negativo indica afinidad al segundo polo (I, N, F, P).

    Parámetros:
        preguntas (list): Lista de preguntas  con dimension y direccion. ('pregunta', 'direccion', 'dimension' son claves)
        respuestas (list): Lista de respuestas en escala 1-5.

    Retorna:
        puntajes (dict): Puntajes netos por dimensión {'EI': x, 'SN': y, 'TF': z, 'JP': w}
    """
    puntajes = {'EI': 0, 'SN': 0, 'TF': 0, 'JP': 0}
    
    #zip: empareja cada pregunta con su respuesta. 
    # si preguntas = [p1, p2] y respuestas = [3, 5], zip te da (p1,3) y (p2,5).

    for pregunta, respuesta in zip(preguntas, respuestas):
        dimension = pregunta['dimension']
        direccion = pregunta['direccion']
        puntos = CONVERSION_LIKERT.get(respuesta, 0) #usa la funcion para convertir rtas en putaje likert
        
        primer_polo = dimension[0]
        if direccion == primer_polo:
            puntajes[dimension] += puntos
        else:
            puntajes[dimension] -= puntos
    
    return puntajes



def calcular_afinidades(puntajes): 
    """"
    Convierte los puntajes por dimensión en porcentajes de afinidad.

    Normaliza cada puntaje del rango [-10, +10] al rango [0%, 100%].
    Un 50% indica neutralidad entre los dos polos de una dimensión.
    Por encima del 50% hay afinidad al primer polo (E, S, T, J).
    Por debajo del 50% hay afinidad al segundo polo (I, N, F, P).

    Parámetros:
        scores (dict): Puntajes netos por dimensión.
                       Ejemplo: {'EI': 6, 'SN': -3, 'TF': 0, 'JP': 4}

    Retorna:
        dict: Porcentaje de afinidad para cada polo.
              Ejemplo: {'E': 80.0, 'I': 20.0, 'S': 35.0, 'N': 65.0, ...}
    """

    afinidades = {}
    MAX = 10  # valor máximo posible de score

    for dimension, puntaje in puntajes.items():  #recorre claves y valores de score
        polo1 = dimension[0]  # ej: 'E'
        polo2 = dimension[1]  # ej: 'I'

        # Me aseguro que el score esté entre -10 y +10
        if puntaje > MAX:
            puntaje = MAX
        elif puntaje < -MAX:
            puntaje = -MAX

        # Convierto el score a porcentaje
        porcentaje = ((puntaje + MAX) / (2 * MAX)) * 100 #raris este calculo de porcentaje

        afinidades[polo1] = round(porcentaje, 1)
        afinidades[polo2] = round(100 - porcentaje, 1) #el porcentaje del polo dos es lo que le sobra al polo uno para llegar a 100 porq son complememtarios!!

    return afinidades



def determinar_tipo_mbti(puntajes):
    """
    Determina el tipo MBTI de 4 letras con mayor afinidad.

    Regla: Para cada dimensión, se elige el polo con mayor afinidad.
    En caso de empate exacto (puntaje=0), se elige el segundo polo
    por convención (I, N, F, P).

    Parámetros:
        puntajes (dict): Puntajes netos por dimensión.

    Retorna:
        str: Tipo MBTI de 4 letras (ej: 'ENTP', 'ISFJ', etc.)
    """
    tipo = ""
    
    for dimension in DIMENSIONES:   #DIMENSIONES  es una lista "global", esta por fuer de la funcion al ppio del codifo
        puntaje = puntajes[dimension]  #dimension es un string 
        polo1 = dimension[0]
        polo2 = dimension[1]
        
        if puntaje > 0:
            tipo += polo1
        else:
            tipo += polo2
    
    return tipo


def obtener_top_tipos(puntajes, afinidades, top_n = 5):
    """
    Calcula los tipos MBTI más afines al usuario, con sus porcentajes.

    El porcentaje total de afinidad a un tipo es el promedio geométrico
    de las afinidades de cada uno de sus 4 polos.

    Parámetros:
        scores (dict): Puntajes brutos por dimensión.
        afinidades (dict): Afinidades porcentuales por polo.
        top_n (int): Cantidad de tipos a retornar.

    Retorna:
        list[tuple]: Lista de (tipo, porcentaje_afinidad), ordenada de mayor a menor.
    """
    todos_los_tipos = [
        'ISTJ','ISFJ','INFJ','INTJ',
        'ISTP','ISFP','INFP','INTP',
        'ESTP','ESFP','ENFP','ENTP',
        'ESTJ','ESFJ','ENFJ','ENTJ'
    ]
    
    resultados = []
    
    for tipo in todos_los_tipos:
        afin_tipo = (
            afinidades[tipo[0]] *
            afinidades[tipo[1]] *
            afinidades[tipo[2]] *
            afinidades[tipo[3]]
        ) ** 0.25  #sacopromedio geometrico (porque geometrico?? porque tiene mas en cuenta valores por separado. ej en doc)
        
        resultados.append((tipo, round(afin_tipo, 1))) # round rondea a decimales
    
   
    def obtener_porcentaje(tupla):
            return tupla[1]
    #ordena (con .sort() de mayor a menor (reverse = True) el porcentaje de cada tupla.
    resultados.sort(key=obtener_porcentaje, reverse=True)  

# Devolver solo los primeros top_n (5) resultados
    return resultados[:top_n] 

