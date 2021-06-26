from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Inscription(Base):
    __tablename__ = 'inscriptions'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)

    calification = Column(Integer, default=0)

    user = relationship("User", back_populates="inscriptions")
    course = relationship("Course", back_populates="inscriptions")

    def __repr__(self):
        return f"<Inscription(user= {self.user.name}, course= {self.course.name}, calification= {self.calification})>"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    courses_created = relationship('Course', back_populates="creator")
    inscriptions = relationship("Inscription", back_populates="user")
    submissions = relationship("Submission", back_populates="user")

    def __repr__(self):
        return f"<User(name= {self.name})>"


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates="courses_created")
    inscriptions = relationship("Inscription", back_populates="course")
    publications = relationship("Publication", back_populates="course")

    def __repr__(self):
        return f"<Course(name= {self.name})>"


class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.now().date())
    time = Column(Time, default=datetime.now().time())
    description = Column(String)
    title = Column(String)
    type = Column(Integer, default=1)  # 1: Anuncio, 2: Material, 3: Tarea

    course_id = Column(Integer, ForeignKey('courses.id'))
    evaluation_id = Column(Integer, ForeignKey('evaluations.id'))

    course = relationship("Course", back_populates="publications")
    evaluation = relationship(
        "Evaluation", back_populates="publication")


class Evaluation(Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True, index=True)
    date_max = Column(Date)
    time_max = Column(Time)

    # publication_id = Column(Integer, ForeignKey('publications.id'))

    publication = relationship(
        "Publication", back_populates="evaluation", uselist=False)
    submissions = relationship("Submission", back_populates="evaluation")


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.now().date())
    time = Column(Time, default=datetime.now().time())
    calification = Column(Integer, default=0)

    evaluation_id = Column(Integer, ForeignKey('evaluations.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    evaluation = relationship("Evaluation", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
