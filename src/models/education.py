from db import db

class Education(db.Model):
    __tablename__ = 'EDUCATION'
    id = db.Column(db.Integer, db.Sequence('education_id_seq'), primary_key=True)
    school_name = db.Column(db.String, nullable=False)
    program = db.Column(db.String)
    location = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    current = db.Column(db.Boolean)
    duration = db.Column(db.String)

    user_id = db.Column(db.String, db.ForeignKey('LINKEDINUSER.id'))
    user = db.relationship('LINKEDINUSER')

    def __init__(self, school_name, user_id, program, location, start_date, end_date, current, duration):
        self.school_name = school_name
        self.user_id = user_id
        self.program = program
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.current = current
        self.duration = duration

    def json(self):
        return {
            'school_name': self.school_name,
            'user_id': self.user_id,
            'program': self.program,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'current': self.current
            'duration': self.duration}

    @classmethod
    def find_by_school_name(cls, school_name):
        return cls.query.filter_by(school_name=school_name)

    @classmethod
    def find_by_program(cls, program):
        return cls.query.filter_by(program=program)

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
