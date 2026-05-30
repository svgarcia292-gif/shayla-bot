"""
Main text message handler — detects user intent, maintains flow, shows typing.
"""
from telegram import Update
from telegram.ext import ContextTypes
from database.db import save_message, get_user_context, set_user_context
from skills.prospector import ProspectorEngine
from services.search_service import search_web, format_search_results

engine = ProspectorEngine()

EXIT_KEYWORDS = ["nada", "eso es todo", "gracias", "bye", "chao", "adiós", "terminamos"]

FLOW_KEYWORDS = {
    "job_search": ["trabajo", "empleo", "busco trabajo", "cv", "contratar", "puesto"],
    "opportunity": ["podcast", "charla", "evento", "freelance", "cliente", "oportunidad"],
    "personal_brand": ["linkedin", "marca personal", "contenido", "publicar"],
    "message_gen": ["mensaje", "escribir", "contactar", "redactar"],
    "interview_prep": ["entrevista", "preparar"],
    "emotional_block": ["miedo", "vergüenza", "bloqueo", "inseguro"],
    "message_audit": ["auditar", "revisa"],
    "response_mgmt": ["respondieron", "respondió", "silencio"],
    "internal_opps": ["ascenso", "promoción", "cambio"],
    "metrics": ["métrica", "kpi", "cómo voy"],
    "deep_research": ["investigar", "research"],
}

async def send_typing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import asyncio
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    await asyncio.sleep(0.5)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = None):
    user_id = update.effective_user.id
    if text is None:
        text = update.message.text.strip()

    await save_message(user_id, "user", text)

    user_context = await get_user_context(user_id)
    current_flow = user_context.get("current_flow", "")

    lower = text.lower()

    is_exit = any(kw in lower for kw in EXIT_KEYWORDS)
    if is_exit:
        await set_user_context(user_id, current_flow="")
        await send_typing(update, context)
        await update.message.reply_text("OK, cuando necesites algo más, aquí estoy.")
        return

    stays_in_flow = False
    if current_flow and current_flow in FLOW_KEYWORDS:
        stays_in_flow = any(kw in lower for kw in FLOW_KEYWORDS[current_flow])

    new_flow = engine.detect_flow(text)

    if current_flow and new_flow in ("general", "general_help", "onboarding"):
        flow = current_flow
    elif current_flow and new_flow != current_flow and new_flow != "general":
        flow = new_flow
    else:
        flow = new_flow

    if flow == "general" and current_flow:
        flow = current_flow

    if flow in ("general", "onboarding"):
        for intent, keywords in FLOW_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                flow = intent
                break

    await set_user_context(user_id, current_flow=flow)

    if flow == "web_search":
        await handle_web_search(update, context, text)
        return

    if flow == "message_audit" and len(text) > 20:
        await handle_audit_request(update, context, text)
        return

    response = engine.get_flow_response(flow, user_context)
    await save_message(user_id, "assistant", response, flow)

    await send_typing(update, context)
    await update.message.reply_text(response, parse_mode="Markdown")

async def handle_web_search(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    query = text
    for prefix in ["busca", "buscar", "internet", "google", "investiga", "dime sobre", "qué sabes de"]:
        if text.lower().startswith(prefix):
            query = text[len(prefix):].strip()
            break
    if not query:
        await send_typing(update, context)
        await update.message.reply_text("¿Qué quieres que busque?")
        return

    results = await search_web(query)
    formatted = format_search_results(results)
    await save_message(update.effective_user.id, "assistant", f"Búsqueda: {query[:100]}", "web_search")

    msg = f"🔎 {query}\n\n{formatted}" if results and not results[0].get("error") else formatted
    await update.message.reply_text(msg, disable_web_page_preview=True)

async def handle_audit_request(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    clean = text
    for prefix in ["audita", "auditar", "revisa esto", "revisa este mensaje", "qué opinas de este"]:
        if text.lower().startswith(prefix):
            clean = text[len(prefix):].strip()
            break
    if not clean or len(clean) < 10:
        await send_typing(update, context)
        await update.message.reply_text("Pega el mensaje completo.")
        return

    result = engine.audit_message(clean)
    await save_message(update.effective_user.id, "assistant", result, "message_audit")
    await send_typing(update, context)
    await update.message.reply_text(result, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    await handle_text_message(update, context)
