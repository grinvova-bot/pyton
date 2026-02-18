import requests
from bs4 import BeautifulSoup
import pycountry
from urllib.parse import urljoin
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Получаем русские названия стран
all_countries = list(pycountry.countries)
russian_country_names = []
for country in all_countries:
    try:
        russian_name = country.name.translate({ord(c): None for c in "()"})
        russian_country_names.append(russian_name.lower())
    except:
        pass

# Исключаем Россию
russian_country_names = [name for name in russian_country_names if name != "россия"]

# Начальный URL
base_url = "https://alt-x.ru"
visited = set()
results = []

def is_valid_url(url):
    return url.startswith(base_url) and url not in visited

def find_country_mentions(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        found_countries = set()
        for country in russian_country_names:
            if country in text:
                found_countries.add(country)

        return list(found_countries)
    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")
        return []

def crawl(url):
    if url in visited:
        return
    visited.add(url)
    print(f"Обхожу: {url}")

    found_countries = find_country_mentions(url)
    if found_countries:
        results.append((url, found_countries))
        print(f"Найдены упоминания на {url}: {', '.join(found_countries)}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(base_url, link['href'])
            if is_valid_url(absolute_url):
                time.sleep(1)  # Задержка
                crawl(absolute_url)
    except Exception as e:
        print(f"Ошибка при обходе {url}: {e}")

# Запускаем обход
crawl(base_url)

# Выводим результаты
print("\n--- Результаты ---")
for url, found_countries in results:
    print(f"Страница: {url}")
    print(f"Страны: {', '.join(found_countries)}\n")
