"""
carga_datos.py
==============
Unidad responsable de leer, validar y limpiar el dataset MBTI.

Responsabilidades:
- Leer el archivo CSV
- Verificar que las columnas esperadas estén presentes
- Limpiar datos nulos o con formato incorrecto
"""

import pandas as pd #importamos libreria pandas. 
import os # permite verificar si un archivo existe con os.path.exists


COLUMNAS_ESPERADAS = [
    "Age", "Gender", "Education", "Interest",
    "Introversion Score", "Sensing Score",
    "Thinking Score", "Judging Score", "Personality"] #columnas obligatorias que debe tener el dataset”


def cargar_dataset(ruta: str) -> pd.DataFrame: #parametro: string con el camino al archivo CSV, deuelve un Data frame. 
    """
    Carga el dataset desde un archivo CSV.

    Parameters:
        ruta (str): Ruta relativa al archivo CSV.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el formato no es CSV válido.
    """
    #VERIFICAMOS QUE EL ARCHVIO EXISTA. Si el archivo NO existe ->lanza un error. 
    if not os.path.exists(ruta):
        raise FileNotFoundError(f" No se ha encontrado el archivo: {ruta}")
    
    try:
        df = pd.read_csv(ruta) #convierte en dataframe. filas = observaciones, columnas = variables
        print(f"Archivo leído: {ruta} | Filas: {len(df)} | Columnas: {len(df.columns)}")
        verificar_columnas(df) 
        return df #Devolvemos el data set ya cargado. 
    except pd.errors.ParserError as e: #pd.errors es submódulo dentro de pandas y ParserError Error al interpretar (parsear) un archivo de texto.
        raise ValueError(f"Error al parsear el CSV: {e}")


def verificar_columnas(df: pd.DataFrame) -> None:
    """
    Verifica que el DataFrame contenga todas las columnas esperadas.

    Parameters:
        df (pd.DataFrame): DataFrame a verificar.

    Raises:
        ValueError: Si faltan columnas necesarias.
    """
    faltantes = []

    for col in COLUMNAS_ESPERADAS:
        if col not in df.columns:
            faltantes.append(col)

    if len(faltantes) > 0:
        raise ValueError(f"Columnas faltantes en el dataset: {faltantes}")

    print("Columnas verificadas correctamente.")


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame eliminando filas con valores nulos
    en columnas críticas y normalizando tipos de datos.

    Parameters:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: DataFrame limpio y listo para usar.
    """
    filas_originales = len(df) #uarda cuántas filas había antes de limpiar
    
    columnas_importantes = ["Personality", "Introversion Score", "Sensing Score",
                         "Thinking Score", "Judging Score"] #NO PUEDEN SER NULOS LOS VALORES. 
    df_limpio = df.dropna(subset=columnas_importantes).copy()
    #dropna dropna(subset=...) elimina filas donde falten esos datos. .copy()crea una copia independiente. 
    # eliminar nulos en columnas críticas. 
    
    df_limpio["Personality"] = df_limpio["Personality"].str.upper().str.strip() #" intj " → "INTJ"
    
    cols_numericas = ["Introversion Score", "Sensing Score",
                      "Thinking Score", "Judging Score"] #Define qué columnas deben ser números
    for col in cols_numericas:
        df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce') #ntenta convertir a número si no puede → pone NaN (errors='coerce'). 
    
    df_limpio = df_limpio.dropna(subset=cols_numericas) #Borra filas donde la conversión falló
    
    filas_finales = len(df_limpio)
    eliminadas = filas_originales - filas_finales
    
    if eliminadas > 0:
        print(f" Se eliminaron {eliminadas} filas con datos incompletos.")
    
    print(f" Datos limpios: {filas_finales} registros disponibles.")
    return df_limpio.reset_index(drop=True)#reinicia los índices del DataFrame. convierte el índice viejo en una columna nueva
# NO guardes el índice viejo como columna, bórralo