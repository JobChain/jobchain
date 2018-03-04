from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import deque
import os, time, random, requests, pickle, re 
from src.person import Person

def getRandomProxy():
    root = 'https://www.ip-adress.com/proxy-list'
    proxies = []
    options = Options()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(root)
    time.sleep(random.uniform(1.0, 3.0))
    page = BeautifulSoup(browser.page_source, 'html.parser')
    for tag in page.find_all('td'):
        pattern  = '^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+){0,1}$'
        text = tag.get_text()
        if tag and re.fullmatch(pattern, text):
            proxies.append(text)
    browser.quit()
    return random.choice(proxies)

def resetPotential():
    q = deque(['/in/jeffreyphuang/'])
    picklePotential(q)

def picklePotential(q):
    file_name = 'potential.q'
    file_object = open(file_name,'wb')
    pickle.dump(q, file_object)
    file_object.close()
    print('Pickled Q:')
    print(q)

def unpicklePotential():
    file_name = 'potential.q'
    file_object = open(file_name,'rb')
    q = pickle.load(file_object)
    file_object.close()
    return q

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

def scrollPattern(browser):
    script = "window.scrollTo(0, Math.ceil(document.body.scrollHeight/"

    randHeight_1 = random.uniform(1.5, 3.0)
    scroll_1 = script + str(randHeight_1) + "));"
    browser.execute_script(scroll_1)
    time.sleep(random.uniform(2.0, 3.0))

    randHeight_2 = random.uniform(1.5, 3.0)
    scroll_2 = script + str(randHeight_2) + "));"
    browser.execute_script(scroll_2)
    _ = WebDriverWait(browser, random.uniform(3.0, 5.0)).until(EC.presence_of_element_located((By.ID, "experience-section")))

    time.sleep(random.uniform(2.0, 3.0))
    browser.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
    _ = WebDriverWait(browser, random.uniform(7.0, 10.0)).until(EC.presence_of_element_located((By.ID, "education-section")))

def main():
    root = 'https://www.linkedin.com'

    try:
        ids = unpicklePotential()
    except IOError:
        print('Potential Q corrupted')
        resetPotential()
        ids = unpicklePotential()

    visited = {}
    max = 5

    # proxy = getRandomProxy()
    # options = Options()
    # options.add_argument('--proxy-server='+proxy)
    # browser = webdriver.Chrome(chrome_options=options)
    # print('Proxy:', proxy)
    browser = webdriver.Chrome()

    try:
        performLogin(browser, root)
    except ValueError as error:
        print(error)
        return

    while len(ids):
        for index in range(len(ids)):
            if len(visited) >= max:
                break
            curr = ids.popleft()
            if (curr in visited):
                continue
            browser.get(root + curr)
            time.sleep(random.uniform(4.0, 7.0))
            try:
                scrollPattern(browser)
            except TimeoutException as ex:
                print('Experienced Timeout:')
                print(ex)
                picklePotential(ids)
                time.sleep(random.uniform(1.0, 7.0))
                browser.close()
                return
            finally:
                page = BeautifulSoup(browser.page_source, 'html.parser')
                person = Person(page, curr)
                visited[curr] = person
                nextUrls = person.also_viewed_urls
                for next in nextUrls:
                    if (next not in visited):
                        ids.append(next)
                print(person)
                print('------------------------------------------------------------------------')
                print('Stats:')
                print('\t' + 'Queue Length:', len(ids))
                print('\t' + 'Visited:', len(visited))
                print('------------------------------------------------------------------------')
        if len(visited) >= max:
            picklePotential(ids)
            break

    time.sleep(random.uniform(10.0, 15.0))
    browser.quit()

if __name__ == '__main__':
    main()
