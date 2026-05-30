"""
Command handlers for Shayla bot.
"""
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from database.db import save_message, clear_conversation, get_or_create_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await get_or_create_user(
        user.id, user.username, user.first_name, user.last_name
    )
    await save_message(user.id, "system", "Usuario inició conversación", "onboarding")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    import asyncio
    await asyncio.sleep(0.5)

    welcome = (
        f"Hola {user.first_name} ✨ Soy Shayla.\n\n"
        "💼 Buscar trabajo\n"
        "🎙 Una oportunidad (podcast, charla, proyecto)\n"
        "📢 Marca personal / LinkedIn\n"
        "✉️ Escribir un mensaje\n"
        "🎯 Preparar entrevista\n"
        "🔎 Buscar en internet\n\n"
        "¿Qué necesitas?"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    import asyncio
    await asyncio.sleep(0.3)

    help_text = (
        "/start — Iniciar\n"
        "/reset — Empezar de nuevo\n"
        "/search [consulta] — Buscar en internet\n"
        "/audit [mensaje] — Revisar un mensaje\n\n"
        "También puedes enviarme audios."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await clear_conversation(user_id)
    await update.message.reply_text(
        "Historial limpiado. Empezamos de nuevo.\n\n¿Qué necesitas?"
    )

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text(
            "¿Qué quieres que busque? Ejemplo: /search oportunidades laborales IA 2026"
        )
        return

    await update.message.reply_text(f"🔎 Buscando: *{query}*...", parse_mode="Markdown")

    from services.search_service import search_web, format_search_results
    results = await search_web(query)
    formatted = format_search_results(results)
    await update.message.reply_text(formatted, parse_mode="Markdown", disable_web_page_preview=True)

async def audit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = " ".join(context.args)
    if not message_text:
        await update.message.reply_text(
            "Pega el mensaje después del comando. Ejemplo:\n/audit Hola, soy ingeniero y busco trabajo..."
        )
        return

    from skills.prospector import ProspectorEngine
    engine = ProspectorEngine()
    audit_result = engine.audit_message(message_text)
    response = f"**Auditoría de mensaje:**\n\n{audit_result}"
    await update.message.reply_text(response, parse_mode="Markdown")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Ocurrió un error inesperado. Si persiste, usa /reset para reiniciar."
            )
    except Exception:
        pass
