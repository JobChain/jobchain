from collections import deque
from bs4 import BeautifulSoup

class Person:
    name = None
    experiences = deque([])
    educations = deque([])
    also_viewed_urls = deque([])
    linkedin_id = None
    page = ""

    def __init__(self, page, linkedin_id):
        self.page = page
        self.linkedin_id = linkedin_id
        self.scrape

    def scrape(self):
        self.getExperiences
        self.getEducation
        self.getAlsoViewedUrls

    def getExperiences(self):
        pass

    def getEducation(self):
        pass

    def getAlsoViewedUrls(self):
        links = []
        for link in self.page.find_all('a'):
            url = link.get('href')
            if url and '/in/' in url:
                links.append(url)
        print("Links:")
        print(links)


    def __repr__(self):
        return "Print person"
