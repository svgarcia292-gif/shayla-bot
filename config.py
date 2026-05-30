import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "ShaylaBot")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
AUDIO_MAX_DURATION = int(os.getenv("AUDIO_MAX_DURATION", "120"))

DATABASE_PATH = os.getenv("DATABASE_PATH", "data/shayla.db")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "data/shayla.log")
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", str(5 * 1024 * 1024)))
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "3"))

ALLOWED_USERS = os.getenv("ALLOWED_USERS", "")
if ALLOWED_USERS:
    ALLOWED_USERS = [int(u.strip()) for u in ALLOWED_USERS.split(",")]
else:
    ALLOWED_USERS = []

WEB_SEARCH_ENABLED = os.getenv("WEB_SEARCH_ENABLED", "true").lower() == "true"
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
