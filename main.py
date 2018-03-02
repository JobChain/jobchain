import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    root = "https://www.linkedin.com"
    urls = ["/in/jeffreyphuang/", "/in/james534/", "/in/jim-zhao-03ba4697/", "/in/donaldngai/"]

    driver = webdriver.Chrome()
    driver.get(root + urls[0])

    # person = Person()
    time.sleep(15)
    # person.scrape()
    # print(person)

    driver.close()

if __name__ == '__main__':
    print("Starting...")
    main()
