from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os, time, random, requests

def main():
    root = 'https://www.linkedin.com'
    urls = ["/in/jeffreyphuang/", "/in/james534/", "/in/jim-zhao-03ba4697/", "/in/donaldngai/"]
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
    time.sleep(random.uniform(3.0, 6.0))
    email_element = browser.find_element_by_id("session_key-login")
    email_element.send_keys(email)
    password_element = browser.find_element_by_id("session_password-login")
    password_element.send_keys(password)
    password_element.submit()

    print('Logged In')

    time.sleep(random.uniform(10.0, 15.0))

    browser.close()

if __name__ == '__main__':
    main()
