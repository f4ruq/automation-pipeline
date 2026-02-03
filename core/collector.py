from pathlib import Path

def collect(source_config):
    if source_config["type"] == "local_html":
        path = Path(source_config["path"])
        return path.read_text(encoding="utf-8")

    raise ValueError("Unsupported source type")