import boto.sqs
import os
from boto.sqs.message import Message

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
        self.connection = boto.sqs.connect_to_region(
            self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        self.q = self.connection.get_queue(self.name)

    def add(self, value):
        message = Message()
        message.set_body(value)
        self.q.write(message)
        print('Added {0} to Q'.format(value))

    def count(self):
        return self.q.count()

    def fetch(self):
        return self.q.get_messages()
    
    def purge(self):
        self.q.purge()
        print('Q Purged')