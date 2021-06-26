from sqlalchemy import Column, Integer, String, ForeignKey, Table
from ...database import Base
from ..user.models import UserCourses
from sqlalchemy.orm import relationship
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates="courses_created")
    users_enrolled = relationship(
        'User', secondary=UserCourses, back_populates="courses_enrolled")