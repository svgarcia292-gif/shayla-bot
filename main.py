"""
Shayla — Bot de Telegram para prospección profesional.
Integra Hot Outreach, Creator Vision Framework, Método Lanzamiento y Principio 1.2x.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()

import config
from utils.logger import logger
from database.db import set_db_path, init_db
from services.whisper_service import load_model
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters
)

from handlers.commands import start, help_command, reset, search_command, audit_command, error_handler
from handlers.audio import handle_audio
from handlers.message import handle_message

async def post_init(app: Application):
    logger.info("Shayla bot initialized successfully")

async def main():
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables. Create a .env file with BOT_TOKEN=your_token")
        print("ERROR: BOT_TOKEN no configurado. Crea un archivo .env con BOT_TOKEN=tu_token")
        sys.exit(1)

    set_db_path(config.DATABASE_PATH)
    await init_db()

    if config.WHISPER_MODEL:
        logger.info(f"Loading Whisper model: {config.WHISPER_MODEL}")
        model_loaded = await load_model(config.WHISPER_MODEL)
        if model_loaded:
            logger.info("Audio transcription enabled")
        else:
            logger.warning("Audio transcription unavailable")

    app = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("audit", audit_command))

    app.add_handler(MessageHandler(filters.VOICE, handle_audio))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error_handler)

    logger.info("Shayla bot started polling...")
    print("🤖 Shayla bot is running. Press Ctrl+C to stop.")

    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shayla bot stopped by user")
        print("\n👋 Shayla bot stopped.")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
