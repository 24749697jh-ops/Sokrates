from __future__ import annotations

import os

APP_TITLE = "Sokrates"
APP_ICON = "🧭"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
MAX_FILE_SIZE_MB = 20
SUPPORTED_TYPES = ["pdf", "png", "jpg", "jpeg", "webp", "docx", "txt"]
