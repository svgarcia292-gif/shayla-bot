"""
Prospector engine — detects user intent and generates beginner-friendly responses.
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

        greetings = ["hola", "buenas", "hey", "qué tal", "h", "ola", "saludos", "buen dia", "buenos días"]
        if any(msg.startswith(g) for g in greetings) and len(msg) < 40:
            return "onboarding"

        if any(kw in msg for kw in ["trabajo", "empleo", "curro", "puesto", "vacante", "busco trabajo",
                                    "contratar", "candidato", "cv", "currículum", "entrevista", "contratarme"]):
            return "job_search"

        if any(kw in msg for kw in ["podcast", "charla", "evento", "conferencia", "reunión con",
                                    "colaboración", "freelance", "cliente", "oportunidad",
                                    "contactar con", "conseguir una reunión"]):
            return "opportunity"

        if any(kw in msg for kw in ["marca personal", "linkedin", "presencia online", "contenido",
                                    "publicar", "crear contenido", "audiencia", "seguidores",
                                    "visibilidad", "darme a conocer"]):
            return "personal_brand"

        if any(kw in msg for kw in ["mensaje", "escribir", "dm", "contactar", "outreach",
                                    "plantilla", "script", "redactar", "decirle"]):
            return "message_gen"

        if any(kw in msg for kw in ["entrevista", "entrevist", "preparar"]):
            return "interview_prep"

        if any(kw in msg for kw in ["vergüenza", "miedo", "bloqueo", "no sé cómo", "no puedo",
                                    "desanimado", "nervios", "inseguro", "no soy suficiente",
                                    "mendigando", "desesperado", "ya lo intenté", "no funcionó",
                                    "me da cosa", "me da pena", "no me sale"]):
            return "emotional_block"

        if any(kw in msg for kw in ["auditar", "revisar mensaje", "revisa esto", "qué opinas de este",
                                    "mensaje que envié", "no responden", "revisa este mensaje"]):
            return "message_audit"

        if any(kw in msg for kw in ["respondieron", "me respondió", "me dijeron que sí",
                                    "me dijeron que no", "no me responden", "respuesta",
                                    "silencio", "me ignoran"]):
            return "response_mgmt"

        if any(kw in msg for kw in ["ascenso", "promoción", "cambio de equipo", "proyecto interno",
                                    "dentro de la empresa", "crecer internamente", "subir de puesto"]):
            return "internal_opps"

        if any(kw in msg for kw in ["métrica", "kpi", "diagnóstico", "cómo voy", "medir",
                                    "estadísticas", "progreso", "resultados"]):
            return "metrics"

        if any(kw in msg for kw in ["investigar", "research", "investigación previa",
                                    "antes de contactar", "preparación", "estudiar empresa",
                                    "investigar empresa"]):
            return "deep_research"

        if any(kw in msg for kw in ["email", "correo", "mail", "e-mail"]):
            return "email_outreach"

        if any(kw in msg for kw in ["buscar", "internet", "google", "busca información",
                                    "investiga sobre", "dime sobre", "qué sabes de"]):
            return "web_search"

        if any(kw in msg for kw in ["ayuda", "qué hago", "no sé", "consejo", "recomienda",
                                    "explica", "qué es", "cómo se hace"]):
            return "general_help"

        return "general"

    def get_flow_response(self, flow: str, context: dict = None) -> str:
        handler = {
            "onboarding": self._onboarding_response,
            "job_search": self._job_search_response,
            "opportunity": self._opportunity_response,
            "personal_brand": self._personal_brand_response,
            "message_gen": self._message_gen_response,
            "interview_prep": self._interview_prep_response,
            "emotional_block": self._emotional_block_response,
            "message_audit": self._message_audit_response,
            "response_mgmt": self._response_mgmt_response,
            "internal_opps": self._internal_opps_response,
            "metrics": self._metrics_response,
            "deep_research": self._deep_research_response,
            "email_outreach": self._email_outreach_response,
            "general_help": self._general_help_response,
        }.get(flow, self._general_response)
        return handler()

    def _onboarding_response(self) -> str:
        return (
            "¡Hola! ✨ Soy Shayla, y estoy aquí para ayudarte a conseguir oportunidades profesionales.\n\n"
            "Pero vamos a empezar desde el principio: ¿sabes qué es lo que hago exactamente?\n\n"
            "Te explico: Hay muchas formas de encontrar trabajo, conseguir clientes, aparecer en "
            "un podcast, o simplemente hacer networking. Pero la mayoría de la gente no sabe por dónde "
            "empezar o hace cosas que no funcionan.\n\n"
            "Yo te enseño un método paso a paso para que puedas conseguir lo que quieras, "
            "sin tener que ser un vendedor ni sentirte incómodo.\n\n"
            "Dime, ¿qué te gustaría conseguir?\n"
            "• ¿Buscar trabajo?\n"
            "• ¿Conseguir clientes o proyectos?\n"
            "• ¿Aparecer en un podcast o dar una charla?\n"
            "• ¿Crear tu marca personal?\n"
            "• ¿O simplemente estás explorando y quieres entender de qué va todo esto?"
        )

    def _job_search_response(self) -> str:
        return (
            "Vale, buscar trabajo. Vamos a ver por dónde empezamos.\n\n"
            "Antes de nada, ¿sabes qué es lo que hace que alguien consiga trabajo hoy en día?\n\n"
            "La mayoría de la gente hace esto: enviar CV a ofertas de LinkedIn y esperar. "
            "Y eso funciona... para muy pocos. Porque el 70-80% de los puestos se cubren "
            "antes de que se publiquen, a través de contactos y referencias.\n\n"
            "Pero no te preocupes, no necesitas ser un experto en networking. Solo necesitas "
            "un sistema, y yo te enseño.\n\n"
            "Cuéntame un poco:\n"
            "1️⃣ ¿Qué tipo de trabajo buscas? (programador, diseñador, lo que sea)\n"
            "2️⃣ ¿Tienes algún proyecto o trabajo anterior que puedas mostrar?\n"
            "3️⃣ ¿Has hecho algo hasta ahora para buscar? (enviar CV, hablar con gente...)"
        )

    def _opportunity_response(self) -> str:
        return (
            "¡Qué interesante! Cuéntame más sobre esa oportunidad que quieres conseguir.\n\n"
            "Para que te ayude bien, necesito entender:\n\n"
            "1️⃣ ¿Qué es exactamente lo que quieres? (¿un podcast, una charla en un evento, "
            "una reunión con alguien específico, un proyecto freelance?)\n"
            "2️⃣ ¿Con quién o con qué empresa? Si no sabes el nombre, dime el sector.\n"
            "3️⃣ ¿Para cuándo lo necesitas? (¿hay una fecha límite o es sin prisa?)\n\n"
            "Y algo importante: ¿has tenido algún contacto con esa persona o empresa antes? "
            "¿O es completamente nuevo?"
        )

    def _personal_brand_response(self) -> str:
        return (
            "Marca personal... suena a cosa de influencers, ¿verdad? Pues no es para tanto.\n\n"
            "Te explico simple: tener marca personal solo significa que cuando alguien busque "
            "tu nombre en internet, encuentre cosas buenas de ti. Que sepas quién eres y qué "
            "haces, y que la gente que te necesita pueda encontrarte.\n\n"
            "No tienes que ser famoso ni tener miles de seguidores. Solo necesitas:\n"
            "• Un perfil de LinkedIn decente\n"
            "• Publicar de vez en cuando sobre lo que sabes\n"
            "• Que la gente pueda ver que existes y qué haces\n\n"
            "Dime:\n"
            "1️⃣ ¿Tienes LinkedIn u otra red social profesional ahora?\n"
            "2️⃣ ¿Sobre qué tema podrías hablar sin problema? (no hace falta ser experto mundial, "
            "solo saber más que la mayoría)"
        )

    def _message_gen_response(self) -> str:
        return (
            "Vas a escribirle a alguien y no sabes cómo hacerlo. Normal, a todo el mundo le pasa.\n\n"
            "El truco está en no escribir como un robot. La mayoría de los mensajes que recibe "
            "la gente son genéricos y aburridos, y los borran en 2 segundos.\n\n"
            "Para escribir un buen mensaje, necesito saber:\n\n"
            "1️⃣ **¿A quién le vas a escribir?** (nombre, cargo, empresa)\n"
            "2️⃣ **¿Qué quieres conseguir?** (¿que te responda, que te contrate, que te dé una oportunidad?)\n"
            "3️⃣ **¿Has tenido contacto antes con esta persona?** (¿le has comentado algo en LinkedIn, "
            "compartido su contenido?)\n"
            "4️⃣ **¿Qué sabes de ellos?** (algo que hayas visto, un post que publicaron, un proyecto que hicieron)\n"
            "5️⃣ **¿Qué puedes ofrecerles?** (tu experiencia, una idea, un análisis)\n\n"
            "Con eso, te escribo un mensaje corto y efectivo. Y te explico por qué funciona cada parte."
        )

    def _interview_prep_response(self) -> str:
        return (
            "Tienes una entrevista. Bien. Vamos a prepararla.\n\n"
            "La clave no está en saberse todas las respuestas técnicas del mundo. La clave "
            "está en mostrar que eres una persona que piensa, que se ha preparado y que "
            "tiene ganas.\n\n"
            "Cuéntame:\n"
            "1️⃣ ¿Qué empresa es y para qué puesto?\n"
            "2️⃣ ¿En qué fase estás? (¿primera entrevista con RRHH, técnica, con el jefe, final?)\n"
            "3️⃣ ¿Sabes cómo se llama la persona que te va a entrevistar?\n\n"
            "Y algo importante: ¿sabes qué es la 'Propuesta de 30 Días'? Es un documento "
            "de una página donde explicas qué harías tu primer mes si te contratan. "
            "Casi nadie lo hace, y por eso funciona tan bien. Si te interesa, te ayudo a hacerla."
        )

    def _emotional_block_response(self) -> str:
        return (
            'Cuéntame qué está pasando. Es normal sentirse así, de verdad.\n\n'
            'La mayoría de la gente siente algo de esto cuando piensa en "venderse" o '
            'en contactar con desconocidos:\n\n'
            '• **"Me da vergüenza"** → Como si estuvieras mendigando. Pero no es así, '
            'en realidad solo estás haciendo visible lo que sabes hacer.\n'
            '• **"No soy suficiente"** → Ese síndrome del impostor. Crees que necesitas '
            'saber mucho más antes de mostrar algo.\n'
            '• **"Ya lo intenté y no funcionó"** → Probablemente el sistema, no tú.\n'
            '• **"Me da cosa escribir a desconocidos"** → Normal, a todos nos da cosa al principio.\n\n'
            '¿Cuál de estos te resuena más? O si es otra cosa, dímelo con tus palabras.'
        )

    def _message_audit_response(self) -> str:
        return (
            "Pásame el mensaje que quieres que revise. Lo leeré y te diré qué funciona "
            "y qué se puede mejorar.\n\n"
            "Te explico cómo lo voy a evaluar:\n\n"
            "1️⃣ **¿Empieza hablando de ellos o de ti?** (mejor empezar por ellos)\n"
            "2️⃣ **¿Es específico o parece copiado?** (los mensajes genéricos no funcionan)\n"
            "3️⃣ **¿Pide demasiado al principio?** (no pidas una reunión de 30 min en el primer mensaje)\n"
            "4️⃣ **¿Muestras algo que demuestre lo que vales?** (un proyecto, un enlace)\n"
            "5️⃣ **¿Es demasiado largo?** (la gente no lee mensajes largos)\n"
            "6️⃣ **¿Termina con una pregunta clara y fácil de responder?**\n\n"
            "Pega el mensaje aquí y lo reviso. ¡Sin miedo!"
        )

    def _response_mgmt_response(self) -> str:
        return (
            "Te han respondido. Cuéntame qué pasó:\n\n"
            "• **Te dijeron que sí** 🎉 → Bien, ahora a no cagarla. Te ayudo a responder "
            "sin sonar demasiado emocionado ni demasiado frío.\n"
            "• **Te dijeron que no o que ahora no** → No pasa nada, eso es información. "
            "Hay formas de dejar la puerta abierta para el futuro.\n"
            "• **No te han respondido (ni al follow-up)** → Puede ser por muchas razones. "
            "Vamos a ver si es el mensaje, el momento o la persona.\n\n"
            "¿Cuál es tu caso?"
        )

    def _internal_opps_response(self) -> str:
        return (
            "Quieres crecer dentro de tu empresa. ¡Perfecto! Eso es más común de lo que crees "
            "y poca gente lo hace bien.\n\n"
            "¿Qué es exactamente lo que quieres?\n"
            "• ¿Un ascenso?\n"
            "• ¿Cambiar de equipo?\n"
            "• ¿Liderar un proyecto nuevo?\n"
            "• ¿Tener más visibilidad con los jefes?\n\n"
            "Y una pregunta importante: ¿tu jefe sabe que quieres esto? A veces damos por "
            "sentado que lo saben, pero no es así."
        )

    def _metrics_response(self) -> str:
        return (
            "Vale, vamos a ver cómo te está yendo. Esto es como revisar el marcador "
            "de un partido: si no miras el marcador, no sabes si estás ganando o perdiendo.\n\n"
            "Cuando estás buscando oportunidades, hay algunos números que conviene mirar:\n"
            "• ¿Cuántos mensajes has enviado esta semana?\n"
            "• ¿Cuántas personas te han respondido?\n"
            "• ¿Cuántas conversaciones se han convertido en algo concreto?\n\n"
            "Dime cómo te está yendo y te ayudo a ver dónde puedes mejorar."
        )

    def _deep_research_response(self) -> str:
        return (
            "Antes de contactar con alguien, conviene saber de quién se trata. "
            "Pero ojo, no hace falta pasarse 3 horas investigando.\n\n"
            "Con 15-20 minutos bien enfocados tienes suficiente.\n\n"
            "Dime a qué empresa o persona quieres investigar y te guío sobre "
            "dónde mirar y qué buscar. Cosas como:\n"
            "• Qué han publicado últimamente\n"
            "• Qué problemas están resolviendo\n"
            "• Cómo puedes tú ayudarles con eso"
        )

    def _email_outreach_response(self) -> str:
        return (
            "Vas a escribir un email. ¿Sabías que los emails funcionan distinto que "
            "los mensajes de LinkedIn? La gente los lee más despacio, pero también "
            "los borran más rápido si no les interesa.\n\n"
            "Cuéntame:\n"
            "1️⃣ ¿A quién le escribes? (nombre, empresa, cargo)\n"
            "2️⃣ ¿Tienes su email o necesitas ayuda para encontrarlo?\n"
            "3️⃣ ¿Qué sabes de ellos que te haya motivado a escribirles?\n"
            "4️⃣ ¿Qué puedes ofrecerles?"
        )

    def _general_help_response(self) -> str:
        return (
            "Claro, te explico. Todo esto va sobre conseguir oportunidades, "
            "ya sea trabajo, clientes, colaboraciones, o simplemente darte a conocer.\n\n"
            "Hay un método que usan las personas que lo consiguen, y no tiene nada que ver "
            "con tener suerte o ser el mejor del mundo. Tiene que ver con:\n\n"
            "1️⃣ **Saber exactamente qué quieres** (no es tan obvio como parece)\n"
            "2️⃣ **Crear contexto antes de pedir** (que la gente sepa quién eres)\n"
            "3️⃣ **Dar antes de recibir** (ofrecer valor primero)\n"
            "4️⃣ **Ser constante** (hacerlo varias veces, no solo un intento)\n\n"
            "¿Te gustaría que profundice en alguno de estos puntos? O dime "
            "qué es lo que más te interesa conseguir ahora."
        )

    def _general_response(self) -> str:
        return (
            "Cuéntame un poco más sobre ti y lo que necesitas, y te ayudo.\n\n"
            "Esto es lo que sé hacer:\n\n"
            "💼 **Buscar trabajo** — Te enseño un método que funciona distinto a lo habitual\n"
            "🎙 **Conseguir oportunidades** — Podcasts, charlas, entrevistas, proyectos freelance\n"
            "📢 **Marca personal** — Que la gente sepa quién eres y lo que haces\n"
            "✉️ **Escribir mensajes** — Para contactar con personas sin sentirte incómodo\n"
            "🎯 **Preparar entrevistas** — Con una estrategia que pocos conocen\n"
            "🧠 **Desbloquear miedos** — Si te da cosa todo esto, es normal, trabajémoslo\n"
            "🔎 **Buscar información** — Pregúntame lo que quieras y busco en internet\n\n"
            "¿Por dónde quieres empezar? O si quieres, dime directamente lo que necesitas."
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
            "\n\n---\n📝 **Por qué funciona este mensaje (explicado simple):**\n"
            "1️⃣ Empieza **hablando de ellos**, no de ti — la gente lee más si siente que va sobre ellos\n"
            "2️⃣ **Ofreces algo** antes de pedir — esto es clave, la gente está harta de que solo le pidan\n"
            "3️⃣ **Muestras pruebas** — un enlace vale más que mil palabras\n"
            "4️⃣ **Pides algo pequeño** — responder a una pregunta es fácil, pedir una reunión no\n\n"
            "⚠️ Cambia lo que está entre [corchetes] por tus datos reales. "
            "Eso es lo que hace que el mensaje funcione: que sea de verdad."
        )
        return result + notes

    def audit_message(self, message: str) -> str:
        issues = []
        score = 0

        first_word = message.split()[0].lower() if message.split() else ""
        self_refs = ["me", "mi", "yo", "soy", "quiero", "necesito", "busco"]
        starts_with_self = any(first_word == r or first_word.startswith(r) for r in self_refs)

        if starts_with_self:
            issues.append("❌ Empieza **hablando de ti**. Intenta empezar con algo de ellos (un post que publicaron, un proyecto, algo que hacen).")
        else:
            score += 1
            issues.append("✅ Empieza hablando de ellos, bien.")

        words = len(message.split())
        if words > 60:
            issues.append(f"❌ Muy largo ({words} palabras). Intenta reducirlo a 5-6 frases como máximo.")
        else:
            score += 1
            issues.append(f"✅ Longitud bien ({words} palabras).")

        generic_phrases = ["estaría encantado", "espero su respuesta", "quedo a la espera",
                          "muchas gracias de antemano", "adjunto mi cv", "para quien corresponda"]
        found_generic = [p for p in generic_phrases if p in message.lower()]
        if found_generic:
            issues.append(f"❌ Tienes frases muy genéricas: {', '.join(found_generic)}. Suenan a copia-pega.")
        else:
            score += 1
            issues.append("✅ Sin frases genéricas. Bien.")

        if "?" in message:
            score += 1
            issues.append("✅ Termina con una pregunta (bueno, la gente necesita saber qué responder).")
        else:
            issues.append("❌ No hay ninguna pregunta. El mensaje necesita terminar con algo que inviten a responder.")

        has_url = bool(re.search(r'https?://[^\s]+', message))
        if has_url:
            score += 1
            issues.append("✅ Incluyes un enlace (prueba de lo que dices).")
        else:
            issues.append("⚠️ No veo ningún enlace. Si tienes algo que mostrar (portfolio, proyecto), añádelo.")

        if "reunión" in message.lower() or "llamada" in message.lower() or "30 minutos" in message.lower():
            issues.append("❌ Estás pidiendo una reunión o llamada ya en el primer mensaje. Pide algo pequeño primero (una opinión, una respuesta rápida).")

        summary = f"\n\n📊 **Puntuación: {score}/6**\n"
        if score <= 2:
            summary += "🔴 Hay que reescribirlo casi todo. No te preocupes, te ayudo."
        elif score <= 4:
            summary += "🟡 Tiene potencial, pero hay que ajustar algunas cosas."
        else:
            summary += "🟢 Está bastante bien. Unos pequeños ajustes y queda listo."

        return "\n".join(issues) + summary

    def get_kpi_advice(self, symptom: str) -> str:
        advice_map = {
            "nadie responde": ["El mensaje no engancha o no has creado contexto antes de escribir",
                              "Prueba a comentar sus posts unos días antes de enviar el mensaje"],
            "responden pero no pasa nada": ["Falta un siguiente paso claro",
                                           "Cuando te respondan, propón algo concreto: una llamada de 15 min"],
            "conversaciones pero no cierran": ["No estás preguntando lo suficiente",
                                              "Averigua qué necesitan realmente antes de ofrecer nada"],
            "respuestas negativas": ["Puede que el target no sea el adecuado o el timing no sea el mejor"],
        }
        for key, advice in advice_map.items():
            if key in symptom.lower():
                return "Diagnóstico:\n" + "\n".join(f"• {a}" for a in advice)
        return "Cuéntame más específicamente qué está pasando para poder ayudarte."
