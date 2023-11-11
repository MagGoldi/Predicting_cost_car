import os
import csv

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


def get_car_data(car_url):
    driver.get(car_url)
    # print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    title = soup.find_all("a", class_="breadcrumbs-link-Vr4Nc")
    all_info = soup.find_all("li", class_="params-paramsList__item-appQw")
    price = soup.find("span", {"itemprop": "price"}).text

    info_tmp = []

    for n in title:
        info_tmp.append(n.text)
        print(info_tmp[4])
    for n in all_info:
        print(n.text)
    print(price)


def main():
    url_proxies = "https://2ip.ru"
    car_url = "https://www.avito.ru/tolyatti/avtomobili/audi_a4_1.8_cvt_2013_191_029_km_3471263326"

    get_location(url_proxies)

    # Получение данных об автомобиле
    car_data = get_car_data(car_url)

    driver.quit()


if __name__ == "__main__":
    main()
