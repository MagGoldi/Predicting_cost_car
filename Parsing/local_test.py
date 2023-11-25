from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import random

driver = webdriver.Chrome()

with open("links_on_page.txt") as file:
    links = file.readlines()

for link in links:
    driver.get(link.strip())  # Открываем ссылку, удаляя символы новой строки
    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        },
    )
    time.sleep(random.uniform(2, 4))

driver.quit()
