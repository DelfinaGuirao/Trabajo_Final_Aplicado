"""
resultados.py
=============
Módulo responsable de mostrar resultados finales y guardar datos del usuario.

Incluye:
- Disclaimer ético obligatorio
- Afinidades del usuario
- Comparación con dataset
- Guardado en CSV
"""

import pandas as pd
import os
from datetime import datetime
from src.metricas import obtener_top_tipos
from src.utilidades import imprimir_separador


descripciones_tipos = {
    'INTJ': "Estratega reflexivo/a. Tendencia a pensar en sistemas y planes a largo plazo.",
    'INTP': "Pensador/a lógico/a. Tendencia a analizar conceptos y teorías abstractas.",
    'ENTJ': "Líder decisivo/a. Tendencia a organizar y dirigir proyectos con visión.",
    'ENTP': "Debatidor/a innovador/a. Tendencia a explorar ideas y desafiar supuestos.",
    'INFJ': "Idealista comprometido/a. Tendencia a buscar significado y conexiones profundas.",
    'INFP': "Mediador/a sensible. Tendencia a guiarse por valores y creatividad.",
    'ENFJ': "Protagonista empático/a. Tendencia a inspirar y ayudar a los demás.",
    'ENFP': "Activista entusiasta. Tendencia a conectar personas e ideas con energía.",
    'ISTJ': "Logístico/a confiable. Tendencia a ser metódico/a, responsable y sistemático/a.",
    'ISFJ': "Defensor/a dedicado/a. Tendencia a proteger y cuidar a quienes lo rodean.",
    'ESTJ': "Ejecutivo/a organizado/a. Tendencia a implementar orden y procedimientos.",
    'ESFJ': "Cónsul sociable. Tendencia a crear armonía y apoyar a la comunidad.",
    'ISTP': "Virtuoso/a pragmático/a. Tendencia a resolver problemas con herramientas.",
    'ISFP': "Aventurero/a artístico/a. Tendencia a vivir el momento y expresarse.",
    'ESTP': "Emprendedor/a dinámico/a. Tendencia a la acción y el pensamiento práctico.",
    'ESFP': "Animador/a espontáneo/a. Tendencia a disfrutar la vida y entretener.",
}


