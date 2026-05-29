"""
preguntas.py
============
Módulo que almacena las preguntas del test exploratorio MBTI.

Estructura de cada pregunta:
    - pregunta (str): Texto de la pregunta
    - dimension (str): Dimensión MBTI que mide ('EI', 'SN', 'TF', 'JP')
    - direccion (str): Polo al que apunta un puntaje alto ('E','I','S','N','T','F','J','P')

Escala de respuesta (Likert):
    1 = Muy en desacuerdo  → -2 puntos al polo indicado
    2 = En desacuerdo      → -1 punto
    3 = Neutral            →  0 puntos
    4 = De acuerdo         → +1 punto
    5 = Muy de acuerdo     → +2 puntos

Total: 20 preguntas (5 por dimensión).
"""


def obtener_preguntas() -> list:
    """
    Retorna la lista completa de preguntas del test.

    Retorna:
        list[dict]: Lista de diccionarios con pregunta, dimension y direccion.
    """
    preguntas = [

        # ─── Dimensión E/I (Extroversión / Introversión) ───
        {
            "pregunta": "Preferís pasar el tiempo libre con grupos de personas "
                        "en lugar de estar solo/a.",
            "dimension": "EI",
            "direccion": "E"
        },
        {
            "pregunta": "Después de un día social intenso, te sentís con más "
                        "energía, no más cansado/a.",
            "dimension": "EI",
            "direccion": "E"
        },
        {
            "pregunta": "Necesitás tiempo a solas para recargar energías después "
                        "de interactuar con mucha gente.",
            "dimension": "EI",
            "direccion": "I"
        },
        {
            "pregunta": "Preferís pensar en profundidad antes de hablar, "
                        "en lugar de pensar en voz alta.",
            "dimension": "EI",
            "direccion": "I"
        },
        {
            "pregunta": "Sos de los/as que toman la iniciativa en conversaciones "
                        "con personas nuevas.",
            "dimension": "EI",
            "direccion": "E"
        },

        # ─── Dimensión S/N (Sensorial / Intuitivo) ───
        {
            "pregunta": "Preferís basarte en hechos concretos y detalles "
                        "antes de tomar decisiones.",
            "dimension": "SN",
            "direccion": "S"
        },
        {
            "pregunta": "Disfrutás más de las actividades prácticas y concretas "
                        "que de las teóricas o abstractas.",
            "dimension": "SN",
            "direccion": "S"
        },
        {
            "pregunta": "Te resulta más interesante explorar posibilidades futuras "
                        "que analizar el estado actual de las cosas.",
            "dimension": "SN",
            "direccion": "N"
        },
        {
            "pregunta": "A menudo imaginás escenarios hipotéticos o conexiones "
                        "entre ideas que no son evidentes.",
            "dimension": "SN",
            "direccion": "N"
        },
        {
            "pregunta": "Confiás más en la experiencia directa que en las "
                        "teorías o presentimientos.",
            "dimension": "SN",
            "direccion": "S"
        },

        # ─── Dimensión T/F (Pensamiento / Sentimiento) ───
        {
            "pregunta": "Al tomar decisiones importantes, priorizás la lógica "
                        "y los datos por sobre los sentimientos.",
            "dimension": "TF",
            "direccion": "T"
        },
        {
            "pregunta": "Cuando alguien tiene un problema, preferís darle "
                        "soluciones concretas antes que apoyo emocional.",
            "dimension": "TF",
            "direccion": "T"
        },
        {
            "pregunta": "Considerás el impacto emocional en las personas "
                        "como un factor clave en tus decisiones.",
            "dimension": "TF",
            "direccion": "F"
        },
        {
            "pregunta": "Te resulta fácil criticar o señalar errores de otros "
                        "cuando es necesario, aunque les cause incomodidad.",
            "dimension": "TF",
            "direccion": "T"
        },
        {
            "pregunta": "La armonía en el grupo es, para vos, más importante "
                        "que tener razón en una discusión.",
            "dimension": "TF",
            "direccion": "F"
        },

        # ─── Dimensión J/P (Juzgador / Perceptivo) ───
        {
            "pregunta": "Preferís tener un plan claro y definido antes de "
                        "comenzar cualquier proyecto.",
            "dimension": "JP",
            "direccion": "J"
        },
        {
            "pregunta": "Te sentís más cómodo/a cuando las cosas están "
                        "organizadas, planificadas y bajo control.",
            "dimension": "JP",
            "direccion": "J"
        },
        {
            "pregunta": "Disfrutás improvisar y adaptarte a las situaciones "
                        "a medida que surgen.",
            "dimension": "JP",
            "direccion": "P"
        },
        {
            "pregunta": "Preferís mantener tus opciones abiertas en lugar de "
                        "tomar decisiones definitivas apresuradamente.",
            "dimension": "JP",
            "direccion": "P"
        },
        {
            "pregunta": "Cumplir con plazos y fechas límite te da una sensación "
                        "de satisfacción y alivio.",
            "dimension": "JP",
            "direccion": "J"
        },
    ]
    
    return preguntas
