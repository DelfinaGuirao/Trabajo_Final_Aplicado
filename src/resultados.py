"""
Módulo responsable de mostrar resultados finales y guardar datos del usuario.

Incluye:
- Disclaimer ético obligatorio
- Afinidades del usuario
- Comparacion con dataset
"""

import pandas as pd
from src.metricas import obtener_top_tipos


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
        
        if af1 >= af2:
            dominante= polo1
        else:
            dominante= polo2
            
        porcentaje = max(af1, af2)
        
        print(nombre_dim)
        print(f"  Afinidad {dominante}: {porcentaje:.1f}%\n")
    
    top5 = obtener_top_tipos(scores, afinidades)
    print("TOP 5 TIPOS MÁS COMPATIBLES CON TU PERFIL")
    
    for i, (t, pct) in enumerate(top5, 1):
        if t == tipo:
            marca = "- tu tipo" 
        else:
            marca= ""
        print(f"  {i}. {t}: {pct:.1f}%{marca}")
    
    if rareza is not None:
        print("\n TU PERFIL EN EL DATASET")
        
        print(f"  Registros con tipo {tipo}: {rareza['cantidad']:,} de {rareza['total']:,}")
        print(f"  Representa el {rareza['porcentaje']}% del dataset")
        print(f"  Ranking de frecuencia: #{rareza['ranking']} de {rareza['total_tipos']} tipos")
        
    
    if intereses is not None and len(intereses) > 0:
        print(f"\n INTERESES MÁS FRECUENTES EN PERSONAS CON TIPO {tipo}")
        
        for interes, pct in intereses.head(4).items():
            print(f"  {interes}: {pct:.1f}%")
    

    print("VISUALIZACIONES GENERADAS")
    
    print("  Ver carpeta: outputs/graficos/")
    print("  1. Distribución MBTI en el dataset")
    print("  2. Intereses por tipo")
    print("  3. Afinidades por polo")

    
