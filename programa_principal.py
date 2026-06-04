"""
MBTI Exploratorio - Proyecto Final
====================================
Sistema interactivo de exploración de afinidades MBTI.
USO EDUCATIVO Y EXPLORATORIO ÚNICAMENTE.
"""

import os
import sys
from src.carga_datos import cargar_dataset, limpiar_datos
from src.preguntas import obtener_preguntas
from src.validaciones import validar_edad, validar_genero, validar_respuesta
from src.metricas import calcular_scores, calcular_afinidades, determinar_tipo_mbti
from src.analisis_dataset import (
    calcular_distribucion_mbti,
    intereses_predominantes,
    calcular_promedios_por_tipo,
    calcular_rareza,
    comparar_usuario_vs_grupo
)
from src.visualizaciones import (
    graficar_distribucion_mbti,
    graficar_intereses_por_tipo,
    graficar_usuario_vs_promedio,
    graficar_histograma_scores,
    graficar_radar_usuario
)
from src.resultados import mostrar_resultados_finales, guardar_usuario
from src.utilidades import imprimir_banner, imprimir_separador


def main():
    """Función principal que orquesta el flujo completo del sistema."""
    
    
    imprimir_banner()
    
    # --- DISCLAIMER ÉTICO ---
    print("\n⚠️  AVISO IMPORTANTE")
    imprimir_separador()
    print("""Este sistema NO constituye una herramienta psicológica clínica ni diagnóstica.
Los resultados representan AFINIDADES EXPLORATORIAS basadas en un dataset sintético.
El MBTI es un marco de referencia popular, no un instrumento clínico validado.
Usá este sistema como una experiencia lúdica y reflexiva, no como un diagnóstico.\n""")
    input("Presioná ENTER para continuar...")
    
    # --- CARGA DEL DATASET ---
    print("\n📊 Cargando dataset...")
    try:
        df_raw = cargar_dataset("data/dataset_mbti.csv")
        df = limpiar_datos(df_raw)
        print(f"✅ Dataset cargado: {len(df)} registros disponibles para comparación.")
    except FileNotFoundError:
        print("⚠️  Dataset no encontrado. Se usarán datos simulados para comparación.")
        df = None
    except Exception as e:
        print(f"⚠️  Error al cargar dataset: {e}. Continuando sin datos comparativos.")
        df = None
    
    imprimir_separador()
    
    # --- DATOS DEMOGRÁFICOS ---
    print("\n👤 DATOS DEMOGRÁFICOS (opcionales, para comparación poblacional)")
    
    nombre = input("¿Cuál es tu nombre o apodo? ").strip() or "Explorador/a"
    edad = validar_edad(input("¿Cuántos años tenés? (14-99): "))
    genero = validar_genero(input("¿Con qué género te identificás? [M/F/Otro]: "))
    
    imprimir_separador()
    
    # --- TEST DE PREGUNTAS ---
    print(f"\n🎯 ¡Hola, {nombre}! Comenzamos con el test exploratorio.")
    print("Vas a responder preguntas usando esta escala:")
    print("  1 = Muy en desacuerdo")
    print("  2 = En desacuerdo")
    print("  3 = Neutral")
    print("  4 = De acuerdo")
    print("  5 = Muy de acuerdo\n")
    input("Presioná ENTER para empezar...")
    
    preguntas = obtener_preguntas()
    respuestas = []
    
    for i, pregunta in enumerate(preguntas, 1):
       
        print(f"\nPregunta {i} de {len(preguntas)}")
        imprimir_separador(40)
        print(f"\n{pregunta['pregunta']}\n")
        print("  [1] Muy en desacuerdo")
        print("  [2] En desacuerdo")
        print("  [3] Neutral")
        print("  [4] De acuerdo")
        print("  [5] Muy de acuerdo\n")
        
        resp = validar_respuesta(input("Tu respuesta (1-5): "))
        respuestas.append(resp)
    
    # --- CÁLCULO DE SCORES ---
    print("\n⚙️  Calculando tus afinidades...")
    scores = calcular_scores(preguntas, respuestas)
    afinidades = calcular_afinidades(scores)
    tipo_predominante = determinar_tipo_mbti(scores)
    
    # --- ANÁLISIS COMPARATIVO ---
    distribucion = None
    intereses = None
    promedios = None
    rareza = None
    comparacion = None
    
    if df is not None:
        print("📈 Analizando comparación con dataset...")
    
    try:

        distribucion = calcular_distribucion_mbti(df)

        intereses = intereses_predominantes(
            df,
            tipo_predominante
        )

        promedios = calcular_promedios_por_tipo(
            df,
            tipo_predominante
        )

        rareza = calcular_rareza(
            df,
            tipo_predominante
        )

        comparacion = comparar_usuario_vs_grupo(
            df,
            tipo_predominante,
            scores
        )

    except KeyError as error:

        print(
            f"⚠️ Error en el análisis del dataset: {error}"
        )
    
    # --- VISUALIZACIONES ---
    print("🎨 Generando visualizaciones...")
    os.makedirs("outputs/graficos", exist_ok=True)
    
    if df is not None and distribucion is not None:
        graficar_distribucion_mbti(distribucion, tipo_predominante)
        graficar_intereses_por_tipo(df, tipo_predominante)
        graficar_usuario_vs_promedio(comparacion, tipo_predominante)
    
    graficar_histograma_scores(scores, afinidades)
    graficar_radar_usuario(afinidades)
    
    # --- RESULTADOS FINALES ---
   
    mostrar_resultados_finales(
        nombre=nombre,
        tipo=tipo_predominante,
        afinidades=afinidades,
        scores=scores,
        distribucion=distribucion,
        intereses=intereses,
        rareza=rareza,
        comparacion=comparacion
    )
    
    # --- GUARDADO OPCIONAL ---
    imprimir_separador()
    guardar = input("\n¿Querés guardar tus resultados? [s/n]: ").strip().lower()
    if guardar == 's':
        guardar_usuario(nombre, edad, genero, tipo_predominante, afinidades, scores)
        print("✅ Resultados guardados en data/usuarios.csv")
    
    print("\n¡Gracias por explorar tus afinidades MBTI! 🌟")
    print("Recordá: esto es una exploración lúdica, ¡no un diagnóstico!")
    imprimir_separador()


if __name__ == "__main__":
    main()
