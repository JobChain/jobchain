from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import deque
import os, time, random, requests, pickle
from src.person import Person

def performLogin(browser, root):
    login = '/uas/login'
    email = os.getenv('JOBCHAIN_EMAIL')
    password = os.getenv('JOBCHAIN_PASSWORD')

    if email is None or password is None:
        raise ValueError('No email or password found')

    browser.get(root + login)
    time.sleep(random.uniform(4.0, 7.0))
    email_element = browser.find_element_by_id("session_key-login")
    email_element.send_keys(email)
    password_element = browser.find_element_by_id('session_password-login')
    password_element.send_keys(password)
    password_element.submit()

    print('Successfully logged in')

def main():
    root = 'https://www.linkedin.com'
    ids = ['/in/jeffreyphuang/', '/in/james534/', '/in/jim-zhao-03ba4697/', '/in/donaldngai/']
    visited = {}

    browser = webdriver.Chrome()

    try:
        performLogin(browser, root)
    except ValueError as error:
        print(error)
        return

    for id in ids:
        browser.get(root + id)
        #flip-card
        time.sleep(random.uniform(4.0, 7.0))
        try:
            browser.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
            _ = WebDriverWait(browser, random.uniform(5.0, 8.0)).until(EC.presence_of_element_located((By.ID, "education-section")))
        finally:
            page = BeautifulSoup(browser.page_source, 'html.parser')
            person = Person(page, id)
            visited[id] = person
            print(person)
            print('------------------------------------------------------------------------')

    time.sleep(random.uniform(10.0, 15.0))
    browser.close()

if __name__ == '__main__':
    main()
