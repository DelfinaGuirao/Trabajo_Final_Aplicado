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
        FileNotFoundError: Si el archivo no se encuentra.
        ValueError: Si el formato no es CSV válido.
    """

    try:
        df = pd.read_csv(ruta)

        print(f"Archivo leído: {ruta} | Filas: {len(df)} | Columnas: {len(df.columns)}")

        verificar_columnas(df)

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"No se ha encontrado el archivo: {ruta}")

    except Exception as e:
        raise ValueError(f"Error al cargar el CSV: {e}")


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
    filas_originales = len(df)  # cuenta cuántas filas tiene el dataset original

    columnas_importantes = [  # lista de columnas donde no puede haber valores nulos
     "Personality", "Introversion Score",
     "Sensing Score", "Thinking Score", "Judging Score"]

    mask = (  # crea una máscara booleana (True/False por fila)
     df[columnas_importantes[0]].notnull() &  # verifica que Personality no sea nulo
     df[columnas_importantes[1]].notnull() &  # verifica que Introversion Score no sea nulo
     df[columnas_importantes[2]].notnull() &  # verifica que Sensing Score no sea nulo
     df[columnas_importantes[3]].notnull() &  # verifica que Thinking Score no sea nulo
     df[columnas_importantes[4]].notnull())    # verifica que Judging Score no sea nulo.

    df_limpio = df.loc[mask].copy()  # filtra solo las filas válidas y crea una copia independiente

    df_limpio["Personality"] = (  # accede a la columna Personality
    df_limpio["Personality"].str.upper().str.strip())  # convierte a mayúsculas y elimina espacios.

    cols_numericas = [  # lista de columnas que deben convertirse a números
     "Introversion Score", "Sensing Score",
     "Thinking Score", "Judging Score"]

    for col in cols_numericas:  # recorre cada columna numérica
         df_limpio[col] = pd.to_numeric(df_limpio[col], errors="coerce")  # convierte a número, errores → NaN

    mask_numericos = (  # máscara para eliminar filas con valores NaN después de la conversión
     df_limpio["Introversion Score"].notnull() &
     df_limpio["Sensing Score"].notnull() &
     df_limpio["Thinking Score"].notnull() &
     df_limpio["Judging Score"].notnull())

    df_limpio = df_limpio.loc[mask_numericos].copy()  # aplica la máscara y filtra filas válidas

    filas_finales = len(df_limpio)  # cuenta cuántas filas quedaron después de limpiar

    eliminadas = filas_originales - filas_finales  # calcula cuántas filas se eliminaron

    print(f"Se eliminaron {eliminadas} filas con datos incompletos.")  # muestra cuántas filas se eliminaron

    print(f"Datos limpios: {filas_finales} registros disponibles.")  # muestra cuántas filas quedaron

    return df_limpio.reset_index(drop=True)  # devuelve el DataFrame limpio con índice reiniciado