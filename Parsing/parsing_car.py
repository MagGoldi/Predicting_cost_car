import csv
import time
import random
import datetime

from selenium import webdriver
from bs4 import BeautifulSoup


CAR_DATA = "Files/car_data_" + str(datetime.date.today()) + ".csv"
LINKS_MARK = "Files/links_mark.txt"
CAR_URL = "https://www.avito.ru/samara/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?radius=100&searchRadius=100"
PROXIES_URL = "https://2ip.ru"


driver = webdriver.Chrome()


def get_soup(url: str) -> BeautifulSoup:
    """
    Get the BeautifulSoup object from a given URL using Selenium.

    Args:
    url (str): The URL of the webpage to scrape.

    Returns:
    BeautifulSoup: The BeautifulSoup object representing the webpage.
    """
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def gen_rand_time() -> None:
    """
    Stops the program for a randomly generated time within the input parameters of the uniform method.

    Returns: None.
    """
    stop_time = random.uniform(1, 5)
    print(f"Время остановки - {stop_time} секунд")
    time.sleep(stop_time)


def get_location(url_proxies: str) -> None:
    """
    Get the location from the ip address page.

    Returns: None.
    """
    soup = get_soup(url_proxies)
    ip = soup.find("div", class_="ip").text.strip()
    location = soup.find("div", class_="value-country").text.strip()
    print(f"IP: {ip}\nLocation: {location}")


def save_links(filename: str, links: list) -> None:
    """
    Saves links from the site and writes them to a ".txt" file.
    If there is no file, it will create it with the name 'filename'.

    Args:
    filename (str): the name of the '.txt' file with links.
    links (list): the list with links to car brands.

    Returns: None.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for link in links:
            file.write(str(link) + "\n")


def create_car_data(filename: str) -> None:
    """
    Creates a forte '.csv' file with car data and writes column names to the first row.

    Args:
    filename (str): the name of the file in the '.csv' format.

    Returns: None.
    """
    with open(filename, "w", newline="", encoding="utf-8") as cars_data:
        writer = csv.DictWriter(cars_data, fieldnames=get_car_info().keys())
        writer.writeheader()


def add_car_data(filename: str, car_info: dict) -> None:
    """
    Adds data about one car to the end of the '.csv' file.

    Args:
    filename (str): the name of the file in the '.csv' format.
    car_info (dict): the dictionary that contains all the information about one car.

    Returns: None.
    """
    with open(filename, "a", newline="", encoding="utf-8") as cars_data:
        writer = csv.DictWriter(cars_data, fieldnames=car_info.keys())
        writer.writerow(car_info)


def get_car_info() -> dict:
    """
    Initializes a dictionary with empty values.

    Returns:
    Dict: dictionary with empty values.
    """
    car_info = {
        "Brand_Model": None,
        "Price": None,
        "Year": None,
        "Condition": None,
        "Engine_capacity": None,
        "Mileage": None,
        "Body_type": None,
        "Drive_type": None,
        "Engine_type": None,
        "City": None,
        "Link": None,
    }
    return car_info


def get_car_params(car_info: dict, params_list: list, index: int) -> dict:
    """
    Extracting parameters from an html page depending on the condition of the car.

    Args:
    car_info (dict): the dictionary that contains all the information about one car.
    params_list (list): the list with the parameters of the car.
    index (int): the index of the correct sequence in 'params_list'.

    Returns:
    dict: the dictionary with the correct sequence of parameters.
    """
    car_info["Mileage"] = params_list[index].strip()
    car_info["Engine_capacity"] = params_list[index + 1].strip()
    car_info["Body_type"] = params_list[index + 2].strip()
    car_info["Drive_type"] = params_list[index + 3].strip()
    car_info["Engine_type"] = params_list[index + 4].strip()
    return car_info


def parsing_car_data(page_item: list) -> None:
    """
    Parsing data about each car on the page.

    Args:
    page_item (list): the list of html blocks with information about each car on the page.

    Returns: None.
    """
    for item in page_item:
        car_info = get_car_info()
        title = item.find("h3", {"itemprop": "name"})

        if title:
            title = item.find("h3", {"itemprop": "name"}).text
        else:
            continue

        car_info["Brand_Model"] = title.split(",")[0].strip()
        car_info["Year"] = title.split(",")[1].strip()
        car_info["Price"] = int(item.find("meta", {"itemprop": "price"})["content"])

        link = item.find("a", {"data-marker": "item-title"})
        car_info["Link"] = "https://www.avito.ru" + str(link.get("href"))

        params = item.find("div", {"class": "iva-item-autoParamsStep-WzfS8"}).text
        params_list = params.split(",")

        if len(params_list) < 5:
            continue
        if len(params_list) == 6:
            car_info["Condition"] = "Битая"
            car_info = get_car_params(car_info, params_list, 1)
        else:
            car_info["Condition"] = "Не битая"
            car_info = get_car_params(car_info, params_list, 0)

        car_info["City"] = item.find("div", {"class": "geo-root-zPwRk"}).text.strip()

        add_car_data(CAR_DATA, car_info)


def parsing_brand_links(soup: BeautifulSoup) -> list:
    """
    The function that parses links to car brands

    Args:
    soup (BeautifulSoup): html page layout with links.

    Returns:
    all_links_mark_list: the list with all links to car brands.
    """
    all_links_mark = soup.find_all("a", {"data-marker": "popular-rubricator/link"})
    all_links_mark_list = [
        "https://www.avito.ru" + str(link.get("href")) for link in all_links_mark
    ]
    all_links_mark_list = all_links_mark_list[:28]
    save_links(LINKS_MARK, all_links_mark_list)
    return all_links_mark_list


def clicking_on_links(car_url: str) -> None:
    """
    The function that follows links and takes their html layout

    Args:
    car_url (str): The URL of the webpage to scrape.

    Returns: None.
    """
    create_car_data(CAR_DATA)

    soup = get_soup(car_url)

    all_links_mark_list = parsing_brand_links(soup)

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
            parsing_car_data(page_item)

            gen_rand_time()
        gen_rand_time()


def main() -> None:
    """
    The function of starting the main work.

    Returns: None
    """
    get_location(PROXIES_URL)
    clicking_on_links(CAR_URL)
    driver.quit()


if __name__ == "__main__":
    main()
