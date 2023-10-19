import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

proxies = {"https": "149.62.183.209:3128"}


def get_location(url_proxies):
    response = requests.get(url=url_proxies, headers=headers)
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

    links = soup.find_all('a', class_='Link ListingItemTitle-module__link')
    print(links)

    # Выводим ссылки на автомобили
    for link in links:
        print(link['href'])


def main():
    url = "https://auto.ru/samarskaya_oblast/cars/all/?utm_source=yandex_direct&utm_medium=direct.brand&utm_campaign=hand_desktop_used_brand_search_samara_zapad-none_81682365&utm_content=cid%3A81682365%7Cgid%3A5103467700%7Caid%3A13249852988%7Cph%3A42630146793%7Cpt%3Apremium%7Cpn%3A1%7Csrc%3Anone%7Cst%3Asearch%7Ccgcid%3A14512433%7Cdt%3Adesktop&utm_term=auto+ru&adjust_t=cl4qttt_nsw4it6&adjust_campaign=81682365&adjust_adgroup=5103467700&tracker_limit=10000&yclid=11119579560045182975&utm_referrer=yandex.ru"
    get_location(url_proxies="https://2ip.ru")
    parsing(url)


if __name__ == "__main__":
    main()
