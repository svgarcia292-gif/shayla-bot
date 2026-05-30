"""
OpenAI Whisper service for transcribing voice messages.
Runs locally with configurable model size.
"""
import os
import tempfile
import asyncio
from pathlib import Path
from utils.logger import logger

WHISPER_AVAILABLE = False
WHISPER_MODEL = None

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    logger.warning("openai-whisper not installed. Audio transcription will be disabled.")

async def load_model(model_name: str = "base"):
    global WHISPER_MODEL
    if not WHISPER_AVAILABLE:
        logger.error("Whisper not available. Cannot load model.")
        return False
    try:
        logger.info(f"Loading Whisper model '{model_name}'...")
        loop = asyncio.get_event_loop()
        WHISPER_MODEL = await loop.run_in_executor(
            None, whisper.load_model, model_name
        )
        logger.info(f"Whisper model '{model_name}' loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load Whisper model: {e}")
        return False

async def transcribe(audio_file_path: str, language: str = "es") -> dict:
    if not WHISPER_AVAILABLE or WHISPER_MODEL is None:
        return {"text": "", "error": "Whisper no está disponible. El modelo no se ha cargado."}

    if not os.path.exists(audio_file_path):
        return {"text": "", "error": "El archivo de audio no existe."}

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: WHISPER_MODEL.transcribe(
                audio_file_path,
                language=language,
                task="transcribe",
                fp16=False
            )
        )
        logger.info(f"Audio transcribed: {len(result.get('text', ''))} chars")
        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language", language),
            "segments": result.get("segments", []),
            "error": None
        }
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return {"text": "", "error": f"Error transcribiendo audio: {str(e)}"}

async def transcribe_file(file_bytes: bytes, filename: str = "audio.ogg") -> dict:
    tmp_dir = Path(tempfile.gettempdir()) / "shayla_audio"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    tmp_path = tmp_dir / filename
    try:
        with open(tmp_path, "wb") as f:
            f.write(file_bytes)

        result = await transcribe(str(tmp_path))
        return result
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return {"text": "", "error": str(e)}
    finally:
        try:
            os.remove(str(tmp_path))
        except OSError:
            pass
