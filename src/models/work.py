from db import db

class Work(db.Model):
    __tablename__ = 'WORK'
    id = db.Column(db.Integer, db.Sequence('work_id_seq'), primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String(80))
    location = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    current = db.Column(db.Boolean)

    user_id = db.Column(db.String, db.ForeignKey('LINKEDINUSER.id'))
    user = db.relationship('LINKEDINUSER')

    def __init__(self, company_name, user_id, job_title, location, start_date, end_date, current):
        self.company_name = company_name
        self.user_id = user_id
        self.job_title = job_title
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.current = current

    def json(self):
        return {
            'company_name': self.company_name,
            'user_id': self.user_id,
            'job_title': self.job_title,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'current': self.current}

    @classmethod
    def find_by_company_name(cls, company_name):
        return cls.query.filter_by(company_name=company_name)

    @classmethod
    def find_by_job_title(cls, job_title):
        return cls.query.filter_by(job_title=job_title)

    @classmethod
    def find_by_location(cls, location):
        return cls.query.filter_by(location=location)

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
