from collections import deque

class Person:
    name = None
    experiences = deque([])
    educations = deque([])
    also_viewed_urls = deque([])
    linkedin_url = None

    def __init__(self, page = "", browser = None):
        self.browser = browser

    def scrape(self):

    def __repr__(self):
        return "Print person"
