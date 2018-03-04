from collections import deque
from bs4 import BeautifulSoup
import re

class Person:
    def __init__(self, page, linkedin_id):
        self.page = page
        self.linkedin_id = linkedin_id
        self.id = linkedin_id[4:]
        self.name = None
        self.experiences = []
        self.educations = []
        self.also_viewed_urls = []
        self.scrape()

    def scrape(self):
        self.getExperiences()
        self.getEducation()
        self.getAlsoViewedUrls()
        self.getName()

    def getName(self):
        name = self.page.find(class_='pv-top-card-section__name')
        self.name = None if name is None else name.get_text()

    def getExperiences(self):
        section = self.page.find(id='experience-section')
        if section is None:
            return
        for experience in section.find_all('li', class_='pv-profile-section__card-item pv-position-entity ember-view'):
            job = {}
            if experience is None:
                return
            summary = experience.find('div', class_='pv-entity__summary-info')
            if summary is None:
                return
            
            company = summary.find('h4', class_='Sans-17px-black-85%').find('span', class_='pv-entity__secondary-title')
            position = summary.find('h3', class_='Sans-17px-black-85%-semibold')
            date_range_div = summary.find('h4', class_='pv-entity__date-range inline-block Sans-15px-black-70%')
            date_range = None
            if date_range_div:
                for span in date_range_div.find_all('span'):
                    span_class = span['class'] if 'class' in span.attrs else []
                    if 'visually-hidden' not in span_class:
                        date_range = span
                        break

            date_duration = summary.find('h4', class_='inline-block Sans-15px-black-70%').find('span', class_='pv-entity__bullet-item')
            location_div = summary.find('h4', class_='pv-entity__location Sans-15px-black-70% block')
            location = None
            if location_div:
                for span in location_div.find_all('span'):
                    span_class = span['class'] if 'class' in span.attrs else []
                    if 'visually-hidden' not in span_class:
                        location = span
                        break

            if company or position or date_range or date_duration or location:
                job['company'] = None if company is None else company.get_text()
                job['position'] = None if position is None else position.get_text()
                job['date_range'] = None if date_range is None else date_range.get_text()
                job['date_duration'] = None if date_duration is None else date_duration.get_text()
                job['location'] = None if location is None else location.get_text()
                self.experiences.append(job)

    def getEducation(self):
        section = self.page.find_all(class_='pv-education-entity')
        if section is None:
            return
        for education in section:
            learning = {}
            school = education.find(class_='pv-entity__school-name')
            degree_div = education.find(class_='pv-entity__degree-name')
            degree_name_div = education.find(class_='pv-entity__fos')
            date_div = education.find(class_='pv-entity__dates')
            degree = None
            beginTime = None
            endTime = None
    
            if degree_div:
                degree_span = degree_div.find(class_='pv-entity__comma-item')
                if degree_span is not None:
                    degree = degree_span.get_text()
                    if degree_name_div is not None:
                        degree_name_span = degree_name_div.find(class_='pv-entity__comma-item')
                        degree += (', ' + degree_name_span.get_text())

            if date_div:
                date = date_div.find_all('time')
                if len(date) >= 2:
                    beginTime = date[0].get_text()
                    endTime = date[1].get_text()

            if school or degree or beginTime or endTime:
                learning['school'] = None if school is None else school.get_text()
                learning['degree'] = None if degree is None else degree
                learning['beginTime'] = None if beginTime is None else beginTime
                learning['endTime'] = None if endTime is None else endTime
                self.educations.append(learning)

    def getAlsoViewedUrls(self):
        pattern = '^\/in\/[a-zA-Z0-9\-]+\/$'
        for link in self.page.find_all('a'):
            url = link.get('href')
            if url and re.fullmatch(pattern, url):
                self.also_viewed_urls.append(url)

    def shouldScrape(self):
        isWaterloo = False
        if self.educations is not None:
            for education in self.educations:
                if 'Waterloo' in str(education['school']):
                    isWaterloo = True
        return isWaterloo

    def __repr__(self):
        value = ''
        value += 'Name: ' + str(self.name) + '\n'
        value += 'Education: ' + '\n'
        for education in self.educations:
            value += '\t' + str(education['school']) + '\n'
            value += '\t\t' + str(education['degree']) + '\n'
            value += '\t\t' + str(education['beginTime']) + ' to ' + str(education['endTime']) + '\n'

        value += 'Experience: ' + '\n'
        for experience in self.experiences:
            value += '\t' + str(experience['company']) + '\n'
            value += '\t\t' +  str(experience['position']) + '\n'
            value += '\t\t' + str(experience['date_range']) + '\n'
            value += '\t\t' + str(experience['date_duration']) + '\n'
            value += '\t\t' + str(experience['location']) + '\n'

        value += 'Viewed: ' + '\n'
        for url in self.also_viewed_urls:
            value += '\t' + str(url) + '\n'

        return value
