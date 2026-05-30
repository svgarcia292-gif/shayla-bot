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

    welcome = (
        f"Hola {user.first_name} 👋 Soy **Shayla**, tu mentora de prospección.\n\n"
        "Estoy aquí para ayudarte a conseguir lo que quieres:\n"
        "• 💼 **Buscar trabajo** con un sistema que funciona\n"
        "• 🎙 **Conseguir oportunidades** (podcasts, charlas, reuniones)\n"
        "• 📢 **Construir tu marca personal**\n"
        "• ✉️ **Generar mensajes** que obtienen respuesta\n"
        "• 🎯 **Preparar entrevistas** con ventaja 1.2x\n"
        "• 🧠 **Desbloqueos emocionales**\n"
        "• 🔎 **Buscar en internet** información actualizada\n\n"
        "¿Qué necesitas hoy? Cuéntame y empezamos."
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "**Comandos disponibles:**\n\n"
        "/start — Iniciar / reiniciar conversación\n"
        "/help — Mostrar esta ayuda\n"
        "/reset — Limpiar historial y empezar de nuevo\n"
        "/new — Nueva oportunidad en tu pipeline\n"
        "/search [consulta] — Buscar en internet directamente\n"
        "/audit [mensaje] — Auditar un mensaje de outreach\n\n"
        "También puedes **enviarme audios** y los transcribo para entenderte.\n\n"
        "Solo dime qué necesitas y te guío."
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
