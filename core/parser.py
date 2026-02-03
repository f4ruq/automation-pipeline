from bs4 import BeautifulSoup

def parse(html, field_map):
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    containers = soup.find_all("div", class_="job")

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