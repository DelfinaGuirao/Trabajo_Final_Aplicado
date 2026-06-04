"""
carga_datos.py
==============
Unidad responsable de leer, validar y limpiar el dataset MBTI.
Asume validez de la existencia de ciertas columnas

Responsabilidades:
- Leer el archivo CSV
- Verificar que las columnas esperadas estén presentes
- Limpiar datos nulos o con formato incorrecto
"""

import pandas as pd #importamos libreria pandas. 


def cargar_dataset(ruta): #parametro: string con el camino al archivo CSV, deuelve un Data frame. 
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
        filas = df.shape[0] #cuando usas df.shape devuele una tupla (fila,columna) entonces de la tupla, la fila sera la pocion 0
        columnas = df.shape[1]#(fila,columna) la columna sera la pocion 1
        print(f"Archivo leído: {ruta} | Cantidad de filas: {filas} | Cantidad de columnas: {columnas}")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"No se ha encontrado el archivo: {ruta}")

    except Exception as e:
        raise ValueError(f"Error al cargar el CSV: {e}")


def limpiar_datos(df):
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

#ME QUEDE ACAAAAAAAAA
    columnas_importantes = [
        "Personality",
        "Introversion Score",
        "Sensing Score",
        "Thinking Score",
        "Judging Score"]
    # Elimina filas con valores nulos en columnas importantes
    df_limpio = df.dropna(subset=columnas_importantes).copy()
    
    
    df_limpio["Personality"] = df_limpio["Personality"].str.upper().str.strip()
    
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