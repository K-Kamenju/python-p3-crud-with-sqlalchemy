#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        # Assigns a primary key to every id 
        PrimaryKeyConstraint(
            "id",
            name = "id_pk"
        ),
        # checks new records to ensure they dont match existing records
        UniqueConstraint(
            "email",
            name = "unique_email"
        ),
        #  Check for certain conditions to be met
        CheckConstraint(
            "grade BETWEEN 1 AND 12",
            name = "grade BETWEEN 1 AND 12"
        )
    )
    #  Assigns an index to every entry
    Index("index_name", "name")

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    # determines their standard output value
    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        student_name="Alan Turing",
        student_email="alan.turing@sherborne.edu",
        student_grade=11,
        student_birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )
    
    session.bulk_save_objects([albert_einstein, alan_turing]) # adds the new students to the session
    session.commit() # saves any changes in the database

    print(f"New student ID is {albert_einstein.id}.")