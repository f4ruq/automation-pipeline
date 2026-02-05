from bs4 import BeautifulSoup

def parse(html, field_map, container_selector="div.job"):
    if isinstance(html, list):
        jobs = []
        for entry in html:
            # Skip legal/metadata entries that might not have required fields if needed
            # But RemoteOK JSON is usually clean.
            item = {}
            for field, key in field_map.items():
                item[field] = entry.get(key)
            jobs.append(item)
        return jobs

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    containers = soup.select(container_selector)

    for c in containers:
        item = {}
        for field, selector in field_map.items():
            if "::attr(" in selector:
                sel, attr = selector.split("::attr(")
                attr = attr.replace(")", "")
                el = c.select_one(sel)
                item[field] = el.get(attr) if el else None
            else:
                el = c.select_one(selector)
                item[field] = el.text.strip() if el else None

        jobs.append(item)

    return jobs
