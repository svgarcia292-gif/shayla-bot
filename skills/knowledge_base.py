"""
Knowledge base containing all the prospecting methodologies, flows, and templates
from ProspectBot 2026 — integrated with Shayla's personality.
"""

SYSTEM_PROMPT = """Eres Shayla, una mentora de prospección profesional experta en cuatro metodologías integradas:
1. Hot Outreach (Shan Hanif / Genflow) — convertir contacto frío en caliente antes de escribir
2. Creator Vision Framework (Jun Yuh / Creator College) — marca personal basada en valor
3. Método Lanzamiento (David Turu) — urgencia y escasez real mediante storytelling
4. Principio 1.2x — hacer un 20% más que los demás de forma consistente

PERSONALIDAD:
- Directa, sin florituras ni frases motivacionales vacías
- Usas analogías técnicas/ingenieriles (inputs → procesos → outputs, backlog, retry con backoff, API pública)
- Honesta sobre el esfuerzo que requiere cada cosa
- Cuando alguien está bloqueado, simplificas al siguiente paso mínimo posible
- Nunca das teoría sin una acción concreta al final
- Hablas en español siempre, con naturalidad

REGLAS:
- Máximo 2 preguntas por mensaje
- Cada respuesta termina con un próximo paso claro y ejecutable hoy
- Cuando generes mensajes de outreach, explica brevemente por qué cada parte funciona
- Si alguien está desanimado, nombras el bloqueo emocional específico y reduces al mínimo accionable
- Recuerdas contexto del usuario durante la conversación (área técnica, objetivo, perfil, bloqueos)
- Para oportunidades no convencionales (podcast, eventos, personas inaccesibles), aplicas el método lanzamiento
"""

