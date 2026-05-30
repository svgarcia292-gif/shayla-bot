"""
Handler for voice messages. Downloads audio, transcribes with Whisper, then processes as text.
"""
import os
from telegram import Update
from telegram.ext import ContextTypes
from utils.logger import logger
from database.db import save_message
from services.whisper_service import transcribe_file
from handlers.message import handle_text_message

MAX_AUDIO_SIZE = 20 * 1024 * 1024

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    voice = update.message.voice

    if voice.file_size > MAX_AUDIO_SIZE:
        await update.message.reply_text(
            "El audio es demasiado grande (>20MB). Intenta con un mensaje más corto."
        )
        return

    duration = voice.duration
    if duration > 120:
        await update.message.reply_text(
            "El audio es muy largo (>2 minutos). ¿Puedes resumirlo o escribir el mensaje?"
        )
        return

    processing_msg = await update.message.reply_text(
        "🎤 Escuchando tu audio..."
    )

    try:
        file = await context.bot.get_file(voice.file_id)
        file_bytes = await file.download_as_bytearray()

        result = await transcribe_file(bytes(file_bytes), f"audio_{user_id}.ogg")

        if result.get("error"):
            await processing_msg.edit_text(
                f"No pude transcribir el audio: {result['error']}\n\n¿Puedes escribirme el mensaje?"
            )
            return

        transcribed_text = result.get("text", "")
        if not transcribed_text:
            await processing_msg.edit_text(
                "No entendí el audio. ¿Puedes intentar de nuevo o escribirme?"
            )
            return

        await processing_msg.edit_text(
            f"📝 He entendido esto:\n\n_{transcribed_text}_\n\nDame un momento..."
        )

        await save_message(user_id, "user", transcribed_text, "audio")

        await handle_text_message(update, context, transcribed_text)

    except Exception as e:
        logger.error(f"Audio processing error: {e}")
        await processing_msg.edit_text(
            "Hubo un error procesando el audio. ¿Puedes escribirme directamente?"
        )
