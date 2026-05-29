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
import numpy as np
from typing import Dict, List, Tuple, Optional


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


def calcular_promedios_por_tipo(df: pd.DataFrame, tipo: str) -> Optional[Dict[str, float]]:
    """
    Calcula el promedio de cada score dimensional para el tipo indicado.

    Parámetros:
        df (pd.DataFrame): Dataset MBTI limpio.
        tipo (str): Tipo MBTI a analizar.

    Retorna:
        dict: Promedios de scores {'Introversion': x, 'Sensing': y, ...}
              o None si el tipo no existe en el dataset.
    """
    columnas_scores = {
        'Introversion Score': 'Introversion',
        'Sensing Score': 'Sensing',
        'Thinking Score': 'Thinking',
        'Judging Score': 'Judging'
    }
    
    subgrupo = df[df['Personality'] == tipo]
    
    if len(subgrupo) == 0:
        return None
    
    promedios = {}
    for col_original, nombre in columnas_scores.items():
        if col_original in df.columns:
            promedios[nombre] = round(subgrupo[col_original].mean(), 2)
    
    return promedios


def calcular_rareza(df: pd.DataFrame, tipo: str) -> Dict[str, object]:
    """
    Calcula qué tan frecuente o raro es el tipo MBTI en el dataset.

    Parámetros:
        df (pd.DataFrame): Dataset MBTI limpio.
        tipo (str): Tipo MBTI a analizar.

    Retorna:
        dict: Información de rareza con claves:
              'porcentaje', 'cantidad', 'total', 'ranking', 'total_tipos'
    """
    total = len(df)
    distribucion = df['Personality'].value_counts()
    
    cantidad = distribucion.get(tipo, 0)
    porcentaje = round((cantidad / total) * 100, 2) if total > 0 else 0
    
    tipos_ordenados = distribucion.index.tolist()
    ranking = tipos_ordenados.index(tipo) + 1 if tipo in tipos_ordenados else len(tipos_ordenados)
    
    return {
        'porcentaje': porcentaje,
        'cantidad': int(cantidad),
        'total': total,
        'ranking': ranking,
        'total_tipos': len(tipos_ordenados)
    }


def comparar_usuario_vs_grupo(
    df: pd.DataFrame,
    tipo: str,
    scores_usuario: Dict[str, int]
) -> Optional[Dict[str, Dict[str, float]]]:
    """
    Compara los scores del usuario con el promedio de su grupo en el dataset.

    El dataset usa una escala diferente (0-10 aprox), por lo que
    los scores del usuario (escala -10 a +10) se normalizan a [0, 10].

    Parámetros:
        df (pd.DataFrame): Dataset MBTI limpio.
        tipo (str): Tipo MBTI del usuario.
        scores_usuario (dict): Scores brutos del usuario por dimensión.

    Retorna:
        dict: Comparación usuario vs grupo con claves por dimensión.
    """
    subgrupo = df[df['Personality'] == tipo]
    
    if len(subgrupo) == 0:
        return None
    
    mapeo_dimensiones = {
        'EI': 'Introversion Score',
        'SN': 'Sensing Score',
        'TF': 'Thinking Score',
        'JP': 'Judging Score'
    }
    
    comparacion = {}
    
    for dim, col in mapeo_dimensiones.items():
        if col not in df.columns:
            continue
        
        score_usuario_raw = scores_usuario.get(dim, 0)
        score_normalizado = round(((score_usuario_raw + 10) / 20) * 10, 2)
        
        promedio_grupo = round(subgrupo[col].mean(), 2)
        desvio_grupo = round(subgrupo[col].std(), 2)
        
        comparacion[dim] = {
            'usuario': score_normalizado,
            'promedio_grupo': promedio_grupo,
            'desvio_grupo': desvio_grupo,
            'n_grupo': len(subgrupo)
        }
    
    return comparacion
