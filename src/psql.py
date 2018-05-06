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

class CheckedUser(Base):
    __tablename__ = 'CHECKEDUSER'

    id = Column(String, primary_key=True)
    def __repr__(self):
       return "<User(id='%s')>" % (
                            self.id)

class Company(Base):
    __tablename__ = 'COMPANY'

    id = Column(String, primary_key=True)
    logo = Column(String)
    url = Column(String)

    def __repr__(self):
        return "<Company(id='%s', logo='%s', url='%s')>" %(
                            self.id, self.logo, self.url)

class PSQL:
    def __init__(self, psql_username, psql_password, psql_address, psql_db):
        print('Opening connection to PSQL DB')
        db_string = "postgresql://" + psql_username + ":" + psql_password + "@" + psql_address + ":5432/" + psql_db
        self.db = create_engine(db_string)
        self.Session = sessionmaker(self.db)
        self.session = self.Session()
        print('Test')
        Base.metadata.create_all(self.db)
        print('Opened connection to PSQL DB')

    def reset(self):
        print(Fore.RED + 'Deleting all rows in db' + Style.RESET_ALL)
        self.db.execute('REMOVE FROM "LINKEDINUSER";')
        self.db.execute('REMOVE FROM "WORK";')
        self.db.execute('REMOVE FROM "EDUCATION";')
        self.db.execute('REMOVE FROM "CHECKEDUSER";')
        print(Fore.GREEN + 'Deleted' + Style.RESET_ALL)