"""
Handler for voice messages.
"""
from telegram import Update
from telegram.ext import ContextTypes
import config
from services.whisper_service import transcribe_file
from handlers.message import handle_text_message

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice

    if voice.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("Audio muy pesado (>20MB). Intenta con uno más corto.")
        return
    max_dur = getattr(config, "AUDIO_MAX_DURATION", 120)
    if voice.duration > max_dur:
        await update.message.reply_text(f"Audio muy largo (>{max_dur}s). Escríbelo mejor.")
        return

    processing_msg = await update.message.reply_text("🎤 Escuchando...")

    try:
        file = await context.bot.get_file(voice.file_id)
        file_bytes = await file.download_as_bytearray()
        result = await transcribe_file(bytes(file_bytes))

        if result.get("error") or not result.get("text"):
            await processing_msg.edit_text("No entendí el audio. ¿Puedes escribirlo?")
            return

        await processing_msg.delete()
        await handle_text_message(update, context, result["text"])
    except Exception:
        try:
            await processing_msg.edit_text("Error procesando el audio.")
        except Exception:
            pass
