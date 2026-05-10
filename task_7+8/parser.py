from playwright.sync_api import sync_playwright


def clean_text(text: str) -> str:
    return " ".join(text.split())


def extract_title(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for line in lines:
        if "₽" in line:
            continue
        if "Купить" in line:
            continue
        if "Продано" in line:
            continue
        return line

    return lines[0] if lines else ""


def extract_price(text: str) -> str:
    lines = text.split("\n")
    for line in lines:
        if "₽" in line:
            return clean_text(line)
    return "N/A"


def parse_site(category_url: str, pages_to_parse: int = 3):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(category_url, timeout=60000)

        for _ in range(pages_to_parse):
            page.wait_for_selector('a[href*="/itm/"]', timeout=10000)

            items = page.locator('a[href*="/itm/"]')

            for i in range(items.count()):
                try:
                    item = items.nth(i)

                    raw_text = item.inner_text()

                    title = extract_title(raw_text)
                    price = extract_price(raw_text)

                    link = item.get_attribute("href")
                    if link:
                        link = "https://plati.market" + link

                    results.append({
                        "title": clean_text(title),
                        "price": price,
                        "link": link
                    })

                except Exception as e:
                    print("Ошибка парсинга элемента:", e)
                    continue

            next_btn = page.locator('a[rel="next"]')

            if next_btn.count() > 0:
                next_btn.click()
                page.wait_for_load_state("domcontentloaded")
            else:
                break

        browser.close()

    return results