FLOWS = {
    "onboarding": {
        "trigger": "primera vez sin contexto claro",
        "response": "Hola, soy Shayla. Estoy aquí para ayudarte a conseguir lo que quieres — trabajo, clientes, un puesto específico, aparecer en un podcast, conseguir una reunión difícil, lo que sea. ¿Qué es exactamente lo que quieres conseguir y cuándo lo necesitas?"
    },
    "job_search": {
        "name": "Búsqueda de trabajo",
        "diagnosis_questions": [
            "¿Qué tipo de trabajo buscas? (rol técnico, sector, tamaño de empresa)",
            "¿Qué tienes para mostrar ahora mismo? (proyectos, GitHub, portafolio)",
            "¿Cuánto tiempo llevas buscando y qué acciones has tomado?"
        ],
        "profiles": {
            "A": {
                "name": "Sin nada visible todavía",
                "desc": "No tiene proyectos, presencia online ni ha aplicado",
                "plan": "Activo mínimo visible en 72 horas: un proyecto funcional en GitHub + perfil de LinkedIn con estructura mínima decente. No saltar a enviar mensajes sin esto."
            },
            "B": {
                "name": "Tiene material, sin sistema",
                "desc": "Tiene experiencia o proyectos pero aplica aleatoriamente",
                "plan": "ICP definido (10 empresas objetivo con criterios claros) + pipeline en Notion/Sheets + Hot Outreach aplicado."
            },
            "C": {
                "name": "Tiene sistema, sin resultados",
                "desc": "Aplica estructuradamente pero sin respuesta",
                "plan": "Diagnóstico de cuál de los tres elementos falla: mensajes, perfil o target."
            }
        }
    },
    "opportunity": {
        "name": "Oportunidades puntuales",
        "description": "Podcasts, charlas, reuniones con inaccesibles, colaboraciones, freelance, medios",
        "diagnosis": [
            "¿Qué quieres conseguir exactamente? ¿Con quién? ¿Para cuándo?",
            "¿Tienes alguna conexión existente con esa persona/organización?",
            "¿Tienes algo concreto que mostrar como prueba de credibilidad?"
        ],
        "plan_steps": [
            "Calentamiento de 5-7 días (contenido sobre el tema, interacciones previas con el target)",
            "Mensaje de contacto con prueba de valor concreta",
            "Secuencia de 3-4 toques si no hay respuesta, cada uno aportando algo nuevo",
            "Cierre o descarte limpio en día 14"
        ]
    },
    "personal_brand": {
        "name": "Marca personal",
        "diagnosis": [
            "¿Tienes presencia online ahora? ¿Dónde?",
            "¿Sobre qué puedes hablar con autoridad real?",
            "¿Tienes 20-30 minutos al día para crear?"
        ],
        "framework": "Creator Vision: Define Mensaje → Define Avatar → Define Unicidad → Plan 3-1-2-1"
    },
    "message_gen": {
        "name": "Generador de mensajes",
        "required_data": [
            "A quién va: cargo, empresa, relación previa",
            "Objetivo del mensaje: ¿qué quieres que pase después?",
            "Contexto de esa persona: algo específico investigado",
            "Qué puedes aportar tú: relevante para ellos ahora"
        ],
        "structure": {
            "conexion": "Algo específico de ellos (1 frase)",
            "valor_anticipado": "Lo que traes (1 frase)",
            "prueba": "Algo tangible (enlace/insight)",
            "pregunta_pequena": "CTA mínimo, 30 segundos de respuesta"
        },
        "max_frases": 5,
        "donts": [
            "No empieces con 'Me llamo X y soy...'",
            "No digas 'estaría encantado de tener una llamada...'",
            "No uses plantillas genéricas",
            "No pidas nada en el primer mensaje"
        ]
    },
    "interview_prep": {
        "name": "Preparación de entrevista",
        "outputs": [
            "3 cosas que el entrevistador investigó de ti",
            "3 puntos de valor más relevantes para ESE rol",
            "Propuesta de 30 Días adaptada al rol y empresa",
            "2 preguntas más inteligentes para el final",
            "Cómo pedir el siguiente paso sin sonar desesperado"
        ]
    },
    "emotional_block": {
        "name": "Desbloqueo emocional",
        "blocks": {
            "vergüenza": "Prospectar no es venderte. Es hacer visible el valor que ya tienes. Si un problema existe y tú puedes resolverlo, ocultarte no es humildad, es ineficiencia.",
            "mendigar": "Hay diferencia entre suplicar y proponer. Suplicar es pedir un favor. Proponer es llegar con algo concreto que resuelve un problema real. Si tu mensaje empieza por ellos, no por ti, no estás mendigando.",
            "desesperado": "La desesperación se nota en el mensaje genérico de copia-pega, no en el contacto proactivo. Un mensaje específico, con investigación real, no suena desesperado.",
            "no_suficiente": "El 'suficientemente bueno' no llega esperando. Llega haciendo. El primer paso es actuar con lo que tienes ahora y mejorar en el proceso.",
            "ya_intente": "El problema no es el esfuerzo — es qué parte del sistema está fallando. Vamos a identificarla."
        }
    },
    "message_audit": {
        "name": "Auditoría de mensajes",
        "criteria": [
            "¿Empieza por ellos o por ti?",
            "¿Hay algo específico y real? (no genérico)",
            "¿Pide demasiado en el primer contacto?",
            "¿Hay prueba de valor? (enlace, análisis, proyecto)",
            "¿Es demasiado largo? (máx 5-6 frases)",
            "¿El CTA es claro y pequeño?"
        ],
        "silence_diagnosis": [
            "¿Has hecho calentamiento previo?",
            "¿Has hecho follow-up? (80% de éxitos vienen del 2º o 3er toque)",
            "¿Es el target correcto?"
        ]
    },
    "response_mgmt": {
        "name": "Gestión de respuestas",
        "positive": {
            "steps": [
                "Confirmar interés sin sonar excesivamente emocionado",
                "Hacer UNA pregunta de calificación",
                "Proponer siguiente paso concreto (20 min, no 'cuando quieras')"
            ]
        },
        "negative": "Perfectamente entendido. ¿Estaría bien que volviera a contactar en [3 meses]? Mientras tanto, seguiré publicando sobre [tema relevante].",
        "silence": "Entiendo que estáis ocupados. Si en algún momento tiene sentido conectar, aquí estaré. Seguiré trabajando en [proyecto relevante]."
    },
    "internal_opps": {
        "name": "Oportunidades internas",
        "areas": ["ascenso", "cambio de equipo", "proyecto propio", "visibilidad con dirección"],
        "key_concept": "Patrocinador interno: alguien más senior que habla bien de ti cuando no estás en la sala."
    },
    "metrics": {
        "name": "Métricas y autodiagnóstico",
        "kpIs": {
            "mensajes_semana": {"desc": "Volumen de outreach", "ref": "5-15 calientes"},
            "tasa_aceptacion": {"desc": "Calidad del perfil", "ref": ">30%"},
            "tasa_respuesta": {"desc": "Calidad del mensaje", "ref": ">15%"},
            "ratio_positivas": {"desc": "Relevancia del target", "ref": ">40%"},
            "dias_respuesta": {"desc": "Velocidad del ciclo", "ref": "<7 días"},
            "opps_activas": {"desc": "Volumen de opciones", "ref": "10-15"},
            "conversion": {"desc": "Efectividad global", "ref": ">10%"}
        },
        "symptoms": {
            "nadie_responde": "Problema en el mensaje o en el calentamiento",
            "responden_sin_pasar": "Problema en gestión de respuestas o propuesta de valor",
            "conversaciones_sin_cierre": "Problema en cualificación o siguiente paso",
            "linkedin_baja_aceptacion": "Problema en titular o foto de perfil",
            "respuestas_negativas": "Target incorrecto o timing inadecuado"
        }
    },
    "deep_research": {
        "name": "Investigación profunda",
        "protocol": {
            "primary": ["10-15 posts del founder/CTO", "Blog técnico", "Job descriptions", "Anuncios de producto"],
            "context": ["Crunchbase", "Glassdoor", "GitHub empresa", "Product Hunt reviews"],
            "synthesis": [
                "Problema más urgente de esta empresa/persona ahora",
                "Cómo puedo ayudar a resolverlo específicamente",
                "Qué puedo mostrar que demuestre que ya lo he pensado"
            ]
        }
    },
    "email_outreach": {
        "name": "Outreach por email",
        "structure": {
            "subject": "Máx 8 palabras, específico, sin clickbait",
            "body_p1": "Por qué escribes ahora con referencia específica",
            "body_p2": "Qué traes con evidencia (enlace o 2-3 bullets)",
            "body_p3": "Pregunta pequeña o CTA mínimo",
            "signature": "Limpia con LinkedIn y GitHub"
        },
        "rules": [
            "Máximo 150-200 palabras",
            "Un solo CTA claro",
            "Sin adjuntos en primer email",
            "Enviar mar-jue 8-10am o 2-4pm"
        ],
        "followup": {
            "day4": "Responde a tu propio email con una línea nueva de valor",
            "day9": "Último toque corto con enlace de contexto",
            "after": "Pausa 60 días"
        }
    }
}

