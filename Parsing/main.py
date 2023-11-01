import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


driver = webdriver.Chrome()


def get_location(url_proxies):
    driver.get(url_proxies)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()

    print(f"IP: {ip}\nLocation: {location}")


def parsing(url):
    driver.get(url)
    # print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    meta_tags = soup.find_all("meta", {"itemprop": "price"})
    price_values = [meta["content"] for meta in meta_tags]

    for price in price_values:
        print(price)


def main():
    url = "https://www.avito.ru/samara/avtomobili/s_probegom/audi-ASgBAQICAUSGFMjmAQFA4LYNFN6XKA?cd=1&f=ASgBAQICAkSGFMjmAfrwD~i79wIBQOC2DRTelyg&radius=200&searchRadius=200"
    url_proxies = "https://2ip.ru"

    get_location(url_proxies)
    parsing(url)

    driver.quit()


if __name__ == "__main__":
    main()
