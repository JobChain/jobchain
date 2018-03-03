from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import deque
import os, time, random, requests
from src.person import Person

def main():
    root = 'https://www.linkedin.com'
    ids = ['/in/jeffreyphuang/', '/in/james534/', '/in/jim-zhao-03ba4697/', '/in/donaldngai/']
    login = '/uas/login'
    email = os.getenv('JOBCHAIN_EMAIL')
    password = os.getenv('JOBCHAIN_PASSWORD')

    try:
        if email is None or password is None:
            raise ValueError('No email or password found')
    except ValueError as error:
        print(error)
        return

    browser = webdriver.Chrome()

    # Login
    browser.get(root + login)
    time.sleep(random.uniform(4.0, 7.0))
    email_element = browser.find_element_by_id("session_key-login")
    email_element.send_keys(email)
    password_element = browser.find_element_by_id('session_password-login')
    password_element.send_keys(password)
    password_element.submit()

    print('Logged In')

    browser.get(root + ids[0])
    time.sleep(random.uniform(4.0, 7.0))
    try:
        browser.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
        _ = WebDriverWait(browser, random.uniform(5.0, 8.0)).until(EC.presence_of_element_located((By.ID, "education-section")))
    finally:
        page = BeautifulSoup(browser.page_source, 'html.parser')
        person = Person(page, ids[0])
        print(person)

    time.sleep(random.uniform(10.0, 15.0))
    browser.close()

if __name__ == '__main__':
    main()
