from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Time
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

    inscriptions = relationship("Inscription", back_populates="user")
    submissions = relationship("Submission", back_populates="user")
    courses_created = relationship(
        'Course', back_populates="creator", primaryjoin="User.id==Course.user_id")
    courses_delegate = relationship(
        'Course', back_populates="delegate", primaryjoin="User.id==Course.delegate_id")

    def __repr__(self):
        return f"<User(name= {self.name})>"


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    delegate_id = Column(Integer, ForeignKey('users.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    inscriptions = relationship("Inscription", back_populates="course")
    publications = relationship("Publication", back_populates="course")
    delegate = relationship(
        'User', back_populates='courses_delegate', foreign_keys=delegate_id)
    creator = relationship(
        'User', back_populates="courses_created", foreign_keys=user_id)

    def __repr__(self):
        return f"<Course(name= {self.name})>"


class Publication(Base):
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.now().date())
    time = Column(Time, default=datetime.now().time())
    description = Column(String)
    title = Column(String)
    # 1: Anuncio, 2: Material, 3: Tarea, 4:Examen
    type = Column(Integer, default=1)

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
    group = Column(Boolean, default=False)

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
