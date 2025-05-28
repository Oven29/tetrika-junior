import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import Tuple
import csv


BASE_URL = "https://ru.wikipedia.org/w/index.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0; +https://example.com/bot)"
}

RUSSIAN_ALPHABET = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ")


async def fetch(session: aiohttp.ClientSession, params: dict) -> str:
    """
    Возвращает HTML-код страницы
    """
    async with session.get(BASE_URL, headers=HEADERS, params=params) as response:
        response.raise_for_status()
        return await response.text()


async def get_count_animals_for_letter(session: aiohttp.ClientSession, letter: str) -> Tuple[str, int]:
    """
    Возвращает количество животных в категории "Категория:Животные_по_алфавиту" по букве
    """
    params = {"from": letter, "title": "Категория:Животные_по_алфавиту"}
    count = 0

    while True:
        html = await fetch(session, params)
        soup = BeautifulSoup(html, "lxml")

        letter_header = soup.select_one("#mw-pages > div.mw-content-ltr > div > div:nth-child(1) > h3")
        if not letter_header or letter_header.text.strip() != letter:
            count += 1
            break

        list_animals = soup.select("#mw-pages > div.mw-content-ltr > div > div:nth-child(1) > ul > li")
        count += len(list_animals) - 1
        if len(list_animals) < 200:
            count += 1
            break

        last_title = list_animals[-1].select_one("a").attrs["title"]
        params["pagefrom"] = last_title

    return letter, count


async def main():
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [get_count_animals_for_letter(session, letter) for letter in RUSSIAN_ALPHABET]
        for coro in asyncio.as_completed(tasks):
            letter, count = await coro
            results.append((letter, count))

    results.sort(key=lambda x: RUSSIAN_ALPHABET.index(x[0]))

    with open("result.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for letter, cnt in results:
            writer.writerow([letter, cnt])


if __name__ == "__main__":
    asyncio.run(main())
