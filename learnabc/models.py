from sqlalchemy import Column, Integer, String, ForeignKey, Table
from .database import Base
from sqlalchemy.orm import relationship


UserCourses = Table(
    'usercourse', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    courses_created = relationship('Course', back_populates="creator")
    courses_enrolled = relationship(
        'Course', secondary=UserCourses, back_populates="users_enrolled")


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates="courses_created")
    users_enrolled = relationship(
        'User', secondary=UserCourses, back_populates="courses_enrolled")
