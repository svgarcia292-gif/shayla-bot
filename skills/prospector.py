"""
Prospector engine — core logic that routes user intents to the right flow and generates responses.
Integrates all 12 flows from the knowledge base.
"""
from skills.knowledge_base import FLOWS, TEMPLATES, PHILOSOPHY, ANALOGIES, NUMBERS, REFERENCES, SYSTEM_PROMPT
from utils.logger import logger
import re

class ProspectorEngine:
    def __init__(self):
        logger.info("ProspectorEngine initialized")

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def detect_flow(self, message: str) -> str:
        msg = message.lower().strip()

        greetings = ["hola", "buenas", "hey", "qué tal", "h", "ola", "saludos", "buen dia"]
        if any(msg.startswith(g) for g in greetings) and len(msg) < 30:
            return "onboarding"

        job_keywords = ["trabajo", "empleo", "curro", "puesto", "vacante", "busco trabajo",
                        "contratar", "candidato", "cv", "currículum", "entrevista"]
        if any(kw in msg for kw in job_keywords):
            return "job_search"

        opp_keywords = ["podcast", "charla", "evento", "conferencia", "reunión con",
                        "inaccesible", "colaboración", "freelance", "proyecto", "cliente",
                        "oportunidad", "contactar con", "conseguir una reunión"]
        if any(kw in msg for kw in opp_keywords):
            return "opportunity"

        brand_keywords = ["marca personal", "linkedin", "presencia online", "contenido",
                          "publicar", "crear contenido", "audiencia", "seguidores",
                          "visibilidad", "influencia"]
        if any(kw in msg for kw in brand_keywords):
            return "personal_brand"

        message_keywords = ["mensaje", "escribir", "dm", "contactar", "outreach",
                           "plantilla", "script", "redactar"]
        if any(kw in msg for kw in message_keywords):
            return "message_gen"

        interview_keywords = ["entrevista", "entrevist", "preparar entrevista",
                             "technical interview", "behavioral"]
        if any(kw in msg for kw in interview_keywords):
            return "interview_prep"

        block_keywords = ["vergüenza", "miedo", "bloqueo", "no sé cómo", "no puedo",
                         "desanimado", "nervios", "inseguro", "no soy suficiente",
                         "mendigando", "desesperado", "ya lo intenté", "no funcionó"]
        if any(kw in msg for kw in block_keywords):
            return "emotional_block"

        audit_keywords = ["auditar", "revisar mensaje", "revisa esto", "qué opinas de este",
                         "mensaje que envié", "no responden"]
        if any(kw in msg for kw in audit_keywords):
            return "message_audit"

        response_keywords = ["respondieron", "me respondió", "me dijeron que sí",
                            "me dijeron que no", "no me responden", "respuesta positiva",
                            "respuesta negativa", "silencio"]
        if any(kw in msg for kw in response_keywords):
            return "response_mgmt"

        internal_keywords = ["ascenso", "promoción", "cambio de equipo", "proyecto interno",
                            "dentro de la empresa", "crecer internamente"]
        if any(kw in msg for kw in internal_keywords):
            return "internal_opps"

        metrics_keywords = ["métrica", "kpi", "diagnóstico", "cómo voy", "medir",
                           "estadísticas", "progreso", "resultados"]
        if any(kw in msg for kw in metrics_keywords):
            return "metrics"

        research_keywords = ["investigar", "research", "investigación previa",
                            "antes de contactar", "preparación", "estudiar empresa"]
        if any(kw in msg for kw in research_keywords):
            return "deep_research"

        email_keywords = ["email", "correo", "mail", "e-mail"]
        if any(kw in msg for kw in email_keywords):
            return "email_outreach"

        if any(kw in msg for kw in ["buscar", "internet", "google", "busca información",
                                    "investiga sobre", "dime sobre"]):
            return "web_search"

        if any(kw in msg for kw in ["ayuda", "qué hago", "no sé", "consejo", "recomienda"]):
            return "general_help"

        return "general"

    def get_flow_response(self, flow: str, context: dict = None) -> str:
        if flow == "onboarding":
            return FLOWS["onboarding"]["response"]

        if flow == "job_search":
            return self._job_search_response(context)

        if flow == "opportunity":
            return self._opportunity_response()

        if flow == "personal_brand":
            return self._personal_brand_response()

        if flow == "message_gen":
            return self._message_gen_response()

        if flow == "interview_prep":
            return self._interview_prep_response()

        if flow == "emotional_block":
            return self._emotional_block_response(context)

        if flow == "message_audit":
            return self._message_audit_response()

        if flow == "response_mgmt":
            return self._response_mgmt_response()

        if flow == "internal_opps":
            return self._internal_opps_response()

        if flow == "metrics":
            return self._metrics_response()

        if flow == "deep_research":
            return self._deep_research_response()

        if flow == "email_outreach":
            return self._email_outreach_response()

        if flow == "general_help":
            return "¿Qué es exactamente lo que quieres conseguir? Cuéntame más y te ayudo a crear un plan."

        return self._general_response(context)

    def _job_search_response(self, context: dict = None) -> str:
        return (
            "Vamos a diagnosticar tu situación actual.\n\n"
            "1️⃣ ¿Qué tipo de trabajo buscas? (rol técnico, sector, tamaño de empresa)\n"
            "2️⃣ ¿Qué tienes para mostrar ahora mismo? (proyectos, GitHub, portafolio)\n"
            "3️⃣ ¿Cuánto tiempo llevas buscando y qué acciones has tomado?\n\n"
            "Cuéntame esto y te digo exactamente en qué perfil estás y qué hacer."
        )

    def _opportunity_response(self) -> str:
        return (
            "Cuéntame más sobre la oportunidad que quieres conseguir:\n\n"
            "1️⃣ ¿Qué es exactamente? ¿Podcast, charla, reunión, colaboración, freelance?\n"
            "2️⃣ ¿Con quién? (persona o empresa)\n"
            "3️⃣ ¿Para cuándo lo necesitas?\n"
            "4️⃣ ¿Tienes algo concreto que mostrar como prueba de credibilidad?"
        )

    def _personal_brand_response(self) -> str:
        return (
            "Construyamos tu marca personal desde donde estás.\n\n"
            "1️⃣ ¿Tienes presencia online ahora? ¿Dónde?\n"
            "2️⃣ ¿Sobre qué puedes hablar con autoridad real? (no hace falta ser experto, "
            "solo saber más que el 80% en algo concreto)\n"
            "3️⃣ ¿Tienes 20-30 minutos al día para crear contenido?\n\n"
            "Con eso te ayudo a definir tu Mensaje, tu Avatar y tu Unicidad."
        )

    def _message_gen_response(self) -> str:
        return (
            "Para generar un mensaje efectivo, necesito 4 cosas:\n\n"
            "1️⃣ **A quién va dirigido**: cargo, empresa, ¿has interactuado antes con su contenido?\n"
            "2️⃣ **Objetivo**: ¿qué quieres que pase después de leerlo?\n"
            "3️⃣ **Contexto específico**: algo que hayas investigado sobre esa persona/empresa\n"
            "4️⃣ **Qué puedes aportar**: ¿qué tienes que sea relevante para ellos ahora?\n\n"
            "Dame esa info y te escribo un mensaje con la estructura de Hot Outreach."
        )

    def _interview_prep_response(self) -> str:
        return (
            "Para preparar tu entrevista, necesito:\n\n"
            "1️⃣ Empresa y rol exacto\n"
            "2️⃣ Fase de la entrevista (técnica / RRHH / hiring manager / final)\n"
            "3️⃣ Nombre del entrevistador si lo sabes\n\n"
            "Con eso te preparo:\n"
            "• Las 3 cosas que habrán investigado de ti\n"
            "• Tus 3 puntos de valor más relevantes para ESE rol\n"
            "• Una Propuesta de 30 Días adaptada\n"
            "• Las 2 preguntas más inteligentes para el final"
        )

    def _emotional_block_response(self, context: dict = None) -> str:
        return (
            "Los bloqueos son normales. Todos los hemos tenido.\n\n"
            "Dime exactamente qué sientes o piensas cuando piensas en prospectar:\n"
            "• ¿Te da vergüenza 'venderte'?\n"
            "• ¿Sientes que estás mendigando?\n"
            "• ¿Te preocupa parecer desesperado?\n"
            "• ¿Crees que no eres 'suficientemente bueno'?\n"
            "• ¿Ya lo intentaste y no funcionó?\n\n"
            "Nombra el bloqueo y lo trabajamos."
        )

    def _message_audit_response(self) -> str:
        return (
            "Pega aquí el mensaje que quieres que audite. Lo revisaré con estos 6 criterios:\n\n"
            "1️⃣ ¿Empieza por ellos o por ti?\n"
            "2️⃣ ¿Hay algo específico y real? (no genérico)\n"
            "3️⃣ ¿Pide demasiado en el primer contacto?\n"
            "4️⃣ ¿Hay prueba de valor?\n"
            "5️⃣ ¿Es demasiado largo? (máx 5-6 frases)\n"
            "6️⃣ ¿El CTA es claro y pequeño?"
        )

    def _response_mgmt_response(self) -> str:
        return (
            "Cuéntame qué pasó:\n\n"
            "• **Respondieron positivo** → Te ayudo a responder sin sonar emocionado de más\n"
            "• **Respondieron negativo o 'ahora no'** → Te doy el cierre elegante que deja puerta abierta\n"
            "• **Silencio total** → Analizamos si es el mensaje, el calentamiento o el target"
        )

    def _internal_opps_response(self) -> str:
        return (
            "Oportunidades dentro de tu empresa — el camino más ignorado.\n\n"
            "¿Qué buscas exactamente?\n"
            "• Ascenso / promoción\n"
            "• Cambio de equipo\n"
            "• Liderar un proyecto propio\n"
            "• Más visibilidad con dirección\n\n"
            "El principio es el mismo que para fuera: Hot Outreach hacia adentro."
        )

    def _metrics_response(self) -> str:
        return (
            "Revisemos tus métricas. Dime cómo te está yendo:\n\n"
            "• ¿Cuántos mensajes envías a la semana?\n"
            "• ¿Cuántos te responden?\n"
            "• ¿Cuántas conversaciones se convierten en algo concreto?\n\n"
            "Según tu síntoma, identificamos dónde está el cuello de botella."
        )

    def _deep_research_response(self) -> str:
        return (
            "La investigación es el paso que más gente salta y el que más diferencia los resultados.\n\n"
            "Dime la empresa o persona que quieres investigar y te guío:\n"
            "1️⃣ Fuentes primarias (posts, blog, job descriptions, anuncios)\n"
            "2️⃣ Fuentes de contexto (Crunchbase, Glassdoor, GitHub, reviews)\n"
            "3️⃣ Síntesis: problema urgente → cómo ayudas → qué mostrar"
        )

    def _email_outreach_response(self) -> str:
        return (
            "Email outreach — canal diferente, mismos principios.\n\n"
            "Dime:\n"
            "1️⃣ ¿A quién le escribes? (nombre, cargo, empresa)\n"
            "2️⃣ ¿Tienes su email? (si no, te digo cómo conseguirlo)\n"
            "3️⃣ ¿Qué contexto específico tienes sobre ellos?\n"
            "4️⃣ ¿Qué puedes aportar?"
        )

    def _general_response(self, context: dict = None) -> str:
        return (
            "Cuéntame más sobre lo que necesitas.\n\n"
            "Puedo ayudarte con:\n"
            "🔍 **Buscar trabajo** — sistema completo de prospección\n"
            "🎙 **Conseguir oportunidades** — podcasts, charlas, reuniones\n"
            "📢 **Marca personal** — contenido que te posiciona\n"
            "✉️ **Generar mensajes** — outreach que funciona\n"
            "🎯 **Preparar entrevistas** — Propuesta de 30 Días incluida\n"
            "🧠 **Desbloqueos emocionales** — la parte que nadie entrena\n"
            "🔎 **Buscar en internet** — información actualizada\n"
            "📊 **Auditar mensajes** — dime qué has escrito\n\n"
            "¿Por dónde empezamos?"
        )

    def generate_message(self, target_name: str = None, target_role: str = None,
                         target_company: str = None, context_info: str = None,
                         your_value: str = None, goal: str = None) -> str:
        template = TEMPLATES["hot_outreach_message"]
        result = template

        if context_info:
            result = result.replace("[X]", context_info)
        if target_name:
            result = result.replace("[nombre]", target_name)
        if your_value:
            result = result.replace("[proyecto/análisis]", your_value)

        notes = (
            "\n\n---\n📝 **Notas sobre por qué funciona este mensaje:**\n"
            "1️⃣ Empieza por **ellos** — mencionas algo específico de su trabajo\n"
            "2️⃣ **Valor anticipado** — no pides, traes algo\n"
            "3️⃣ **Prueba tangible** — hay evidencia de lo que dices\n"
            "4️⃣ **CTA mínimo** — responder es fácil y rápido\n\n"
            "⚠️ Personaliza los corchetes antes de enviar. La personalización real es lo que hace que funcione."
        )
        return result + notes

    def audit_message(self, message: str) -> str:
        issues = []
        score = 0

        first_word = message.split()[0].lower() if message.split() else ""
        self_refs = ["me", "mi", "yo", "soy", "quiero", "necesito", "busco"]
        starts_with_self = any(first_word == r or first_word.startswith(r) for r in self_refs)

        if starts_with_self:
            issues.append("❌ Empieza por ti. Debería empezar por algo de ellos.")
        else:
            score += 1
            issues.append("✅ Empieza por ellos. Bien.")

        words = len(message.split())
        if words > 60:
            issues.append("❌ Demasiado largo (>60 palabras). Máximo 5-6 frases.")
        else:
            score += 1
            issues.append(f"✅ Longitud adecuada ({words} palabras).")

        generic_phrases = ["estaría encantado", "espero su respuesta", "quedo a la espera",
                          "muchas gracias de antemano", "para quien corresponda",
                          "interesado en trabajar", "adjunto mi cv"]
        found_generic = [p for p in generic_phrases if p in message.lower()]
        if found_generic:
            issues.append(f"❌ Frases genéricas detectadas: {', '.join(found_generic)}")
        else:
            score += 1
            issues.append("✅ Sin frases genéricas.")

        if "?" in message:
            score += 1
            issues.append("✅ Incluye pregunta (CTA).")
        else:
            issues.append("❌ No hay pregunta. El mensaje necesita un CTA claro.")

        has_url = bool(re.search(r'https?://[^\s]+', message))
        if has_url:
            score += 1
            issues.append("✅ Incluye enlace (prueba de valor).")
        else:
            issues.append("⚠️ No se detecta enlace. Considera añadir prueba tangible.")

        if "reunión" in message.lower() or "llamada" in message.lower() or "30 minutos" in message.lower():
            issues.append("❌ Pides demasiado tiempo en primer contacto. Reduce a algo de 30 segundos.")

        summary = f"\n📊 **Puntuación: {score}/6**\n"
        if score <= 2:
            summary += "🔴 Necesita reescribirse completamente."
        elif score <= 4:
            summary += "🟡 Tiene potencial pero requiere ajustes importantes."
        else:
            summary += "🟢 Bien encaminado. Ajusta los detalles y está listo."

        return "\n".join(issues) + summary

    def get_kpi_advice(self, symptom: str) -> str:
        symptoms_map = {
            "nadie responde": FLOWS["message_audit"]["silence_diagnosis"],
            "responden pero no pasa nada": ["Problema en gestión de respuestas", "Revisar propuesta de valor"],
            "conversaciones pero no cierran": ["Problema en cualificación", "Siguiente paso poco claro"],
            "respuestas negativas": ["Target incorrecto", "Timing inadecuado"],
        }
        for key, advice in symptoms_map.items():
            if key in symptom.lower():
                return "Diagnóstico: " + "\n".join(f"• {a}" for a in advice)
        return "Cuéntame más específicamente qué está pasando para diagnosticarlo."