TEMPLATES = {
    "hot_outreach_message": """[CONEXIÓN — algo específico de ellos]
Vi que publicaste sobre [X] / que tu equipo está trabajando en [Y]...

[VALOR ANTICIPADO — lo que traes]
He estado construyendo [proyecto/análisis] que aborda exactamente ese problema...

[PRUEBA — algo tangible]
Aquí está: [enlace / imagen / 3 bullets del insight]

[PREGUNTA PEQUEÑA]
¿Tiene sentido esto para vuestro contexto / stack?""",

    "email_structure": """Asunto: [Algo específico sobre ellos]

[Párrafo 1 — Por qué escribes ahora, con referencia específica]
He estado siguiendo el trabajo de [empresa] en [área]. Vuestro reciente [post/release/anuncio] sobre [X] me hizo pensar en [Y].

[Párrafo 2 — Qué traes, con evidencia]
He construido [proyecto/análisis] que aborda exactamente ese problema. [Enlace o 2-3 bullets del insight concreto.]

[Párrafo 3 — Pregunta pequeña o CTA mínimo]
¿Tiene sentido para vuestro contexto? Estaré encantado de explicarlo en más detalle si es de utilidad.""",

    "positive_response": """Genial que resuene, [nombre].

[Pregunta de calificación]
Para prepararme bien, ¿cuál es el mayor reto técnico que estáis enfrentando ahora mismo en [área]?

[Propuesta de siguiente paso]
Si tiene sentido, podríamos hablar 20 minutos esta semana. ¿Cuándo te va bien?""",

    "followup_sequence": """Día 1:  Mensaje inicial (Hot Outreach)
Día 5:  Seguimiento — algo nuevo (dato, update, algo que les afecta)
Día 10: Último toque — corto, sin presión
Día 10+: Archivar como 'Pausado'. Volver en 60-90 días.""",

    "propuesta_30_dias": """PRIMEROS 30 DÍAS EN [EMPRESA] — [TU NOMBRE]

Semana 1-2: Entender antes de proponer
- Reunión con personas clave del equipo/stakeholders
- Revisión de codebase/arquitectura/sistema actual
- Identificar los 3 principales cuellos de botella técnicos

Semana 3: Primer entregable concreto
- [Algo específico: análisis, mejora, prototipo]
- Criterio de éxito: [métrica concreta]

Semana 4: Propuesta de siguiente trimestre
- Prioridades técnicas basadas en lo aprendido
- Quick wins vs. trabajo estructural

Cómo sabré que he tenido éxito al final del mes:
[Una métrica concreta y medible]""",

    "linkedin_titular": """[Especialidad técnica] | [Resultado concreto de proyecto] | Resolviendo [tipo problema] para [tipo empresa/sector]"""
}

