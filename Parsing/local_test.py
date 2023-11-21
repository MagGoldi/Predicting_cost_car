from random import uniform
from bs4 import BeautifulSoup
from selenium import webdriver


driver = webdriver.Chrome()


def get_soup(url):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def get_location(url_proxies):
    driver.get(url_proxies)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()
    print(f"IP: {ip}\nLocation: {location}")


url_proxies = "https://2ip.ru"
get_location(url_proxies)
links = [
    "https://www.avito.ru/samara/avtomobili/toyota_rav4_2.0_mt_2020_50_000_km_3272058958",
    "https://www.avito.ru/samara/avtomobili/toyota_rav4_2.0_mt_2020_50_000_km_3272058958",
    "https://www.avito.ru/samara/avtomobili/toyota_rav4_2.0_mt_2020_50_000_km_3272058958",
    "https://www.avito.ru/samara/avtomobili/toyota_rav4_2.0_mt_2020_50_000_km_3272058958",
]
for l in links:
    driver.get(l)
    driver.get(l)
    soup = get_soup(l)
    uniform(3, 4)
    driver.quit()
