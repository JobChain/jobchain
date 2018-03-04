from sqlalchemy import Column, ForeignKey, Integer, String, MetaData, Date, Boolean, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'LINKEDINUSER'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    def __repr__(self):
       return "<User(id='%s', name='%s')>" % (
                            self.id, self.name)

class Work(Base):
    __tablename__ = 'WORK'
    id = Column(Integer, Sequence('work_id_seq'), primary_key=True)
    company_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    job_title = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    current = Column(Boolean)

    def __repr__(self):
       return "<Work(name='%s', user id='%s', job title='%s')>" % (
                            self.company_name, self.user_id, self.job_title)

class Education(Base):
    __tablename__ = 'EDUCATION'
    id = Column(Integer, Sequence('education_id_seq'), primary_key=True)
    school_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    program = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    current = Column(Boolean)
    duration = Column(String)

    def __repr__(self):
       return "<Education(name='%s', user id='%s', program='%s')>" % (
                            self.school_name, self.user_id, self.program)

class PSQL:
    def __init__(self, psql_username, psql_password):
        print('Opening connection to PSQL DB')
        db_string = "postgresql://" + psql_username + ":" + psql_password + "@jobchain-db.czszo1jjniwj.eu-central-1.rds.amazonaws.com:5432/jobchaindatabase"
        db = create_engine(db_string)
        self.Session = sessionmaker(db)  
        self.session = self.Session()
        Base.metadata.create_all(db)
        print('Opened connection to PSQL DB')
        
    def get_session(self):
        return self.session

