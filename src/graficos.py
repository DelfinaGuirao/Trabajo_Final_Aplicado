"""
Módulo que genera los gráficos del sistema MBTI.
    - Gráfico 1: Torta con las afinidades del usuario por letra
    - Gráfico 2: Barras con la distribución de personalidades en el dataset
"""
import matplotlib.pyplot as plt
from src.analisis_dataset import intereses_predominantes


def graficar_torta_usuario(afinidades):
    """
    Genera un gráfico de torta con el porcentaje de afinidad del usuario para cada letra de personalidad MBTI.

    Parámetros:
        afinidades (dict): Diccionario con porcentajes por polo.
                           Ejemplo: {'E': 70.0, 'I': 30.0, 'S': 45.0, ...}
    """

    # datos
    letras = list(afinidades.keys())         # ['E', 'I', 'S', 'N', 'T', 'F', 'J', 'P']
    porcentajes = list(afinidades.values())  # [70.0, 30.0, 45.0, ...]

    # gráfico
    plt.figure(figsize=(8, 8))

    plt.pie(
        porcentajes,        # tamaño de cada porción
        labels=letras,      # etiqueta de cada porción
        autopct='%1.1f%%',  # muestra el porcentaje con 1 decimal. Ej: 70.0%
        startangle=90       # empieza desde arriba
    )

    plt.title('Afinidad del usuario por letra MBTI', fontsize=14)

    plt.tight_layout()  #acomoda elementos del gráfico para que no se superpongan ni queden cortados
    plt.savefig('outputs/graficos/torta_usuario.png')  # guarda el gráfico como una img
    plt.show()


def graficar_barras_personalidades(df):
    """
    Genera un gráfico de barras horizontales con la distribución de los 16 tipos de personalidad MBTI en el dataset.

    Parámetros:
        df (DataFrame): Dataset completo ya cargado y limpio.
    """

    # datos
    # Cuenta cuántas veces aparece cada tipo y los ordena de mayor a menor
    conteo = df['Personality'].value_counts()

    tipos = conteo.index.tolist()        # ['INFP', 'ENTP', 'ISTJ', ...]
    cantidades = conteo.values.tolist()  # [120, 98, 87, ...]

    # gráfico
    plt.figure(figsize=(10, 8))

    plt.barh(tipos, cantidades, color='steelblue')  # barh = barras horizontales

    # etiqueta con el número exacto al lado de cada barra
    for i in range(len(tipos)):
        plt.text(
            cantidades[i] + 1,  # posición horizontal: un poco a la derecha de la barra
            i,                  # posición vertical: altura de la barra
            str(cantidades[i]), # texto a mostrar: la cantidad
            va='center',        # centrado verticalmente
            fontsize=10
        )

    plt.title('Distribución de personalidades MBTI en el dataset', fontsize=14)
    plt.xlabel('Cantidad de personas')
    plt.ylabel('Tipo de personalidad')

    plt.tight_layout()
    plt.savefig('outputs/graficos/barras_personalidades.png')  # guarda el gráfico
    plt.show()



def grafico_intereses(df, tipo_mbti): #piechart
    
    subgrupo= intereses_predominantes(df, tipo_mbti)
    
    intereses= subgrupo["Interest"].value_counts.head(6)  #cuenta los intereses y toma los 6 mas frecentes
    
    fig, ax = plt.subplots(figsize=(8, 8)) 
    
    fig.patch.set_facecolor('#F8F9FA') #fonfo gris clarito
    
    ax.pie( intereses.values, labels=intereses.index, autopct='%1.1f%%', colors=["#4D0B1A", "#1E9623", "#F2E646", "#7A428A", "#4C8FBF", "#BF4C9E"], startangle=90 )
    
    ax.set_title( f"Distribución de intereses — tipo {tipo_mbti}", fontsize=14, fontweight='bold', color='#2C3E50' ) 
   
    plt.tight_layout() 
    
    plt.savefig("outputs/graficos/pie_tipo_intereses.png", dpi=120) 
    
    plt.show()
    
    plt.close()
    
    