import hashlib

def deduplicate(items):
    seen = set()
    unique = []

    for item in items:
        key = (item.get("title"), item.get("company"), item.get("url"))
        h = hashlib.sha256(str(key).encode()).hexdigest()
        item["id"] = h

        if h not in seen:
            seen.add(h)
            unique.append(item)

    return unique