def mostrar_resultados_finales(nombre, tipo, afinidades, scores, distribucion=None, intereses=None, rareza=None, comparacion=None):
    """
    Muestra el resumen completo de resultados en la consola.

    Incluye disclaimer ético, afinidades, descripción exploratoria,
    datos poblacionales e intereses del grupo.
    """
    
    print(f"\n RESULTADOS EXPLORATORIOS PARA {nombre.upper()}")
    
    print("\n DISCLAIMER ÉTICO")
    
    print("Este sistema NO constituye una herramienta psicológica")
    print("clínica ni diagnóstica. Los resultados representan")
    print("AFINIDADES EXPLORATORIAS basadas en un dataset sintético.")
    print("El MBTI no tiene validez diagnóstica confirmada por")
    print("la psicología científica contemporánea.\n")
    
    print("TU TIPO CON MAYOR AFINIDAD")

    print(f"  Tipo predominante: {tipo}")
    descripcion = descripciones_tipos.get(tipo, "Perfil exploratorio.")
    print(f"  Tendencia exploratoria: {descripcion}\n")
    
    print("AFINIDADES PORCENTUALES POR DIMENSIÓN")
    
    dimensiones = [
        ('E', 'I', 'Extroversión / Introversión'),
        ('S', 'N', 'Sensorial / Intuitivo'),
        ('T', 'F', 'Pensamiento / Sentimiento'),
        ('J', 'P', 'Juzgador / Perceptivo'),
    ]
    
    for polo1, polo2, nombre_dim in dimensiones:
        af1 = afinidades.get(polo1, 50)
        af2 = afinidades.get(polo2, 50)
        dominante = polo1 if af1 >= af2 else polo2
        porcentaje = max(af1, af2)
        barra = _generar_barra(af1)
        print(f"  {nombre_dim}")
        print(f"  {polo1} {barra} {polo2}")
        print(f"  Afinidad {dominante}: {porcentaje:.1f}%\n")
    
    top5 = obtener_top_tipos(scores, afinidades)
    print("TOP 5 TIPOS MÁS COMPATIBLES CON TU PERFIL")
    
    for i, (t, pct) in enumerate(top5, 1):
        marca = "- tu tipo" if t == tipo else ""
        print(f"  {i}. {t}: {pct:.1f}%{marca}")
    
    if rareza:
        print("\n TU PERFIL EN EL DATASET SINTÉTICO")
        
        print(f"  Registros con tipo {tipo}: {rareza['cantidad']:,} de {rareza['total']:,}")
        print(f"  Representa el {rareza['porcentaje']}% del dataset")
        print(f"  Ranking de frecuencia: #{rareza['ranking']} de {rareza['total_tipos']} tipos")
        
        if rareza['ranking'] <= 4:
            print(f"  Es uno de los tipos más frecuentes en el dataset.")
        elif rareza['ranking'] >= rareza['total_tipos'] - 3:
            print(f"  Es uno de los tipos menos frecuentes en el dataset.")
    
    if intereses is not None and len(intereses) > 0:
        print(f"\n INTERESES MÁS FRECUENTES EN PERSONAS CON TIPO {tipo}")
        
        for interes, pct in intereses.head(4).items():
            print(f"  {interes}: {pct:.1f}%")
    

    print("VISUALIZACIONES GENERADAS")
    
    print("  Ver carpeta: outputs/graficos/")
    print("  1. Distribución MBTI en el dataset")
    print("  2. Intereses por tipo")
    print("  3. Tu perfil vs promedio del grupo")
    print("  4. Afinidades por polo")
    print("  5. Radar de afinidades")
    


def guardar_usuario(nombre: str, edad: int, genero: str, tipo: str, afinidades: Dict[str, float], scores: Dict[str, int]):
    """
    Guarda los resultados del usuario en el archivo data/usuarios.csv.

    Parámetros:
        nombre (str): Nombre o apodo del usuario.
        edad (int): Edad del usuario.
        genero (str): Género del usuario.
        tipo (str): Tipo MBTI predominante.
        afinidades (dict): Afinidades porcentuales.
        scores (dict): Scores brutos.
    """
    os.makedirs("data", exist_ok=True)
    ruta = "data/usuarios.csv"
    
    registro = {
        'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'Nombre': nombre,
        'Edad': edad,
        'Genero': genero,
        'Tipo': tipo,
        'Afinidad_E': afinidades.get('E', 0),
        'Afinidad_I': afinidades.get('I', 0),
        'Afinidad_S': afinidades.get('S', 0),
        'Afinidad_N': afinidades.get('N', 0),
        'Afinidad_T': afinidades.get('T', 0),
        'Afinidad_F': afinidades.get('F', 0),
        'Afinidad_J': afinidades.get('J', 0),
        'Afinidad_P': afinidades.get('P', 0),
        'Score_EI': scores.get('EI', 0),
        'Score_SN': scores.get('SN', 0),
        'Score_TF': scores.get('TF', 0),
        'Score_JP': scores.get('JP', 0),
    }
    
    df_nuevo = pd.DataFrame([registro])
    
    if os.path.exists(ruta):
        df_existente = pd.read_csv(ruta)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo
    
    df_final.to_csv(ruta, index=False)


def _generar_barra(afinidad_polo1, largo: int = 20):
    """
    Genera una barra ASCII que representa la distribución entre dos polos.

    Parámetros:
        afinidad_polo1 (float): Porcentaje del primer polo (0-100).
        largo (int): Longitud total de la barra.

    Retorna:
        str: Barra ASCII como '████░░░░░░'.
    """
    n_llenos = int(round(afinidad_polo1 / 100 * largo))
    n_vacios = largo - n_llenos
    return '█' * n_llenos + '░' * n_vacios
