import re
import requests
import multiprocessing
import time


def handler(proxy):
    link = "http://icanhazip.com/"
    proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}

    try:
        responce = requests.get(link, proxies=proxies, timeout=2).text
        print(f"IP: {responce.split()}")
    except:
        print("Прокси не валидный")


if __name__ == "__main__":
    with open("C:\PYTHON\Predicting_cost_car\Parsing\proxy.txt") as file:
        proxy_base = "".join(file.readlines()).strip().split("\n")
        print(len(set(proxy_base)))

    with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
        process.map(handler, proxy_base)
