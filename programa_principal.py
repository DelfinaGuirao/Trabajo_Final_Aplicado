"""
Sistema interactivo de exploración de afinidades MBTI.
USO EDUCATIVO Y EXPLORATORIO ÚNICAMENTE.
"""


from src.carga_datos import cargar_dataset, limpiar_datos
from src.preguntas import obtener_preguntas
from src.validaciones import validar_edad, validar_genero, validar_respuesta
from src.metricas import calcular_scores, calcular_afinidades, determinar_tipo_mbti
from src.analisis_dataset import (
    calcular_distribucion_mbti,
    intereses_predominantes,
    calcular_promedios_por_tipo,
    calcular_rareza,
    comparar_usuario_vs_grupo,
    calcular_genero_por_tipo
)

from src.resultados import mostrar_resultados_finales
from src.utilidades import imprimir_banner, imprimir_separador
from src.graficos import graficar_torta_usuario, graficar_genero_por_tipo, grafico_intereses


def main():
    """Función principal que orquesta el flujo completo del sistema."""
   
    imprimir_banner()
    
    # --- DISCLAIMER ÉTICO ---
    print("\n AVISO IMPORTANTE")
    imprimir_separador()
    print("""Este sistema NO constituye una herramienta psicológica clínica ni diagnóstica. 
Los resultados representan AFINIDADES EXPLORATORIAS basadas en un dataset sintético.
El MBTI es un marco de referencia popular, no un instrumento clínico validado.
Usá este sistema como una experiencia lúdica y reflexiva, no como un diagnóstico.\n""")
    input("Presioná ENTER para continuar...")
    
    # --- CARGA DEL DATASET ---
    print("\n Cargando dataset...")
    try:
        df_inicial = cargar_dataset("datos/data.csv")
        df = limpiar_datos(df_inicial)
        print(f"Dataset cargado: {len(df)} registros disponibles para comparación.")
        
    except FileNotFoundError:
        print("Dataset no encontrado. Se usarán datos simulados para comparación.")
        df = None
        
    except Exception as e:
        print(f"Error al cargar dataset: {e}. Continuando sin datos comparativos.")
        df = None
    
    imprimir_separador()
    
    # --- DATOS DEMOGRÁFICOS ---
    print("\n DATOS DEMOGRÁFICOS") #puramente diseño
    
    nombre = input("¿Cuál es tu nombre o apodo? ").strip() or "UsuarioDesconocido" 
    edad = validar_edad()
    genero = validar_genero()
    
    imprimir_separador()
    
    # --- TEST DE PREGUNTAS ---
    print(f"\n ¡Hola, {nombre}! Comenzamos con el test exploratorio.")
    print("Vas a responder preguntas usando esta escala:")
    print("  1 = Muy en desacuerdo")
    print("  2 = En desacuerdo")
    print("  3 = Neutral")
    print("  4 = De acuerdo")
    print("  5 = Muy de acuerdo\n")
    input("Presioná ENTER para empezar...")
    
    preguntas = obtener_preguntas() #trae la lista con diccionarios con la pregunta, dimension y direccion
    respuestas = [] #carga el valor que le da el usuario a cada pregunta
    
    for i, pregunta in enumerate(preguntas, 1): #arranque a contar las preguntas desde el 1
       
        print(f"\nPregunta {i} de {len(preguntas)}")
        imprimir_separador(40)
        print(f"\n{pregunta['pregunta']}\n")
        print("  [1] Muy en desacuerdo")
        print("  [2] En desacuerdo")
        print("  [3] Neutral")
        print("  [4] De acuerdo")
        print("  [5] Muy de acuerdo\n")
        
        resp = validar_respuesta()
        respuestas.append(resp)
    
    # --- CÁLCULO DE SCORES ---
    print("\n Calculando tus afinidades...")
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
        print("Analizando comparación con dataset...")
    
        try:

            distribucion = calcular_distribucion_mbti(df)

            intereses = intereses_predominantes(df, tipo_predominante)

            promedios = calcular_promedios_por_tipo(df, tipo_predominante)
            
            promedios = calcular_promedios_por_tipo(df, tipo_predominante)
            
            rareza = calcular_rareza(df, tipo_predominante)

            comparacion = comparar_usuario_vs_grupo(df, tipo_predominante, scores)

        except KeyError as error:

            print(f"Error en el análisis del dataset: {error}")
    
    
    
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
    if df is None:
        print("\nNo se generarán gráficos porque el dataset no pudo cargarse.")
        print("Fin del test. Gracias por tu participación!")
        return
    
    while True:

        try:
            print("\n VISUALIZACIONES GENERADAS")
            
            print("  Para observar las visualizacions, ver carpeta: graficos")
            print("  1. Afinidades por polo ")
            print("  2. Distribucion de género por tipo")
            print("  3. Intereses por tipo")
            grafico_usuario = int(input("\nSeleccione una opción (1, 2 o 3): "))

        except ValueError:
            print("Error! Debe ingresar un número.")
            continue

        if grafico_usuario != 1 and grafico_usuario != 2 and grafico_usuario != 3:
            print("Error! Debe ingresar 1, 2 o 3.")
            continue

        if grafico_usuario == 1:
            graficar_torta_usuario(afinidades, nombre)

        elif grafico_usuario == 2:
            if df is None:
                print("No se puede generar el gráfico porque no hay dataset cargado.")
                continue

            genero_pct= calcular_genero_por_tipo (df, tipo_predominante)
            graficar_genero_por_tipo(genero_pct, tipo_predominante, nombre)

        elif grafico_usuario == 3:
            if df is None:
                print("No se puede generar el gráfico porque no hay dataset cargado.")
                continue
            grafico_intereses(df, tipo_predominante, nombre)

        while True:

            seguir = input("\n¿Desea ver otro gráfico? (s/n): ").lower()

            if seguir != "s" and seguir != "n":
                print("Error! Debe ingresar 's' o 'n'.")
                continue

            break

        if seguir == "n":
            print("Fin del test. Gracias por tu participacion!")
            break
        
main()

