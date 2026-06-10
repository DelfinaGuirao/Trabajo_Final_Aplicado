"""
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

# lista de columnas donde no puede haber valores nulos
    columnas_importantes = [ "Personality", "Introversion Score",
     "Sensing Score", "Thinking Score", "Judging Score"]

    # Elimina filas con valores nulos en columnas importantes
    df_limpio = df.dropna(subset=columnas_importantes).copy()
    #df.dropna(subset=columnas_importantes) nuevo DataFrame. se eliminaron las filas que tienen algún NaN en las columnas indicadas.
    #copy() crea una copia independiente al  DataFrame. 
 #sirve: cuando después hagas modificaciones, no modificás accidentalmente el DataFrame original (df). 
 #El .copy() es para trabajar con el nuevo DataFrame sin las filas eliminadas, de forma independiente al original.
 #eliminas filas con nulos en columnas importantes, creas una copia independiente
    
    
    df_limpio["Personality"] = ( df_limpio["Personality"] .str.upper().str.strip())
    
    # lista de columnas que deben convertirse a números
    cols_numericas = [  
     "Introversion Score", "Sensing Score",
     "Thinking Score", "Judging Score"]

    for col in cols_numericas:  # recorre cada columna numérica e intenta transofrmar a float. 
        try: 
            df_limpio[col] = df_limpio[col].astype(float)#astype(float) → convierte a número
        except ValueError: # si algún valor no se puede convertir a número (ej: texto),no rompe el programa y muestra un mensaje de error
            print(f"Error al convertir la columna {col}")

    df_limpio = df_limpio.dropna(subset=cols_numericas).copy() #Elimina filas que quedaron inválidas. 
#estás trabajando sobre df_limpio (que ya es una copia). astype(float) puede haber generado NaN si algo falló (o si ya había problemas)
#entonces: eliminas esas filas con NaN y haces otra copia independiente.
#estás haciendo una copia de un DataFrame que ya era copia, pero ahora filtrado otra vez.

    filas_finales = len(df_limpio) #Cuenta cuántas filas quedaron en el DataFrame después de la limpieza.

    print(f"Datos limpios: {filas_finales} registros disponibles.")

    return df_limpio.reset_index(drop=True)# .reset_index() Esto reinicia los índices del DataFrame.
#Toma el DataFrame limpio y volvé a numerar las filas desde cero.
#Después de eliminar filas (con dropna), los números de las filas quedan “saltados” entonces aca ordenas bien los indices. 
#drop=True : No guardes los números viejos como una columna nueva. 
#si fuese drop=False (o sin escribir nada). El índice viejo se convierte en columna:Sirve si te interesa guardar el índice original como dato. 


