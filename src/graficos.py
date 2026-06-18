"""
Módulo que genera los gráficos del sistema MBTI.
    - Gráfico 1: Torta con las afinidades del usuario por letra
    - Grafico 2: Barras con la distribucion de female y male en el dataset
    - Gráfico 2: Torta de los 6 intereses predominantes para el tipo MBTI
"""
import matplotlib.pyplot as plt
from src.analisis_dataset import intereses_predominantes, calcular_distribucion_mbti, calcular_genero_por_tipo



def graficar_torta_usuario(afinidades, nombre):
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

    plt.title('Afinidad para {nombre} por cada letra de su MBTI')

    plt.tight_layout()  #acomoda elementos del gráfico para que no se superpongan ni queden cortados
    plt.savefig("outputs/graficos/graficar_torta_usuario.png")

    plt.show()


def graficar_genero_por_tipo(genero_pct, tipo_usuario, nombre):
   
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#F8F9FA')

    ax.bar(
        genero_pct.index,
        genero_pct.values,
        color=['#3498DB', '#E74C3C']
    )

    ax.set_title(
        f"Grafico para {nombre} con la distribucion de generos con un MBTI del tipo {tipo_usuario}",
        fontsize=14,
        fontweight='bold',
        color='#2C3E50'
    )

    ax.set_ylabel("Porcentaje (%)")

    # Mostrar el valor encima de cada barra
    for i, valor in enumerate(genero_pct.values):
        ax.text(
            i,
            valor + 1,
            f"{valor:.1f}%",
            ha='center',
            fontweight='bold'
        )

    plt.tight_layout()
    plt.savefig("outputs/graficos/graficar_genero_por_tipo.png")
    plt.show()


def grafico_intereses(df, tipo_mbti, nombre):
    
    intereses = intereses_predominantes(df, tipo_mbti)

    intereses = intereses.head(6)

    fig, ax = plt.subplots(figsize=(8, 8))

    fig.patch.set_facecolor('#F8F9FA')

    ax.pie(
        intereses.values,
        labels=intereses.index,
        autopct='%1.1f%%',
        startangle=90
    )

    ax.set_title(
        f"6 intereses predominantes de {nombre} del tipo {tipo_mbti}",
        fontsize=14,
        fontweight='bold'
    )

    
    plt.tight_layout()
    plt.savefig("outputs/graficos/grafico_intereses.png")

    plt.show()