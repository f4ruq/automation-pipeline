from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/last_run.log")


def log(message, level="INFO"):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().isoformat()
    line = f"[{timestamp}] [{level}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)