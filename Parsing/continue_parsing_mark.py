import os
import csv
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


LINKS_MARK = "links_mark.txt"
LINKS_ON_PAGE = "links_on_page.txt"

driver = webdriver.Chrome()


def get_soup(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def gen_rand_time():
    stop_time = random.uniform(1, 5)
    print(f"Время остановки - {stop_time} секунд")
    time.sleep(stop_time)


def save_links(name_file, links):
    with open(name_file, "a", encoding="utf-8") as file:
        for link in links:
            file.write(str(link) + "\n")


def get_location(url_proxies):
    soup = get_soup(url_proxies)
    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()
    print(f"IP: {ip}\nLocation: {location}")


def get_car_data():
    with open("LINKS_MARK.txt", "r") as file:
        all_links_mark_list = file.readlines()

    # Удаляем символ переноса строки из каждой ссылки
    all_links_mark_list = [link.strip() for link in all_links_mark_list]

    for mark in all_links_mark_list:
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
            save_links(LINKS_ON_PAGE, all_link_page_list)
            gen_rand_time()
        gen_rand_time()


def main():
    url_proxies = "https://2ip.ru"
    get_location(url_proxies)
    get_car_data()
    driver.quit()


if __name__ == "__main__":
    main()
