import random
from selenium import webdriver
from bs4 import BeautifulSoup

with open("good_proxy.txt", "r") as proxy_file:
    proxies = proxy_file.readlines()


def get_random_proxy():
    return random.choice(proxies)


def get_soup(url):
    proxy = get_random_proxy()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=%s" % proxy)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        },
    )
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    return soup
