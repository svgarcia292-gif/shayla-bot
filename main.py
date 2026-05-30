"""
Shayla — Bot de Telegram para prospección profesional.
"""
import asyncio
import sys
import os
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

import config
from utils.logger import logger
from database.db import set_db_path, init_db
from services.whisper_service import load_model
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from handlers.commands import start, help_command, reset, search_command, audit_command, error_handler
from handlers.audio import handle_audio
from handlers.message import handle_message

def run_healthcheck():
    import http.server
    class HC(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
        def log_message(self, *a): pass
    port = int(os.getenv("PORT", "8000"))
    server = http.server.HTTPServer(("0.0.0.0", port), HC)
    logger.info(f"Healthcheck on port {port}")
    server.serve_forever()

async def main():
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN no configurado")
        sys.exit(1)

    set_db_path(config.DATABASE_PATH)
    await init_db()

    if config.WHISPER_MODEL:
        await load_model(config.WHISPER_MODEL)

    app = (
        Application.builder()
        .token(config.BOT_TOKEN)
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

    t = threading.Thread(target=run_healthcheck, daemon=True)
    t.start()

    logger.info("Shayla started")
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
    except Exception as e:
        logger.critical(f"Fatal: {e}")
        sys.exit(1)
