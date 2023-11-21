import csv
import random
import time
import requests

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


url_proxies = "https://2ip.ru"
get_location(url_proxies)
car_url = "https://www.avito.ru/samara/avtomobili/toyota_rav4_2.0_mt_2020_50_000_km_3272058958"
soup = get_soup(car_url)

print(type(soup.find("a", {"data-marker": "item-view/closed-warning"})))
if type(soup.find("a", {"data-marker": "item-view/closed-warning"})) == type(None):
    print("есть")
else:
    print("снято c обьявления")
