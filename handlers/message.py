"""
Main text message handler — detects user intent and routes to the right flow.
"""
from telegram import Update
from telegram.ext import ContextTypes
from database.db import (
    save_message, get_user_context, set_user_context
)
from skills.prospector import ProspectorEngine
from services.search_service import search_web, format_search_results

engine = ProspectorEngine()

FLOW_LABELS = {
    "onboarding": "Onboarding",
    "job_search": "Búsqueda de trabajo",
    "opportunity": "Oportunidades",
    "personal_brand": "Marca personal",
    "message_gen": "Generación de mensajes",
    "interview_prep": "Preparación de entrevista",
    "emotional_block": "Desbloqueo emocional",
    "message_audit": "Auditoría de mensajes",
    "response_mgmt": "Gestión de respuestas",
    "internal_opps": "Oportunidades internas",
    "metrics": "Métricas",
    "deep_research": "Investigación",
    "email_outreach": "Email outreach",
    "general_help": "Ayuda general",
    "web_search": "Búsqueda web",
    "general": "General"
}

FLOW_EMOJIS = {
    "onboarding": "👋",
    "job_search": "💼",
    "opportunity": "🎙",
    "personal_brand": "📢",
    "message_gen": "✉️",
    "interview_prep": "🎯",
    "emotional_block": "🧠",
    "message_audit": "📊",
    "response_mgmt": "💬",
    "internal_opps": "🏢",
    "metrics": "📈",
    "deep_research": "🔍",
    "email_outreach": "📧",
    "general_help": "❓",
    "web_search": "🔎",
    "general": "💡"
}

EXPLICIT_FLOW_TRIGGERS = {
    "buscar trabajo": "job_search",
    "quiero trabajo": "job_search",
    "busco empleo": "job_search",
    "marca personal": "personal_brand",
    "crear contenido": "personal_brand",
    "linkedin": "personal_brand",
    "preparar entrevista": "interview_prep",
    "tengo entrevista": "interview_prep",
    "mensaje": "message_gen",
    "escribir a": "message_gen",
    "miedo": "emotional_block",
    "vergüenza": "emotional_block",
    "bloqueado": "emotional_block",
    "no sé venderme": "emotional_block",
    "auditar": "message_audit",
    "revisa esto": "message_audit",
    "respondieron": "response_mgmt",
    "me respondió": "response_mgmt",
    "ascenso": "internal_opps",
    "promoción": "internal_opps",
    "métricas": "metrics",
    "kpi": "metrics",
    "investigar empresa": "deep_research",
    "investigar persona": "deep_research",
    "email": "email_outreach",
    "correo": "email_outreach",
    "podcast": "opportunity",
    "charla": "opportunity",
    "evento": "opportunity",
    "cliente": "opportunity",
    "freelance": "opportunity",
    "ayuda": "general_help",
    "qué hago": "general_help",
    "no sé cómo": "general_help",
}

async def handle_text_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str = None
):
    user_id = update.effective_user.id

    if text is None:
        text = update.message.text.strip()

    await save_message(user_id, "user", text)

    user_context = await get_user_context(user_id)

    lower_text = text.lower()

    flow = engine.detect_flow(text)

    if flow == "general" and user_context.get("current_flow"):
        flow = user_context["current_flow"]

    if flow == "onboarding" or flow == "general":
        for trigger, mapped_flow in EXPLICIT_FLOW_TRIGGERS.items():
            if trigger in lower_text:
                flow = mapped_flow
                break

    await set_user_context(user_id, current_flow=flow)

    if flow == "web_search":
        await handle_web_search(update, context, text)
        return

    if flow == "message_audit":
        await handle_audit_request(update, context, text)
        return

    if context.args and context.args[0:1] == ["--search"]:
        query = " ".join(context.args[1:]) if len(context.args) > 1 else text
        await handle_web_search(update, context, query)
        return

    response = engine.get_flow_response(flow, user_context)

    flow_label = FLOW_LABELS.get(flow, "General")
    flow_emoji = FLOW_EMOJIS.get(flow, "💡")
    header = f"{flow_emoji} **{flow_label}**\n\n"

    await save_message(user_id, "assistant", response, flow)

    await update.message.reply_text(
        header + response,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def handle_web_search(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    query = text
    for prefix in ["busca", "buscar", "internet", "google", "investiga", "dime sobre",
                    "qué sabes de", "búscame", "búscame en internet", "busca en internet"]:
        if text.lower().startswith(prefix):
            query = text[len(prefix):].strip()
            break

    if not query:
        await update.message.reply_text("¿Qué quieres que busque en internet?")
        return

    await update.message.reply_text(f"🔎 Buscando *{query}*...", parse_mode="Markdown")

    results = await search_web(query)
    formatted = format_search_results(results)

    await save_message(update.effective_user.id, "assistant",
                       f"Resultados de búsqueda: {query[:100]}", "web_search")

    await update.message.reply_text(
        f"🔎 **Resultados para:** _{query}_\n\n{formatted}",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def handle_audit_request(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    clean_text = text
    for prefix in ["audita", "auditar", "revisa esto", "revisa este mensaje",
                    "qué opinas de este mensaje", "analiza este mensaje"]:
        if text.lower().startswith(prefix):
            clean_text = text[len(prefix):].strip()
            break

    if not clean_text or len(clean_text) < 10:
        await update.message.reply_text(
            "Pega el mensaje completo que quieres que audite."
        )
        return

    audit_result = engine.audit_message(clean_text)
    response = f"📊 **Auditoría de mensaje:**\n\n{audit_result}"

    await save_message(update.effective_user.id, "assistant", response, "message_audit")
    await update.message.reply_text(response, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    await handle_text_message(update, context)
