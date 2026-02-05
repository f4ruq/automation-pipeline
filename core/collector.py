from pathlib import Path

def collect(source_config):
    if source_config["type"] == "local_html":
        path = Path(source_config["path"])
        return path.read_text(encoding="utf-8")

    if source_config["type"] == "remote_html":
        import requests
        headers = source_config.get("headers", {})
        response = requests.get(source_config["url"], headers=headers, timeout=10)
        response.raise_for_status()
        return response.text

    if source_config["type"] == "remote_json":
        import requests
        headers = source_config.get("headers", {})
        response = requests.get(source_config["url"], headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    raise ValueError("Unsupported source type")
