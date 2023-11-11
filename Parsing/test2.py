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

    car_info = {
        "Год выпуска": None,
        "Поколение": None,
        "Пробег": None,
        "Владельцев по ПТС": None,
        "Состояние": None,
        "Модификация": None,
        "Объём двигателя": None,
        "Тип двигателя": None,
        "Коробка передач": None,
        "Привод": None,
        "Комплектация": None,
        "Тип кузова": None,
        "Цвет": None,
        "Руль": None,
        "Обмен": None,
    }

    # Находим марку и модель
    title = soup.find_all("span", {"itemprop": "name"})

    car_info["Марка"] = title[4].text
    car_info["Модель"] = title[5].text

    price = soup.find("span", {"itemprop": "price"}).text
    car_info["Цена"] = "".join(price.split("#\xa0"))  # ????

    details = soup.find_all("li", class_="params-paramsList__item-appQw")

    for detail in details:
        if "Год выпуска" in detail.text:
            car_info["Год выпуска"] = detail.text.split()[-1]
            continue
        elif "Поколение" in detail.text:
            car_info["Поколение"] = detail.text.split()[-2]
            continue
        elif "Пробег" in detail.text:
            car_info["Пробег"] = detail.text.split()[-2]
            continue
        elif "Владельцев по ПТС" in detail.text:
            car_info["Владельцев по ПТС"] = detail.text.split()[-1]
            continue
        elif "Состояние" in detail.text:
            car_info["Состояние"] = detail.text.split(":")[-1]
            continue
        elif "Модификация" in detail.text:
            car_info["Модификация"] = detail.text.split(":")[-1]
            continue
        elif "Объём двигателя" in detail.text:
            car_info["Объём двигателя"] = detail.text.split()[-2]
            continue
        elif "Тип двигателя" in detail.text:
            car_info["Тип двигателя"] = detail.text.split()[-1]
            continue
        elif "Коробка передач" in detail.text:
            car_info["Коробка передач"] = detail.text.split()[-1]
            continue
        elif "Привод" in detail.text:
            car_info["Привод"] = detail.text.split()[-1]
            continue
        elif "Комплектация" in detail.text:
            car_info["Комплектация"] = detail.text.split(":")[-1]
            continue
        elif "Тип кузова" in detail.text:
            car_info["Тип кузова"] = detail.text.split(":")[-1]
            continue
        elif "Цвет" in detail.text:
            car_info["Цвет"] = detail.text.split()[-1]
            continue
        elif "Руль" in detail.text:
            car_info["Руль"] = detail.text.split()[-1]
            continue
        elif "Обмен" in detail.text:
            car_info["Обмен"] = detail.text.split()[-1]
            continue
    # не учел история пробега

    print(car_info)


def main():
    url_proxies = "https://2ip.ru"
    car_url = "https://www.avito.ru/samara/avtomobili/chery_tiggo_7_pro_1.5_cvt_2021_30_100_km_3578803563"

    get_location(url_proxies)

    # Получение данных об автомобиле
    car_data = get_car_data(car_url)

    driver.quit()


if __name__ == "__main__":
    main()