PHILOSOPHY = """
FILOSOFÍA: La Persona 1.2x

No se trata de ser 10x (el genio técnico, el rockstar). Todos van a por lo mismo con las mismas estrategias.

Ser 1.2x es hacer consistentemente un 20% más de lo que los demás están dispuestos a hacer. Ese margen, mantenido en el tiempo, genera resultados exponenciales.

Ejemplos prácticos:
- Mientras otros envían el CV, tú envías CV + análisis del problema que resuelve la empresa
- Mientras otros esperan el puesto publicado, tú contactas antes
- Mientras otros comentan 'gran post', tú dejas una idea concreta de 3 frases
- Mientras otros preparan la entrevista la noche anterior, tú llevas una propuesta de 30 días
- Mientras otros publican proyectos sin contexto, tú escribes un hilo explicando qué aprendiste

No es talento. No es suerte. Es disposición a hacer lo que los demás no están dispuestos a hacer.
"""

ANALOGIES = {
    "prospectar": "construir un sistema de inputs → procesos → outputs",
    "ICP": "definir los requisitos antes de escribir el código",
    "pipeline": "backlog priorizado con estados claros",
    "hot_outreach": "calentar el entorno antes de ejecutar la llamada principal",
    "followup": "retry con backoff exponencial de peticiones de red",
    "marca_personal": "API pública que documenta tu valor antes de que te necesiten",
    "ser_1.2x": "añadir un 20% de esfuerzo donde los demás paran, de forma consistente"
}

NUMBERS = {
    "porcentaje_puestos_no_publicados": "70-80%",
    "toques_para_respuesta": "4-5",
    "respuesta_personalizados": "15-25%",
    "respuesta_genericos": "3-5%",
    "prefieren_proactivos": "71%",
    "pipeline_activo_optimo": "10-15"
}

REFERENCES = """
Referencias:
- Shan Hanif — Genflow ($115M+). Método Hot Outreach. genflow.com
- Jun Yuh — Creator College (8M+ seguidores). Creator Vision Framework.
- David Turu (David Tevosyan) — Academia de Lanzamientos. academialanzamientos.com
- Principio 1.2x — Diferenciación basada en consistencia.
"""
