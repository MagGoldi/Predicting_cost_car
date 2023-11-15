import csv
import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver


driver = webdriver.Chrome()


def get_soup(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def get_location(url_proxies):
    driver.get(url_proxies)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()
    print(f"IP: {ip}\nLocation: {location}")


def gen_rand_time():
    stop_time = random.uniform(2, 5)
    print(f"Время остановки - {stop_time} секунд")
    time.sleep(stop_time)


def get_car_info():
    car_info = {
        "Цена": None,
        "Марка": None,
        "Модель": None,
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
        "Ссылка": None,
    }
    return car_info


def get_car_data(car_url):
    soup = get_soup(car_url)
    car_info = get_car_info(car_url)

    title = soup.find_all("span", {"itemprop": "name"})

    car_info["Ссылка"] = car_url
    car_info["Марка"] = title[4].text
    car_info["Модель"] = title[5].text

    price = soup.find("span", {"itemprop": "price"}).text
    car_info["Цена"] = int(price.replace("\xa0", ""))

    details = soup.find_all("li", class_="params-paramsList__item-appQw")

    for detail in details:
        if "Год выпуска" in detail.text:
            car_info["Год выпуска"] = int(detail.text.split()[-1])
            continue
        elif "Поколение" in detail.text:
            car_info["Поколение"] = detail.text.split(":")[-1].strip()
            continue
        elif "Пробег" in detail.text:
            car_info["Пробег"] = detail.text.split(":")[-1]
            continue
        elif "Владельцев по ПТС" in detail.text:
            car_info["Владельцев по ПТС"] = int(detail.text.split()[-1])
            continue
        elif "Состояние" in detail.text:
            car_info["Состояние"] = detail.text.split(":")[-1].strip()
            continue
        elif "Модификация" in detail.text:
            car_info["Модификация"] = detail.text.split(":")[-1].strip()
            continue
        elif "Объём двигателя" in detail.text:
            car_info["Объём двигателя"] = float(detail.text.split()[-2])
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
            car_info["Комплектация"] = detail.text.split(":")[-1].strip()
            continue
        elif "Тип кузова" in detail.text:
            car_info["Тип кузова"] = detail.text.split(":")[-1].strip()
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
    # не учел история пробега, VIN
    return car_info


def main():
    url_proxies = "https://2ip.ru"
    get_location(url_proxies)

    with open("file.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=get_car_info().keys())
        writer.writeheader()
        with open("links_on_page.txt", "r") as file:
            car_url = file.readlines()
            car_info = get_car_data(car_url)
        writer.writerow(car_info)
    driver.quit()


if __name__ == "__main__":
    main()
