from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Time, false
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

"""
TODO implement CASCADE deletes
"""


class Inscription(Base):
    __tablename__ = 'inscriptions'

    calification = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'))

    user = relationship('User', back_populates='inscriptions')

    course = relationship('Course', back_populates='inscriptions')

    group = relationship('Group', back_populates='inscriptions')

    def __repr__(self):
        return f"<Inscription(user= {self.user.name}, course= {self.course.name}, calification= {self.calification})>"


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, default="Unknow")
    locked = Column(Boolean, default=False)

    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    course = relationship('Course', back_populates='groups')

    inscriptions = relationship('Inscription', back_populates='group')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    oauth = Column(Boolean)

    inscriptions = relationship(
        "Inscription",
        back_populates="user",
        cascade="delete, merge, save-update"
    )

    submissions = relationship(
        "Submission",
        back_populates="user",
        cascade="delete, merge, save-update"
    )

    courses_created = relationship(
        'Course',
        back_populates="creator",
        primaryjoin="User.id==Course.user_id",
        cascade="delete, merge, save-update"
    )

    courses_delegate = relationship(
        'Course',
        back_populates="delegate",
        primaryjoin="User.id==Course.delegate_id"
    )

    comments = relationship(
        'Comment',
        back_populates='user',
        cascade="delete, merge, save-update"
    )

    comment_reactions = relationship(
        'CommentReaction',
        back_populates='user',
        cascade="delete, merge, save-update"
    )

    def __repr__(self):
        return f"<User(name= {self.name})>"


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    code = Column(String)

    delegate_id = Column(
        Integer,
        ForeignKey('users.id')
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )

    delegate = relationship(
        'User',
        back_populates='courses_delegate',
        foreign_keys=delegate_id
    )

    creator = relationship(
        'User',
        back_populates="courses_created",
        foreign_keys=user_id
    )

    inscriptions = relationship(
        "Inscription",
        back_populates="course",
        cascade="delete, merge, save-update"
    )

    publications = relationship(
        "Publication",
        back_populates="course",
        cascade="delete, merge, save-update"
    )

    groups = relationship(
        'Group',
        back_populates='course',
        cascade="delete, merge, save-update"
    )

    def __repr__(self):
        return f"<Course(name= {self.name})>"


class Publication(Base):

    """ type = 1: Anuncio, 2: Material, 3: Tarea, 4:Examen """

    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.now().date())
    time = Column(Time, default=datetime.now().time())
    description = Column(String)
    title = Column(String)
    type = Column(Integer, default=1)

    course_id = Column(
        Integer,
        ForeignKey('courses.id'),
        nullable=False
    )

    evaluation_id = Column(
        Integer,
        ForeignKey('evaluations.id')
    )

    course = relationship(
        "Course",
        back_populates="publications"
    )

    evaluation = relationship(
        "Evaluation",
        back_populates="publication",
        cascade="delete, merge, save-update"
    )

    comments = relationship(
        'Comment',
        back_populates='publication',
        cascade="delete, merge, save-update"
    )


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.now().date())
    time = Column(Time, default=datetime.now().time())
    content = Column(String)

    publication_id = Column(
        Integer,
        ForeignKey('publications.id'))

    user_id = Column(
        Integer,
        ForeignKey('users.id'))

    parent_id = Column(
        Integer,
        ForeignKey('comments.id'))

    user = relationship('User')

    publication = relationship(
        'Publication',
        back_populates='comments')

    reply_to = relationship(
        'Comment',
        remote_side=[id])

    comments = relationship(
        'Comment',
        back_populates='reply_to',
        cascade="delete, merge, save-update"
    )

    reactions = relationship(
        'CommentReaction',
        back_populates='comment',
        cascade="delete, merge, save-update"
    )


class CommentReaction(Base):

    """ type = 1: Like 2: Dislike """

    __tablename__ = 'comment_reactions'

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True)

    comment_id = Column(
        Integer,
        ForeignKey('comments.id'),
        primary_key=True)

    type = Column(Integer)

    user = relationship(
        'User',
        back_populates="comment_reactions",
    )

    comment = relationship(
        'Comment',
        back_populates='reactions'
    )


class Evaluation(Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    date_max = Column(Date)
    time_max = Column(Time)
    score_max = Column(Integer)
    group = Column(Boolean, default=False)

    publication = relationship(
        "Publication",
        back_populates="evaluation",
        uselist=False
    )

    submissions = relationship(
        "Submission",
        back_populates="evaluation",
        cascade="delete, merge, save-update"
    )


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.now().date())
    time = Column(Time, default=datetime.now().time())
    calification = Column(Integer, default=0)

    evaluation_id = Column(
        Integer,
        ForeignKey('evaluations.id'),
        nullable=False)

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False)

    evaluation = relationship(
        "Evaluation",
        back_populates="submissions"
    )

    user = relationship(
        "User",
        back_populates="submissions"
    )
