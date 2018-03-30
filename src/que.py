import boto.sqs
import os
from boto.sqs.message import Message
from colorama import Fore, Back, Style

class Que:
    def __init__(self, name, aws_access_key_id, aws_secret_access_key, region):
        self.name = name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region
        self.connection = None
        self.q = None
        self.connect()
    
    def connect(self):
        while (self.connection is None or self.q is None):
            print(Fore.YELLOW + 'Attempting to connect to Q' + Style.RESET_ALL)
            self.connection = boto.sqs.connect_to_region(
                self.region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )
            self.q = self.connection.get_queue(self.name)
        print('Connected to Q')

    def add(self, value):
        message = Message()
        message.set_body(value)
        self.q.write(message)
        print('Added {0} to Q'.format(value))

    def remove(self, message):
        self.q.delete_message(message)
        print('Removed {0} from Q'.format(message.get_body()))

    def count(self):
        return self.q.count()

    def fetch(self):
        return self.q.get_messages()

    def first(self):
        messages = self.fetch()
        return messages[0] if len(messages) > 0 else None

    def initial(self):
        return '/in/pushkinabbott/'

    def seed(self):
        self.add(self.initial())
        print('Seeding Q')

    def purge(self):
        self.q.purge()
        print('Q Purged')

    def reset(self):
        print('Q reset')
        self.purge()
        self.seed()