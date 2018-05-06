from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import deque
from datetime import datetime
from colorama import Fore, Back, Style
import os, time, random, requests, re, sys
from person import Person
from helpers import educationStartDate, educationEndDate, parseDate
from que import Que
from psql import User, Work, Education, PSQL, CheckedUser, Company


class Scraper:
    def __init__(self):
        self.starttime = datetime.now()
        self.root_url = 'https://www.linkedin.com'
        self.login_url = '/uas/login'
        self.partial_scroll = 'window.scrollTo(0, Math.ceil(document.body.scrollHeight/'
        self.full_scroll = 'window.scrollTo(0, Math.ceil(document.body.scrollHeight));'
        self.q_name = os.getenv('JOBCHAIN_Q_NAME')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION')
        self.email = os.getenv('JOBCHAIN_EMAIL')
        self.password = os.getenv('JOBCHAIN_PASSWORD')
        self.psql_username = os.getenv('PSQL_USERNAME')
        self.psql_password = os.getenv('PSQL_PASSWORD')
        self.psql_address = os.getenv('PSQL_ADDRESS')
        self.psql_db = os.getenv('PSQL_DB')
        self.verify_env_var()
        self.potential = None
        self.psql = None
        self.visited = {}
        self.options = Options()
        # self.options.add_argument('headless')
        self.options.add_argument('no-sandbox')
        self.browser = None
        self.psql = None
        self.connect()
        self.run()


    def verify_env_var(self):
        if not self.q_name:
            print("Missing q_name")
            sys.exit(0)
        elif not self.aws_access_key_id:
            print("Missing aws_access_key_id")
            sys.exit(0)
        elif not self.aws_secret_access_key:
            print("Missing aws_secret_access_key")
            sys.exit(0)
        elif not self.aws_region:
            print("Missing aws_region")
            sys.exit(0)
        elif not self.email:
            print("Missing email")
            sys.exit(0)
        elif not self.password:
            print("Missing password")
            sys.exit(0)
        elif not self.psql_username:
            print("Missing psql_username")
            sys.exit(0)
        elif not self.psql_password:
            print("Missing psql_password")
            sys.exit(0)
        elif not self.psql_address:
            print("Missing psql_address")
            sys.exit(0)
        elif not self.psql_db:
            print("Missing psql_db")
            sys.exit(0)

    def login(self):
        if self.email is None or self.password is None:
            raise ValueError('No email or password found')

        if self.browser:
            self.browser.quit()
            self.sleep(4.0, 7.0)
            self.browser = None

        self.drive()
        self.visit(self.root_url + self.login_url)
        _ = WebDriverWait(self.browser, random.uniform(5.0, 8.0)).until(EC.presence_of_element_located((By.ID, 'session_key-login')))
        email_element = self.browser.find_element_by_id("session_key-login")
        email_element.send_keys(self.email)
        password_element = self.browser.find_element_by_id('session_password-login')
        password_element.send_keys(self.password)
        password_element.submit()

    def maneuver(self):
        randHeight_1 = random.uniform(1.5, 3.0)
        scroll_1 = self.partial_scroll + str(randHeight_1) + "));"

        self.browser.execute_script(scroll_1)
        self.sleep(2.0, 3.0)

        randHeight_2 = random.uniform(1.5, 3.0)
        scroll_2 = self.partial_scroll + str(randHeight_2) + "));"
        self.browser.execute_script(scroll_2)
        _ = WebDriverWait(self.browser, random.uniform(7.0, 10.0)).until(EC.presence_of_element_located((By.ID, "experience-section")))

        time.sleep(random.uniform(2.0, 3.0))
        self.browser.execute_script(self.full_scroll)
        _ = WebDriverWait(self.browser, random.uniform(7.0, 10.0)).until(EC.presence_of_element_located((By.ID, "education-section")))

    def connect(self):
        if self.potential:
            self.potential = None
            self.sleep(1.0, 3.0)

        self.potential = Que(
            self.q_name,
            self.aws_access_key_id,
            self.aws_secret_access_key,
            self.aws_region
        )

        self.psql = PSQL(self.psql_username, self.psql_password, self.psql_address, self.psql_db)
        self.session = self.psql.session
        print(self.session)

    def hack(self):
        soup = BeautifulSoup(self.browser.page_source.encode('utf-8').decode('ascii', 'ignore'), 'html.parser')
        if soup.find(class_='join-form'):
            print(Fore.RED + 'Access Denied' + Style.RESET_ALL)
            print(Fore.YELLOW + 'Attempting Hack' + Style.RESET_ALL)
            self.run()

    def scroll(self):
        for i in range(0, 5):
            try:
                print(Fore.YELLOW + 'Attempting to scroll ' + Style.RESET_ALL)
                self.maneuver()
            except TimeoutException as tex:
                print(Fore.RED + 'Experienced Timeout Exception:' + Style.RESET_ALL)
                print(tex)
                self.hack()
                continue
            except WebDriverException as wdex:
                print(Fore.RED + 'Experienced WebDriver Exception:' + Style.RESET_ALL)
                print(wdex)
                self.hack()
                continue
            else:
                print(Fore.GREEN + 'Scrolled ' + Style.RESET_ALL)
                self.sleep(3.0, 6.0)
                return True
                break
        return False

    def visit(self, url):
        while True:
            try:
                print(Fore.YELLOW + 'Attempting to visit ' + url + Style.RESET_ALL)
                self.browser.get(url)
            except TimeoutException as tex:
                print(Fore.RED + 'Experienced Timeout Exception:' + Style.RESET_ALL)
                print(tex)
                self.sleep(3.0, 6.0)
                continue
            except WebDriverException as wdex:
                print(Fore.RED + 'Experienced WebDriver Exception:' + Style.RESET_ALL)
                print(wdex)
                self.sleep(3.0, 6.0)
                continue
            else:
                print(Fore.GREEN + 'Visited ' + url + Style.RESET_ALL)
                self.sleep(3.0, 6.0)
                break

    def drive(self):
        while True:
            try:
                print(Fore.YELLOW + 'Attempting to create WebDriver' + Style.RESET_ALL)
                self.browser = webdriver.Chrome(chrome_options=self.options)
            except ConnectionResetError as cre:
                print(Fore.RED + 'Experienced ConnectionResetError:' + Style.RESET_ALL)
                print(cre)
                self.sleep(3.0, 6.0)
                continue
            else:
                print(Fore.GREEN + 'WebDriver Created' + Style.RESET_ALL)
                self.sleep(3.0, 6.0)
                break

    def sleep(self, low, high):
        time.sleep(random.uniform(low, high))

    def run(self):
        try:
            self.login()
        except ValueError as ve:
            print(ve)
            sys.exit(0)
        else:
            print(Fore.GREEN + 'Logged In' + Style.RESET_ALL)
            self.sleep(1.0, 3.0)

        if self.potential is None:
            print(Fore.RED + 'Q is None' + Style.RESET_ALL)
            sys.exit(0)

        self.visit("https://www.linkedin.com/school/uwaterloo/alumni/?educationEndYear=2015&educationStartYear=2010&keywords=software")
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        lastHeight = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.sleep(3.0, 3.2)
            newHeight = self.browser.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
        print(Fore.YELLOW + 'Done scrolling' + Style.RESET_ALL)
        soup = BeautifulSoup(self.browser.page_source.encode('utf-8').decode('ascii', 'ignore'), 'html.parser')
        print(self.browser.page_source)

        # while self.potential.first():
        #     current_message = self.potential.first()
        #     self.potential.remove(current_message)
        #     current_id = current_message.get_body()

        #     self.visit(self.root_url + current_id)

        #     if not self.scroll():
        #         print(Fore.YELLOW + current_id + ' Waste' + Style.RESET_ALL)
        #         # self.potential.remove(current_message)
        #         continue

        #     showMoreButtons = self.browser.find_elements_by_css_selector("section[id='experience-section'] button.pv-profile-section__see-more-inline")
        #     while showMoreButtons:
        #         print(Fore.YELLOW + str(len(showMoreButtons)) + ' show alls' + Style.RESET_ALL)
        #         for button in showMoreButtons:
        #             ActionChains(self.browser).move_to_element(button).perform()
        #             scroll = self.partial_scroll + "-2));"
        #             self.browser.execute_script(scroll)
        #             button.click()
        #             print(Fore.BLUE + 'Clicked: ' + Style.RESET_ALL)
        #             self.sleep(1.0, 2.0)

        #         showMoreButtons = self.browser.find_elements_by_css_selector("section[id='experience-section'] button.pv-profile-section__see-more-inline")
            # soup = BeautifulSoup(self.browser.page_source.encode('utf-8').decode('ascii', 'ignore'), 'html.parser')

            # if self.session.query(User).filter_by(id=current_id).first():
            #     print(Fore.YELLOW + current_id + ' Already in DB' + Style.RESET_ALL)
            #     # self.potential.remove(current_message)
            #     continue
            # person = Person(soup, current_id)
            # if person.shouldScrape():
            #     self.visited[current_id] = person
            #     for url in person.also_viewed_urls:
            #         if url not in self.visited and not self.is_in_checked_user(url):
            #             self.potential.add(url)

            #     self.write_to_db(person)
            #     print(person)
            #     print('------------------------------------------------------------------------')
            #     print('Stats:')
            #     print('\t' + 'Queue Length:', self.potential.count())
            #     print('\t' + 'Visited:', len(self.visited))
            #     print('\t' + 'Elapsed time:', datetime.now() - self.starttime)
            #     print('------------------------------------------------------------------------')
            #     # self.potential.remove(current_message)
            # else:
            #     print(Fore.BLUE + 'Skipped:' + Style.RESET_ALL, current_id)
            #     # self.potential.remove(current_message)

        self.sleep(100.0, 100.0)
        # self.browser.quit()

    def reset(self):
        print('all Purged')
        # self.psql.reset()
        # self.potential.reset()
        while(not self.potential.first()):
            self.sleep(2.0,3.0)
        self.is_in_checked_user(self.potential.initial())

    def is_in_checked_user(self, id):
        if self.session.query(CheckedUser).filter_by(id=id).first():
            return True
        else:
            self.session.add(CheckedUser(id=id))
            self.session.commit()
            return False

    def is_in_companies(self, id):
        if self.session.query(Company).filter_by(id=id).first():
            return True
        else:
            return False

    def write_to_db(self, person):
        print(Fore.GREEN + 'Saving data to PSQL' + Style.RESET_ALL)
        u = User(id=person.id, name=person.name)
        self.session.add(u)
        self.session.commit()
        for e in person.experiences:
            work = Work(company_name=e['company'],
                        user_id=person.id,
                        job_title=e['position'],
                        location=e['location'],
                        start_date=parseDate(e['date_range'])[0],
                        end_date=parseDate(e['date_range'])[1])
            self.session.add(work)
            self.session.commit()
        for e in person.educations:
            education = Education(school_name=e['school'],
                                  user_id=person.id,
                                  program=e['degree'],
                                  start_date=educationStartDate(e['beginTime']),
                                  end_date=educationEndDate(e['endTime']))
            self.session.add(education)
            self.session.commit()
        for c in person.companies:
            if not self.is_in_companies(c['id']):
                company = Company(id=c['id'], logo=c['logo'], url=c['url'])
                self.session.add(company)
                self.session.commit()
        print(Fore.GREEN + 'Saved data to PSQL' + Style.RESET_ALL)

if __name__ == '__main__':
    Scraper()
