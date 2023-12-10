import os
import csv
import time
import random
import datetime

from selenium import webdriver
from bs4 import BeautifulSoup


CAR_DATA = "Files/car_data_" + str(datetime.date.today()) + ".csv"
LINKS_MARK = "Files/links_mark.txt"
CAR_URL = "https://www.avito.ru/samara/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?radius=100&searchRadius=100"


driver = webdriver.Chrome()


def get_soup(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def gen_rand_time():
    stop_time = random.uniform(1, 5)
    print(f"Время остановки - {stop_time} секунд")
    time.sleep(stop_time)


def get_location(url_proxies):
    soup = get_soup(url_proxies)
    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()
    print(f"IP: {ip}\nLocation: {location}")


def save_links(name_file, links):
    with open(name_file, "w", encoding="utf-8") as file:
        for link in links:
            file.write(str(link) + "\n")


def create_car_data(filename):
    with open(filename, "w", newline="", encoding="utf-8") as cars_data:
        writer = csv.DictWriter(cars_data, fieldnames=get_car_info().keys())
        writer.writeheader()


def add_car_data(filename, car_info):
    with open(filename, "a", newline="", encoding="utf-8") as cars_data:
        writer = csv.DictWriter(cars_data, fieldnames=car_info.keys())
        writer.writerow(car_info)


def get_car_info():
    car_info = {
        "Brand_Model": None,
        "Price": None,
        "Condition": None,
        "Engine_capacity": None,
        "Mileage": None,
        "Body_type": None,
        "Drive_type": None,
        "Engine_type": None,
        "City": None,
        "Link": None,
        "Photo": None,
    }
    return car_info


def get_car_data(car_url):
    create_car_data(CAR_DATA)

    soup = get_soup(car_url)

    all_links_mark = soup.find_all("a", {"data-marker": "popular-rubricator/link"})
    all_links_mark_list = [
        "https://www.avito.ru" + str(link.get("href")) for link in all_links_mark
    ]
    all_links_mark_list = all_links_mark_list[:29]
    save_links(LINKS_MARK, all_links_mark_list)

    for mark in all_links_mark_list:
        soup = get_soup(mark)
        time.sleep(10)
        max_num_page = soup.find(
            "li",
            class_="styles-module-listItem-_La42 styles-module-listItem_last-GI_us styles-module-listItem_notFirst-LGEQU",
        ).text
        for num_page in range(1, int(max_num_page) + 1):
            page = (
                mark.split("?")[0]
                + "?cd="
                + str(num_page)
                + "&p="
                + str(num_page)
                + "&radius=100&searchRadius=100"
            )

            soup = get_soup(page)

            div_to_remove = soup.find("div", {"data-marker": "witcher/block"})

            if div_to_remove:
                div_to_remove.decompose()

            page_item = soup.find_all("div", class_="iva-item-content-rejJg")

            for item in page_item:
                car_info = get_car_info()
                title = item.find("h3", {"itemprop": "name"})

                if title:
                    title = item.find("h3", {"itemprop": "name"}).text
                else:
                    continue

                car_info["Brand_Model"] = title.split(",")[0].strip()
                car_info["Price"] = int(
                    item.find("meta", {"itemprop": "price"})["content"]
                )

                # Ссылка
                link = item.find("a", {"data-marker": "item-title"})
                car_info["Link"] = "https://www.avito.ru" + str(link.get("href"))

                # Объем двигателя, пробег, bodytype, вид привода, тип двигателя
                params = item.find(
                    "div", {"class": "iva-item-autoParamsStep-WzfS8"}
                ).text
                params_list = params.split(",")

                if len(params_list) != 5:
                    continue

                car_info["Mileage"] = params_list[0].strip()
                car_info["Engine_capacity"] = params_list[1].strip().split()[0]
                car_info["Body_type"] = params_list[2].strip()
                car_info["Drive_type"] = params_list[3].strip()
                car_info["Engine_type"] = params_list[4].strip()

                # Город объявления
                car_info["City"] = item.find(
                    "div", {"class": "geo-root-zPwRk"}
                ).text.strip()

                # Фото
                # photo = item.find("div", class_="iva-item-sliderLink-uLz1v")
                # if photo:
                #    car_info["Photo"] = photo.get("src")
                # else:
                #    car_info["Photo"] = None
                add_car_data(CAR_DATA, car_info)
            gen_rand_time()
        gen_rand_time()


def main():
    # url_proxies = "https://2ip.ru"
    # get_location(url_proxies)
    get_car_data(CAR_URL)
    driver.quit()


if __name__ == "__main__":
    main()
