import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

proxies = {"https": "149.62.183.209:3128"}


def get_location(url_proxies):
    response = requests.get(url=url_proxies, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")

    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()

    print(f"IP: {ip}\nLocation: {location}")


def parsing(url):
    response = requests.get(url)
    print(response)

    if response.status_code != 200:
        print("Ошибка при получении страницы")
        exit()

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)

   # Находим все теги <a> с классом `item-description-title-link`
    links = soup.find_all('a', class_='item-description-title-link')

# Выводим ссылки на товары
    for link in links:
        print(link['href'])


def main():
    url = "https://www.avito.ru/"
    get_location(url_proxies="https://2ip.ru")
    parsing(url)


if __name__ == "__main__":
    main()
