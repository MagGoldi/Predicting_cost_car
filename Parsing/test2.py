import os
import csv
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


driver = webdriver.Chrome()

import random


def get_soup(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def gen_rand(start=3, end=10):
    return random.uniform(start, end)


def get_location(url_proxies):
    soup = get_soup(url_proxies)

    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()

    print(f"IP: {ip}\nLocation: {location}")


def get_car_data(car_url):
    soup = get_soup(car_url)
    time.sleep(gen_rand())

    all_link_mark = soup.find_all("a", {"data-marker": "popular-rubricator/link"})
    all_link_mark_list = [
        "https://www.avito.ru" + str(link.get("href")) for link in all_link_mark
    ]
    print(all_link_mark_list)
    print(len(all_link_mark_list))

    for mark in all_link_mark_list:
        soup = get_soup(mark)

        max_num_page = soup.find(
            "li",
            class_="styles-module-listItem-_La42 styles-module-listItem_last-GI_us styles-module-listItem_notFirst-LGEQU",
        ).text

        for num_page in range(1, int(max_num_page) + 1):
            mark = (
                mark.split("?")[0]
                + "?cd="
                + str(num_page)
                + "&p="
                + str(num_page)
                + "&radius=100&searchRadius=100"
            )

            soup = get_soup(mark)
            print(mark)

            all_link_page = soup.find_all("a", {"data-marker": "item-title"})
            all_link_page_list = [
                "https://www.avito.ru" + str(link.get("href")) for link in all_link_page
            ]

            print(all_link_page_list)
            print(len(all_link_page_list))

            for link in all_link_page_list:
                soup = get_soup(link)

                title = soup.find_all("a", class_="breadcrumbs-link-Vr4Nc")
                all_info = soup.find_all("li", class_="params-paramsList__item-appQw")
                price = soup.find("span", {"itemprop": "price"}).text

                for n in title:
                    print(n.text)
                for n in all_info:
                    print(n.text)
                print(price)

                time.sleep(gen_rand())

            time.sleep(gen_rand())


def main():
    url_proxies = "https://2ip.ru"
    car_url = "https://www.avito.ru/samara/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?radius=100&searchRadius=100"

    get_location(url_proxies)

    # Получение данных об автомобиле
    car_data = get_car_data(car_url)

    driver.quit()


if __name__ == "__main__":
    main()
