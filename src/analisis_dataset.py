"""
analisis_dataset.py
===================
Módulo de análisis descriptivo y estadístico del dataset MBTI.

IMPORTANTE: El dataset es SINTÉTICO. Los análisis son exploratorios
y no representan poblaciones clínicas reales.

Responsabilidades:
- Calcular distribución de tipos MBTI en el dataset
- Identificar intereses predominantes por tipo
- Calcular promedios de scores por tipo
- Determinar rareza/frecuencia del perfil del usuario
- Comparar usuario contra promedio del grupo
"""

import pandas as pd


def calcular_distribucion_mbti(df: pd.DataFrame) -> pd.Series:
    """
    Calcula la distribución porcentual de tipos MBTI en el dataset.

    Parámetros:
        df (pd.DataFrame): Dataset MBTI limpio.

    Retorna:
        pd.Series: Porcentaje de cada tipo MBTI, ordenado de mayor a menor.
    """
    total = len(df)
    distribucion = df['Personality'].value_counts()
    distribucion_pct = (distribucion / total * 100).round(2)
    return distribucion_pct


def intereses_predominantes(df: pd.DataFrame, tipo: str) -> pd.Series:
    """
    Identifica los intereses más frecuentes en personas con el mismo tipo MBTI.

    Parámetros:
        df (pd.DataFrame): Dataset MBTI limpio.
        tipo (str): Tipo MBTI a analizar (ej: 'ENTP').

    Retorna:
        pd.Series: Frecuencia de intereses para ese tipo, ordenados.
    """
    if 'Interest' not in df.columns:
        return pd.Series(dtype='float64')
    
    subgrupo = df[df['Personality'] == tipo]
    
    if len(subgrupo) == 0:
        return pd.Series(dtype='float64')
    
    intereses = subgrupo['Interest'].value_counts()
    intereses_pct = (intereses / len(subgrupo) * 100).round(1)
    return intereses_pct


def calcular_promedios_por_tipo(datos_mbti: pd.DataFrame, tipo_mbti: str):
    """
    Calcula los puntajes promedio de las dimensiones MBTI
    para un tipo de personalidad específico.

    Parámetros:
        datos_mbti (pd.DataFrame):
            DataFrame que contiene la información del dataset.

        tipo_mbti (str):
            Tipo MBTI que se desea analizar.
            Ejemplos: "ENFP", "INTJ", "ENTP".

    Retorna:
        dict:
            Diccionario con los promedios de cada dimensión.

            Ejemplo:
            {
                "Introversion": 6.42,
                "Sensing": 4.81,
                "Thinking": 7.23,
                "Judging": 5.94
            }

        None:
            Si el tipo MBTI no existe en el dataset.
    """

    columnas_scores = {
        "Introversion Score": "Introversion",
        "Sensing Score": "Sensing",
        "Thinking Score": "Thinking",
        "Judging Score": "Judging"
    }

    personas_del_tipo = datos_mbti[
        datos_mbti["Personality"] == tipo_mbti
    ]

    if len(personas_del_tipo) == 0:
        return None

    promedios = {}

    for columna_original, nombre_dimension in columnas_scores.items():

        if columna_original in datos_mbti.columns:

            promedios[nombre_dimension] = round(
                personas_del_tipo[columna_original].mean(),
                2
            )

    return promedios

def calcular_rareza(datos_mbti, tipo_mbti):
    """
    Calcula la frecuencia de un tipo MBTI dentro del dataset.
    """

    total_personas = len(datos_mbti)

    distribucion = datos_mbti["Personality"].value_counts()

    cantidad_tipo = distribucion.get(tipo_mbti, 0)

    porcentaje = 0

    if total_personas > 0:
        porcentaje = round(
            (cantidad_tipo / total_personas) * 100,
            2
        )

    tipos_ordenados = distribucion.index.tolist()

    if tipo_mbti in tipos_ordenados:
        ranking = tipos_ordenados.index(tipo_mbti) + 1
    else:
        ranking = len(tipos_ordenados)

    return {
        "porcentaje": porcentaje,
        "cantidad": int(cantidad_tipo),
        "total": total_personas,
        "ranking": ranking,
        "total_tipos": len(tipos_ordenados)
    }

def comparar_usuario_vs_grupo(datos_mbti, tipo_mbti, scores_usuario):
    """
    Compara los scores del usuario con los promedios
    de las personas que comparten su mismo tipo MBTI.

    Parámetros:
        datos_mbti (pd.DataFrame):
            Dataset MBTI limpio.

        tipo_mbti (str):
            Tipo MBTI obtenido por el usuario.

        scores_usuario (dict):
            Puntajes obtenidos por el usuario en cada dimensión.

            Ejemplo:
            {
                "EI": 6,
                "SN": -2,
                "TF": 4,
                "JP": -8
            }

    Retorna:
        dict:
            Comparación entre el usuario y el promedio
            de su grupo MBTI.

        None:
            Si el tipo MBTI no existe en el dataset.
    """

    subgrupo = datos_mbti[
        datos_mbti["Personality"] == tipo_mbti
    ]

    if len(subgrupo) == 0:
        return None

    mapeo_dimensiones = {
        "EI": "Introversion Score",
        "SN": "Sensing Score",
        "TF": "Thinking Score",
        "JP": "Judging Score"
    }

    comparacion = {}

    for dimension, columna in mapeo_dimensiones.items():

        if columna not in datos_mbti.columns:
            continue

        score_usuario = scores_usuario.get(
            dimension,
            0
        )

        score_normalizado = round(
            ((score_usuario + 10) / 20) * 10,
            2
        )

        promedio_grupo = round(
            subgrupo[columna].mean(),
            2
        )

        desvio_grupo = round(
            subgrupo[columna].std(),
            2
        )

        comparacion[dimension] = {
            "usuario": score_normalizado,
            "promedio_grupo": promedio_grupo,
            "desvio_grupo": desvio_grupo,
            "n_grupo": len(subgrupo)
        }

    return comparacion
