"""
carga_datos.py
==============
Módulo responsable de leer, validar y limpiar el dataset MBTI.

Responsabilidades:
- Leer el archivo CSV
- Verificar que las columnas esperadas estén presentes
- Limpiar datos nulos o con formato incorrecto
"""

import pandas as pd
import os


COLUMNAS_ESPERADAS = [
    "Age", "Gender", "Education", "Interest",
    "Introversion Score", "Sensing Score",
    "Thinking Score", "Judging Score", "Personality"
]


def cargar_dataset(ruta: str) -> pd.DataFrame:
    """
    Carga el dataset desde un archivo CSV.

    Parámetros:
        ruta (str): Ruta relativa al archivo CSV.

    Retorna:
        pd.DataFrame: DataFrame con los datos cargados.

    Lanza:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el formato no es CSV válido.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    
    try:
        df = pd.read_csv(ruta)
        print(f"  ✅ Archivo leído: {ruta} | Filas: {len(df)} | Columnas: {len(df.columns)}")
        verificar_columnas(df)
        return df
    except pd.errors.ParserError as e:
        raise ValueError(f"Error al parsear el CSV: {e}")


def verificar_columnas(df: pd.DataFrame) -> None:
    """
    Verifica que el DataFrame contenga todas las columnas esperadas.

    Parámetros:
        df (pd.DataFrame): DataFrame a verificar.

    Lanza:
        ValueError: Si faltan columnas necesarias.
    """
    faltantes = [col for col in COLUMNAS_ESPERADAS if col not in df.columns]
    if faltantes:
        raise ValueError(f"Columnas faltantes en el dataset: {faltantes}")
    print(f"  ✅ Columnas verificadas correctamente.")


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame eliminando filas con valores nulos
    en columnas críticas y normalizando tipos de datos.

    Parámetros:
        df (pd.DataFrame): DataFrame original.

    Retorna:
        pd.DataFrame: DataFrame limpio y listo para usar.
    """
    filas_originales = len(df)
    
    columnas_criticas = ["Personality", "Introversion Score", "Sensing Score",
                         "Thinking Score", "Judging Score"]
    df_limpio = df.dropna(subset=columnas_criticas).copy()
    
    df_limpio["Personality"] = df_limpio["Personality"].str.upper().str.strip()
    
    cols_numericas = ["Introversion Score", "Sensing Score",
                      "Thinking Score", "Judging Score"]
    for col in cols_numericas:
        df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce')
    
    df_limpio = df_limpio.dropna(subset=cols_numericas)
    
    filas_finales = len(df_limpio)
    eliminadas = filas_originales - filas_finales
    
    if eliminadas > 0:
        print(f"  ℹ️  Se eliminaron {eliminadas} filas con datos incompletos.")
    
    print(f"  ✅ Datos limpios: {filas_finales} registros disponibles.")
    return df_limpio.reset_index(drop=True)
