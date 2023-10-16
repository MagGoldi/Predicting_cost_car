from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = (
    r"C:/Users/фвьшт/AppData/Local/Programs/Python/Python312/chromedriver.exe"
)
driver = webdriver.Firefox(
    executable_path=r"C:/Users/фвьшт/AppData/Local/Programs/Python/Python312/geckodriver.exe",
    options=options,
)
