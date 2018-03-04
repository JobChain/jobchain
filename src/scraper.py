from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import deque
from datetime import datetime
from colorama import Fore, Back, Style
import os, time, random, requests, re
from person import Person
from que import Que
from psql import User, Work, Education, PSQL


def performLogin(browser, root):
    login = '/uas/login'
    email = os.getenv('JOBCHAIN_EMAIL')
    password = os.getenv('JOBCHAIN_PASSWORD')

    if email is None or password is None:
        raise ValueError('No email or password found')

    browser.get(root + login)
    time.sleep(random.uniform(6.0, 10.0))
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
    starttime = datetime.now()
    root = 'https://www.linkedin.com'
    q_name = os.getenv('JOBCHAIN_Q_NAME')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION')
    psql_username = os.getenv('PSQL_USERNAME')
    psql_password = os.getenv('PSQL_PASSWORD')

    visited = {}
    max = 5

    options = Options()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    browser = webdriver.Chrome(chrome_options=options)

    try:
        performLogin(browser, root)
    except ValueError as error:
        print(error)
        return

    potential = Que(q_name, aws_access_key_id, aws_secret_access_key, aws_region)

    psql = PSQL(psql_username, psql_password)

    while potential.count():
        current = potential.first()
        browser.get(root + current)
        time.sleep(random.uniform(6.0, 9.0))
        try:
            scrollPattern(browser)
        except TimeoutException as time_ex:
            print(Fore.RED + 'Experienced Timeout Exception:' + Style.RESET_ALL)
            browser.quit()
            time.sleep(random.uniform(3.0, 7.0))
            browser = webdriver.Chrome(chrome_options=options)
            try:
                performLogin(browser, root)
            except ValueError as error:
                print(error)
                return
        except WebDriverException as web_drive_ex:
            print(Fore.RED + 'Experienced WebDriver Exception:' + Style.RESET_ALL)
            browser.quit()
            time.sleep(random.uniform(3.0, 7.0))
            browser = webdriver.Chrome(chrome_options=options)
            try:
                performLogin(browser, root)
            except ValueError as error:
                print(error)
                return
        finally:
            soup = BeautifulSoup(browser.page_source.encode('utf-8').decode('ascii', 'ignore'), 'html.parser')
            person = Person(soup, current)
            if person.shouldScrape():
                visited[current] = person
                for url in person.also_viewed_urls:
                    if url not in visited:
                        potential.add(url)
                data = [User(id=person.id, first_name=person.name)]
                for e in p.experiences:
                    work = Work(company_name=e['company'], 
                                user_id=person.id,
                                job_title=e['position'],
                                duration=e['date_duration'])
                    data.append(work)
                for e in p.educations:
                    education = Education(school_name=e['school'], 
                                user_id=person.id,
                                program=e['degree'])
                    data.append(education)
                print(data)
                print('Saving data to PSQL')
                psql.session.bulk_save_objects(data)
                print('Saved data to PSQL')

                print(person)
                print('------------------------------------------------------------------------')
                print('Stats:')
                print('\t' + 'Queue Length:', potential.count())
                print('\t' + 'Visited:', len(visited))
                print('\t' + 'Elapsed time:', datetime.now() - starttime)
                print('------------------------------------------------------------------------')
            else:
                print(Fore.BLUE + 'Skipped:' + Style.RESET_ALL, current)

    time.sleep(random.uniform(10.0, 15.0))
    browser.quit()

if __name__ == '__main__':
    main()
