from collections import deque
from bs4 import BeautifulSoup

class Person:
    name = None
    experiences = deque([])
    educations = deque([])
    also_viewed_urls = deque([])
    linkedin_id = None
    page = ''

    def __init__(self, page, linkedin_id):
        self.page = page
        self.linkedin_id = linkedin_id
        self.scrape()

    def scrape(self):
        self.getExperiences()
        self.getEducation()
        self.getAlsoViewedUrls()
        self.getName()

    def getName(self):
        n = self.page.find(class_='pv-top-card-section__name')
        if n is not None:
            self.name = n.get_text()

    def getExperiences(self):
        pass

    def getEducation(self):
        edu = self.page.find_all(class_='pv-education-entity')
        if edu is None:
            return
        for e in edu:
            school = e.find(class_='pv-entity__school-name')
            degree = e.find(class_='pv-entity__degree-name')
            degreeName = e.find(class_='pv-entity__fos')
            date = e.find(class_='pv-entity__dates')
            beginTime = None
            endTime = None

            if school is not None:
                school = school.get_text()
            if degree is not None:
                degree = degree.find(class_='pv-entity__comma-item')
                if degree is not None:
                    degree = degree.get_text()
                    if degreeName is not None:
                        degreeName = degreeName.find(class_='pv-entity__comma-item')
                        degree += (', ' + degreeName.get_text())
            if date is not None:
                date = date.find_all('time')
                if len(date) >= 2:
                    beginTime = date[0].get_text()
                    endTime = date[1].get_text()
            education = {
                'school': school,
                'degree': degree,
                'beginTime': beginTime,
                'endTime': endTime
            }
            print(education)

    def getAlsoViewedUrls(self):
        links = []
        for link in self.page.find_all('a'):
            url = link.get('href')
            if url and '/in/' in url:
                links.append(url)
        print('Links:')
        print(links)

    def __repr__(self):
        return 'Print person'
