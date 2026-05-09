import csv

from playwright.sync_api import sync_playwright


category_url = "https://plati.market/games/"
pages_to_parse = 3


def save_to_csv(data):
    if not data:
        print("Нет данных")
        return

    keys = data[0].keys()
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print("Данные сохранены в results.csv")


def open_page(page):
    page.goto(category_url)


def parse_items(page, pages_to_parse):
    results = []

    for pg in range(pages_to_parse):
        page.wait_for_selector('a[href*="/itm/"]')

        items = page.locator('a[href*="/itm/"]')

        count = items.count()

        for i in range(count):
            item = items.nth(i)

            title = item.inner_text().strip()

            # ссылка
            link = item.get_attribute("href")
            if link:
                link = "https://plati.market" + link

            # поднимаемся к родителю (карточка)
            parent = item.locator("xpath=ancestor::div[1]")

            # цена
            price_el = parent.locator('text=₽').first
            price = price_el.inner_text() if price_el.count() > 0 else "N/A"

            results.append({
                "title": title,
                "price": price,
                "link": link
            })

        # пагинация
        next_btn = page.locator('a[rel="next"]')
        if next_btn.count() > 0:
            next_btn.click()
            page.wait_for_timeout(2000)
        else:
            print("Страницы закончились")
            break

    return results


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        open_page(page)
        data = parse_items(page, pages_to_parse)
        save_to_csv(data)

        browser.close()


if __name__ == "__main__":
    main()