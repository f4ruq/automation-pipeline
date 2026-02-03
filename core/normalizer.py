from datetime import datetime

def normalize(items, source_name):
    normalized = []
    for item in items:
        item["source"] = source_name
        item["scraped_at"] = datetime.utcnow().isoformat()
        normalized.append(item)
    return normalized