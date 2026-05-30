"""
Prospector engine — detects user intent and generates responses.
"""
from skills.knowledge_base import FLOWS, TEMPLATES, SYSTEM_PROMPT
from utils.logger import logger
import re

class ProspectorEngine:
    def __init__(self):
        logger.info("ProspectorEngine initialized")

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def detect_flow(self, message: str) -> str:
        msg = message.lower().strip()

        if any(msg.startswith(g) for g in ["hola", "buenas", "hey", "ola", "saludos", "buenos días"]) and len(msg) < 40:
            return "onboarding"

        if any(kw in msg for kw in ["trabajo", "empleo", "curro", "busco trabajo", "cv", "currículum", "entrevista", "contratarme"]):
            return "job_search"

        if any(kw in msg for kw in ["podcast", "charla", "evento", "conferencia", "cliente", "freelance", "oportunidad"]):
            return "opportunity"

        if any(kw in msg for kw in ["marca personal", "linkedin", "contenido", "publicar", "darme a conocer"]):
            return "personal_brand"

        if any(kw in msg for kw in ["mensaje", "escribir", "dm", "contactar", "redactar", "decirle"]):
            return "message_gen"

        if any(kw in msg for kw in ["entrevista", "preparar"]):
            return "interview_prep"

        if any(kw in msg for kw in ["vergüenza", "miedo", "bloqueo", "no sé cómo", "no puedo", "inseguro", "me da cosa", "me da pena"]):
            return "emotional_block"

        if any(kw in msg for kw in ["auditar", "revisa esto", "qué opinas de este", "no responden"]):
            return "message_audit"

        if any(kw in msg for kw in ["respondieron", "me respondió", "me dijeron", "silencio", "me ignoran"]):
            return "response_mgmt"

        if any(kw in msg for kw in ["ascenso", "promoción", "cambio de equipo", "subir de puesto"]):
            return "internal_opps"

        if any(kw in msg for kw in ["métrica", "kpi", "cómo voy", "progreso", "resultados"]):
            return "metrics"

        if any(kw in msg for kw in ["investigar"]):
            return "deep_research"
        if any(kw in msg for kw in ["email", "correo"]):
            return "email_outreach"

        if any(kw in msg for kw in ["buscar", "internet", "google", "dime sobre", "qué sabes de"]):
            return "web_search"

        if any(kw in msg for kw in ["ayuda", "qué hago", "no sé", "explica", "qué es"]):
            return "general_help"

        return "general"

    def get_flow_response(self, flow: str, context: dict = None) -> str:
        responses = {
            "onboarding": "Cuéntame qué necesitas:\n\n💼 Buscar trabajo\n🎙 Una oportunidad (podcast, charla, proyecto)\n📢 Marca personal / LinkedIn\n✉️ Escribir a alguien\n🎯 Preparar entrevista\n🧠 Miedos o bloqueos",
            "job_search": "¿Qué tipo de trabajo buscas y qué tienes para mostrar? (proyectos, LinkedIn, GitHub). Cuéntame y te digo por dónde empezar.",
            "opportunity": "¿Qué oportunidad quieres y con quién? Dame contexto y te ayudo con el enfoque.",
            "personal_brand": "¿Tienes LinkedIn? ¿Sobre qué tema puedes hablar? Con eso arrancamos.",
            "message_gen": "¿A quién le escribes, qué quieres conseguir y qué sabes de esa persona? Dame eso y te redacto algo.",
            "interview_prep": "¿Qué empresa, puesto y en qué fase estás? Dame eso y preparamos la entrevista.",
            "emotional_block": "¿Qué sientes exactamente? ¿Vergüenza, miedo a no ser suficiente, ya lo intentaste y no funcionó? Nómbralo y lo trabajamos.",
            "message_audit": "Pega el mensaje aquí y te digo qué mejorar.",
            "response_mgmt": "¿Te respondieron bien, mal o te ignoraron? Cuéntame y te digo cómo seguir.",
            "internal_opps": "¿Quieres ascender, cambiar de equipo o liderar un proyecto? Dime.",
            "metrics": "Cuéntame cómo te está yendo: ¿cuántos mensajes envías, cuántos responden?",
            "deep_research": "¿Qué empresa o persona quieres investigar?",
            "email_outreach": "¿A quién le escribes y qué sabes de ellos?",
            "general_help": "Dime qué necesitas y te ayudo. Puedo asistirte con trabajo, oportunidades, marca personal o mensajes.",
        }
        return responses.get(flow, responses["general_help"])

    def generate_message(self, **kwargs) -> str:
        template = TEMPLATES["hot_outreach_message"]
        if kwargs.get("context_info"):
            template = template.replace("[X]", kwargs["context_info"])
        if kwargs.get("your_value"):
            template = template.replace("[proyecto/análisis]", kwargs["your_value"])
        template += (
            "\n\nNota: Cambia los [corchetes] por tus datos. "
            "La personalización real es lo que hace que funcione."
        )
        return template

    def audit_message(self, message: str) -> str:
        issues = []
        score = 0

        first = message.split()[0].lower() if message.split() else ""
        if first in ["me", "mi", "yo", "soy", "quiero", "necesito", "busco"]:
            issues.append("❌ Empiezas hablando de ti. Empieza por ellos.")
        else:
            score += 1
            issues.append("✅ Bien, empiezas por ellos.")

        words = len(message.split())
        if words > 60:
            issues.append(f"❌ Muy largo ({words} palabras). Máximo 5-6 frases.")
        else:
            score += 1
            issues.append(f"✅ Extensión bien ({words} palabras).")

        generic = ["estaría encantado", "espero su respuesta", "quedo a la espera", "adjunto mi cv"]
        found = [g for g in generic if g in message.lower()]
        if found:
            issues.append(f"❌ Frases genéricas: {', '.join(found)}")
        else:
            score += 1
            issues.append("✅ Sin frases genéricas.")

        if "?" in message:
            score += 1
            issues.append("✅ Termina con pregunta.")
        else:
            issues.append("❌ Falta pregunta para que puedan responder.")

        if re.search(r'https?://[^\s]+', message):
            score += 1
            issues.append("✅ Incluye enlace.")
        else:
            issues.append("⚠️ Sin enlace. Añade algo que mostrar.")

        if any(w in message.lower() for w in ["reunión", "llamada", "30 minutos"]):
            issues.append("❌ Pides mucho en el primer mensaje. Pide algo pequeño primero.")

        level = f"\n\n{score}/6"
        if score <= 2:
            level += " 🔴 Hay que reescribirlo."
        elif score <= 4:
            level += " 🟡 Ajustable."
        else:
            level += " 🟢 Está bien."

        return "\n".join(issues) + level
