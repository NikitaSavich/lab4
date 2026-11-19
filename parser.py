import os
import re
import csv
import time
import argparse
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def get_html(url_name, cache_dir="cache"):
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    cache_file = os.path.join(cache_dir, f"{url_name}.html")

    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read(), True

    url = f"https://en.wikipedia.org/wiki/{url_name}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"Ошибка загрузки {url_name}: статус {resp.status_code}")
            return None, False

        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(resp.text)
        return resp.text, False

    except requests.RequestException as e:
        print(f"Не удалось подключиться к {url_name}: {e}")
        return None, False


def parse_number(text):
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\(.*?\)", "", text)

    raw_nums = re.findall(r"\d[\d,\s]*", text)
    nums = []
    for item in raw_nums:
        clean = re.sub(r"\D", "", item)
        if clean:
            nums.append(clean)

    if not nums:
        return ""
    return max(nums, key=int)


def parse_infobox(html, country):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="infobox")

    if not table:
        print(f"Карточка infobox не найдена для: {country}")
        return "", "", ""

    city = ""
    area = ""
    population = ""

    rows = table.find_all("tr")
    for i, row in enumerate(rows):
        th = row.find("th")
        if not th:
            continue

        header = th.get_text(" ", strip=True).lower()

        if "capital" in header and not city:
            td = row.find("td")
            if td:
                for sup in td.find_all("sup"):
                    sup.decompose()
                a_tag = td.find("a")
                if a_tag and a_tag.get_text(strip=True):
                    city = a_tag.get_text(strip=True)
                else:
                    city = td.get_text(" ", strip=True).split("°")[0].strip()

        elif (header == "area" or header.startswith("area ")) and not area:
            td = row.find("td")
            if td and re.search(r"\d", td.get_text()):
                area = parse_number(td.get_text())
            else:
                for next_row in rows[i + 1:i + 5]:
                    sub_th = next_row.find("th")
                    sub_td = next_row.find("td")
                    if sub_th and sub_td and "total" in sub_th.get_text().lower():
                        area = parse_number(sub_td.get_text())
                        break

        elif (header == "population" or header.startswith("population ")) and not population:
            td = row.find("td")
            if td and re.search(r"\d", td.get_text()):
                population = parse_number(td.get_text())
            else:
                for next_row in rows[i + 1:i + 5]:
                    sub_td = next_row.find("td")
                    if sub_td and re.search(r"\d", sub_td.get_text()):
                        population = parse_number(sub_td.get_text())
                        break

    return city, area, population


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="countries.txt")
    parser.add_argument("--output", default="countries_data.csv")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Файл {args.input} не найден")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        countries = [line.strip() for line in f if line.strip()]

    data = []

    for country in countries:
        url_name = country.replace(" ", "_")
        html, from_cache = get_html(url_name)

        if html is None:
            data.append([country, "", "", ""])
        else:
            city, area, population = parse_infobox(html, country)
            data.append([country, city, area, population])
            print(f"{country}: {city} | {area} | {population}")

        if not from_cache:
            time.sleep(1)

    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["country", "city", "area", "population"])
        writer.writerows(data)

    print(f"Готово, результат в {args.output}")


if __name__ == "__main__":
    main()