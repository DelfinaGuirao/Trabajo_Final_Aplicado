"""
scoring_mbti.py
===============
Módulo que transforma respuestas en puntajes MBTI y calcula afinidades.

Lógica de scoring:
    Cada pregunta tiene una "dirección" (polo al que apunta una respuesta alta).
    La conversión de escala Likert (1-5) a puntos es:
        5 → +2  (Muy de acuerdo = mucho hacia el polo indicado)
        4 → +1  (De acuerdo)
        3 →  0  (Neutral)
        2 → -1  (En desacuerdo = hacia el polo opuesto)
        1 → -2  (Muy en desacuerdo = fuertemente hacia el polo opuesto)

Cálculo de afinidad porcentual:
    Se normaliza el puntaje neto de cada dimensión al rango [0%, 100%].
    Un 50% indica neutralidad perfecta entre ambos polos.
    Por encima del 50% hay afinidad al primer polo (E, S, T, J).
    Por debajo del 50% hay afinidad al segundo polo (I, N, F, P).
"""

from typing import List, Dict, Tuple


CONVERSION_LIKERT = {
    5: +2,
    4: +1,
    3:  0,
    2: -1,
    1: -2
}

POLOS_OPUESTOS = {
    'E': 'I', 'I': 'E',
    'S': 'N', 'N': 'S',
    'T': 'F', 'F': 'T',
    'J': 'P', 'P': 'J'
}

DIMENSIONES = ['EI', 'SN', 'TF', 'JP']


def calcular_scores(preguntas: List[Dict], respuestas: List[int]) -> Dict[str, int]:
    """
    Convierte las respuestas en puntajes brutos por dimensión.

    Cada puntaje positivo indica afinidad al primer polo (E, S, T, J).
    Cada puntaje negativo indica afinidad al segundo polo (I, N, F, P).

    Parámetros:
        preguntas (list): Lista de preguntas con dimension y direccion.
        respuestas (list): Lista de respuestas en escala 1-5.

    Retorna:
        dict: Puntajes netos por dimensión {'EI': x, 'SN': y, 'TF': z, 'JP': w}
    """
    scores = {'EI': 0, 'SN': 0, 'TF': 0, 'JP': 0}
    
    for pregunta, respuesta in zip(preguntas, respuestas):
        dimension = pregunta['dimension']
        direccion = pregunta['direccion']
        puntos = CONVERSION_LIKERT.get(respuesta, 0)
        
        primer_polo = dimension[0]
        if direccion == primer_polo:
            scores[dimension] += puntos
        else:
            scores[dimension] -= puntos
    
    return scores


def calcular_afinidades(scores: Dict[str, int]) -> Dict[str, float]:
    """
    Convierte los puntajes brutos a afinidades porcentuales.

    Asumiendo 5 preguntas por dimensión con valor máximo ±2 cada una,
    el rango de puntaje es [-10, +10].
    Se normaliza a [0%, 100%] donde 50% = neutral.

    Parámetros:
        scores (dict): Puntajes netos por dimensión.

    Retorna:
        dict: Afinidad porcentual para cada polo.
              Ejemplo: {'E': 72.5, 'I': 27.5, 'S': 40.0, 'N': 60.0, ...}
    """
    preguntas_por_dimension = 5
    max_puntos = preguntas_por_dimension * 2  # = 10

    afinidades = {}
    
    for dimension, score in scores.items():
        polo1 = dimension[0]
        polo2 = dimension[1]
        
        score_clamped = max(-max_puntos, min(max_puntos, score))
        
        afinidad_polo1 = round(((score_clamped + max_puntos) / (2 * max_puntos)) * 100, 1)
        afinidad_polo2 = round(100 - afinidad_polo1, 1)
        
        afinidades[polo1] = afinidad_polo1
        afinidades[polo2] = afinidad_polo2
    
    return afinidades


def determinar_tipo_mbti(scores: Dict[str, int]) -> str:
    """
    Determina el tipo MBTI de 4 letras con mayor afinidad.

    Regla: Para cada dimensión, se elige el polo con mayor afinidad.
    En caso de empate exacto (score=0), se elige el segundo polo
    por convención (I, N, F, P).

    Parámetros:
        scores (dict): Puntajes netos por dimensión.

    Retorna:
        str: Tipo MBTI de 4 letras (ej: 'ENTP', 'ISFJ', etc.)
    """
    tipo = ""
    
    for dimension in DIMENSIONES:
        score = scores[dimension]
        polo1 = dimension[0]
        polo2 = dimension[1]
        
        if score > 0:
            tipo += polo1
        else:
            tipo += polo2
    
    return tipo


def obtener_top_tipos(scores: Dict[str, int], afinidades: Dict[str, float], top_n: int = 5) -> List[Tuple[str, float]]:
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
        ) ** 0.25  # promedio geométrico
        
        resultados.append((tipo, round(afin_tipo, 1)))
    
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados[:top_n]
