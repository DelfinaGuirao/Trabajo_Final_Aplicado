"""
visualizaciones.py
==================
Módulo de visualizaciones con matplotlib.

Gráficos generados:
    1. Distribución MBTI en el dataset (barras)
    2. Intereses predominantes por tipo (barras horizontales)
    3. Usuario vs Promedio del grupo (barras agrupadas)
    4. Histograma / barras de afinidades por polo (barras)
    5. Radar chart de afinidades del usuario

Todos los gráficos se guardan en outputs/graficos/.
"""

import matplotlib
matplotlib.use('Agg')  # para entornos sin pantalla

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from typing import Dict, Optional

OUTPUT_DIR = "outputs/graficos"


def _preparar_figura(titulo: str, figsize=(12, 6)):
    """Crea y configura una figura matplotlib con estilo consistente."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#FFFFFF')
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15, color='#2C3E50')
    return fig, ax


def graficar_distribucion_mbti(distribucion, tipo_usuario: str) -> None:
    """
    Grafica la distribución porcentual de tipos MBTI en el dataset.
    Resalta el tipo del usuario.

    Parámetros:
        distribucion (pd.Series): Porcentaje de cada tipo MBTI.
        tipo_usuario (str): Tipo MBTI del usuario para resaltar.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    fig, ax = _preparar_figura(
        "Distribución de tipos MBTI en el dataset\n"
        "(Datos sintéticos — solo fines exploratorios)",
        figsize=(14, 6)
    )
    
    tipos = distribucion.index.tolist()
    valores = distribucion.values.tolist()
    colores = ['#E74C3C' if t == tipo_usuario else '#3498DB' for t in tipos]
    
    barras = ax.bar(tipos, valores, color=colores, edgecolor='white', linewidth=0.5)
    
    for barra, val in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width() / 2., barra.get_height() + 0.1,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=8, color='#555')
    
    ax.set_xlabel("Tipo MBTI", fontsize=11, color='#555')
    ax.set_ylabel("Porcentaje (%)", fontsize=11, color='#555')
    ax.tick_params(axis='x', rotation=45)
    
    parche_usuario = mpatches.Patch(color='#E74C3C', label=f'Tu tipo: {tipo_usuario}')
    parche_otros = mpatches.Patch(color='#3498DB', label='Otros tipos')
    ax.legend(handles=[parche_usuario, parche_otros], fontsize=10)
    
    ax.text(0.5, -0.20,
            "⚠ Dataset sintético — no representa población clínica real",
            ha='center', transform=ax.transAxes,
            fontsize=9, color='#888', style='italic')
    
    plt.tight_layout()
    ruta = os.path.join(OUTPUT_DIR, "1_distribucion_mbti.png")
    plt.savefig(ruta, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  💾 Gráfico guardado: {ruta}")


def graficar_intereses_por_tipo(df, tipo_usuario: str) -> None:
    """
    Grafica los intereses predominantes para el tipo MBTI del usuario.

    Parámetros:
        df (pd.DataFrame): Dataset MBTI limpio.
        tipo_usuario (str): Tipo MBTI del usuario.
    """
    if 'Interest' not in df.columns:
        print("  ⚠️  Columna 'Interest' no disponible.")
        return
    
    subgrupo = df[df['Personality'] == tipo_usuario]
    if len(subgrupo) == 0:
        return
    
    intereses = subgrupo['Interest'].value_counts().head(8)
    
    fig, ax = _preparar_figura(
        f"Intereses frecuentes en personas con tipo {tipo_usuario}\n"
        f"(Basado en {len(subgrupo)} registros del dataset sintético)",
        figsize=(10, 6)
    )
    
    colores = plt.cm.viridis(np.linspace(0.2, 0.8, len(intereses)))
    ax.barh(intereses.index, intereses.values, color=colores, edgecolor='white')
    
    for i, val in enumerate(intereses.values):
        ax.text(val + 0.5, i, str(val), va='center', fontsize=9, color='#555')
    
    ax.set_xlabel("Cantidad de personas", fontsize=11, color='#555')
    ax.set_ylabel("Interés", fontsize=11, color='#555')
    ax.invert_yaxis()
    
    plt.tight_layout()
    ruta = os.path.join(OUTPUT_DIR, "2_intereses_por_tipo.png")
    plt.savefig(ruta, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  💾 Gráfico guardado: {ruta}")


def graficar_usuario_vs_promedio(comparacion: Optional[Dict], tipo_usuario: str) -> None:
    """
    Grafica el score del usuario comparado con el promedio de su grupo.

    Parámetros:
        comparacion (dict): Datos de comparación por dimensión.
        tipo_usuario (str): Tipo MBTI del usuario.
    """
    if not comparacion:
        print("  ⚠️  No hay datos de comparación disponibles.")
        return
    
    dimensiones = list(comparacion.keys())
    valores_usuario = [comparacion[d]['usuario'] for d in dimensiones]
    valores_grupo = [comparacion[d]['promedio_grupo'] for d in dimensiones]
    
    x = np.arange(len(dimensiones))
    ancho = 0.35
    
    fig, ax = _preparar_figura(
        f"Comparación: tus scores vs promedio del grupo {tipo_usuario}\n"
        "(Escala normalizada 0-10 — solo referencia exploratoria)",
        figsize=(10, 6)
    )
    
    barras1 = ax.bar(x - ancho/2, valores_usuario, ancho,
                     label='Tu perfil', color='#E74C3C', alpha=0.85, edgecolor='white')
    barras2 = ax.bar(x + ancho/2, valores_grupo, ancho,
                     label=f'Promedio {tipo_usuario}', color='#3498DB', alpha=0.85, edgecolor='white')
    
    for barra in barras1:
        ax.text(barra.get_x() + barra.get_width()/2., barra.get_height() + 0.1,
                f'{barra.get_height():.1f}', ha='center', va='bottom', fontsize=9)
    for barra in barras2:
        ax.text(barra.get_x() + barra.get_width()/2., barra.get_height() + 0.1,
                f'{barra.get_height():.1f}', ha='center', va='bottom', fontsize=9)
    
    ax.set_xticks(x)
    ax.set_xticklabels(dimensiones, fontsize=11)
    ax.set_ylabel("Score normalizado (0-10)", fontsize=11, color='#555')
    ax.set_ylim(0, 12)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    ruta = os.path.join(OUTPUT_DIR, "3_usuario_vs_promedio.png")
    plt.savefig(ruta, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  💾 Gráfico guardado: {ruta}")


def graficar_histograma_scores(scores: Dict[str, int], afinidades: Dict[str, float]) -> None:
    """
    Grafica las afinidades porcentuales del usuario por polo MBTI.

    Parámetros:
        scores (dict): Puntajes brutos por dimensión.
        afinidades (dict): Afinidades porcentuales por polo.
    """
    fig, ax = _preparar_figura(
        "Tus afinidades MBTI por polo\n"
        "(Porcentaje de afinidad — 50% = completamente neutral)",
        figsize=(12, 6)
    )
    
    pares = [('E', 'I'), ('S', 'N'), ('T', 'F'), ('J', 'P')]
    colores_positivos = ['#2ECC71', '#3498DB', '#9B59B6', '#E67E22']
    colores_neutros = ['#95A5A6', '#BDC3C7', '#A8A8A8', '#C0C0C0']
    
    x_labels = []
    y_valores = []
    colores = []
    
    for i, (polo1, polo2) in enumerate(pares):
        af1 = afinidades.get(polo1, 50)
        af2 = afinidades.get(polo2, 50)
        
        c1 = colores_positivos[i] if af1 >= 50 else colores_neutros[i]
        c2 = colores_positivos[i] if af2 >= 50 else colores_neutros[i]
        
        x_labels.extend([polo1, polo2])
        y_valores.extend([af1, af2])
        colores.extend([c1, c2])
    
    barras = ax.bar(x_labels, y_valores, color=colores, edgecolor='white', linewidth=0.8, width=0.6)
    
    ax.axhline(y=50, color='#E74C3C', linestyle='--', linewidth=1.5,
               alpha=0.7, label='Línea de neutralidad (50%)')
    
    for barra, val in zip(barras, y_valores):
        ax.text(barra.get_x() + barra.get_width()/2., barra.get_height() + 0.5,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for i, pos in enumerate([1.5, 5.5, 9.5, 13.5]):
        if i < 3:
            ax.axvline(x=pos, color='#CCC', linestyle='-', linewidth=0.5, alpha=0.5)
    
    ax.set_ylabel("Afinidad (%)", fontsize=11, color='#555')
    ax.set_ylim(0, 115)
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    ruta = os.path.join(OUTPUT_DIR, "4_afinidades_por_polo.png")
    plt.savefig(ruta, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  💾 Gráfico guardado: {ruta}")


def graficar_radar_usuario(afinidades: Dict[str, float]) -> None:
    """
    Genera un gráfico de radar (spider chart) con las afinidades del usuario.

    Parámetros:
        afinidades (dict): Afinidades porcentuales por polo.
    """
    polos = ['E', 'S', 'T', 'J', 'I', 'N', 'F', 'P']
    valores = [afinidades.get(p, 50) for p in polos]
    
    n = len(polos)
    angulos = [i * 2 * np.pi / n for i in range(n)]
    angulos += angulos[:1]
    valores += valores[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#FFFFFF')
    
    ax.plot(angulos, valores, 'o-', linewidth=2, color='#3498DB', markersize=8)
    ax.fill(angulos, valores, alpha=0.25, color='#3498DB')
    
    ax.plot(angulos, [50] * (n + 1), '--', linewidth=1,
            color='#E74C3C', alpha=0.5, label='Neutralidad (50%)')
    
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(polos, fontsize=13, fontweight='bold', color='#2C3E50')
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=8, color='#888')
    ax.set_title("Radar de afinidades MBTI\n(Exploración personal)", 
                 fontsize=13, fontweight='bold', color='#2C3E50', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
    
    plt.tight_layout()
    ruta = os.path.join(OUTPUT_DIR, "5_radar_afinidades.png")
    plt.savefig(ruta, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  💾 Gráfico guardado: {ruta}")
