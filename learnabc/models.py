from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Time, false
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


USERS_ID = "users.id"
COURSES_ID = "courses.id"
DEL_MER_SAVEUPDATE =  "delete, merge, save-update"

class Inscription(Base):
    """
    Modelo para la tabla inscriptiones

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """
    __tablename__ = 'inscriptions'

    calification = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey(USERS_ID), primary_key=True)

    course_id = Column(Integer, ForeignKey(COURSES_ID), primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'))

    user = relationship('User', back_populates='inscriptions')

    course = relationship('Course', back_populates='inscriptions')

    group = relationship('Group', back_populates='inscriptions')

    def __repr__(self):
        """
        metodo para representar la clase en un string

        Returns:
            [type]: [description]
        """

        return f"<Inscription(user= {self.user.name}, course= {self.course.name}, calification= {self.calification})>"


class Group(Base):
    """
    Modelo para la tabla grupos

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, default="Unknow")
    locked = Column(Boolean, default=False)

    course_id = Column(Integer, ForeignKey(COURSES_ID), nullable=False)

    course = relationship('Course', back_populates='groups')

    inscriptions = relationship('Inscription', back_populates='group')


class User(Base):
    """
    Modelo para la tabla usuarios

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    oauth = Column(Boolean, default=False)
    phone = Column(String, default='sin número')
    link = Column(String, default='sin enlace')

    inscriptions = relationship(
        "Inscription",
        back_populates="user",
        cascade=DEL_MER_SAVEUPDATE
    )

    submissions = relationship(
        "Submission",
        back_populates="user",
        cascade=DEL_MER_SAVEUPDATE
    )

    courses_created = relationship(
        'Course',
        back_populates="creator",
        primaryjoin="User.id==Course.user_id",
        cascade=DEL_MER_SAVEUPDATE
    )

    courses_delegate = relationship(
        'Course',
        back_populates="delegate",
        primaryjoin="User.id==Course.delegate_id"
    )

    comments = relationship(
        'Comment',
        back_populates='user',
        cascade=DEL_MER_SAVEUPDATE
    )

    comment_reactions = relationship(
        'CommentReaction',
        back_populates='user',
        cascade=DEL_MER_SAVEUPDATE
    )

    def __repr__(self):
        """
        metodo para representar la clase en un string

        Returns:
            [type]: [description]
        """

        return f"<User(name= {self.name})>"


class Course(Base):
    """
    Modelo para la tabla cursos

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    code = Column(String)

    delegate_id = Column(
        Integer,
        ForeignKey(USERS_ID)
    )

    user_id = Column(
        Integer,
        ForeignKey(USERS_ID),
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
        cascade=DEL_MER_SAVEUPDATE
    )

    publications = relationship(
        "Publication",
        back_populates="course",
        cascade=DEL_MER_SAVEUPDATE
    )

    groups = relationship(
        'Group',
        back_populates='course',
        cascade=DEL_MER_SAVEUPDATE
    )

    def __repr__(self):
        """
        metodo para representar la clase en un string

        Returns:
            [type]: [description]
        """

        return f"<Course(name= {self.name})>"


class Publication(Base):
    """
    Modelo para la tabla publicaciones

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """

    """ type = 1: Anuncio, 2: Material, 3: Tarea, 4:Examen """

    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=lambda: datetime.now().date())
    time = Column(Time, default=lambda: datetime.now().time())
    description = Column(String)
    title = Column(String)
    type = Column(Integer, default=1)

    course_id = Column(
        Integer,
        ForeignKey(COURSES_ID),
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
        cascade=DEL_MER_SAVEUPDATE
    )

    comments = relationship(
        'Comment',
        back_populates='publication',
        cascade=DEL_MER_SAVEUPDATE
    )


class Comment(Base):
    """
    Modelo para la tabla comentarios

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=lambda: datetime.now().date())
    time = Column(Time, default=lambda: datetime.now().time())
    content = Column(String)

    publication_id = Column(
        Integer,
        ForeignKey('publications.id'))

    user_id = Column(
        Integer,
        ForeignKey(USERS_ID))

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
        cascade=DEL_MER_SAVEUPDATE
    )

    reactions = relationship(
        'CommentReaction',
        back_populates='comment',
        cascade=DEL_MER_SAVEUPDATE
    )


class CommentReaction(Base):
    """
    Modelo para la tabla de reacciones a comentarios, tal como
    like o dislike

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """

    """ type = 1: Like 2: Dislike """

    __tablename__ = 'comment_reactions'

    user_id = Column(
        Integer,
        ForeignKey(USERS_ID),
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
        cascade=DEL_MER_SAVEUPDATE
    )


class Submission(Base):
    """
    Modelo para la tabla de los envios de los estudiantes

    Args:
        Base ([type]): [description]

    Returns:
        [type]: [description]
    """
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=lambda: datetime.now().date())
    time = Column(Time, default=lambda: datetime.now().time())
    calification = Column(Integer, default=0)

    evaluation_id = Column(
        Integer,
        ForeignKey('evaluations.id'),
        nullable=False)

    user_id = Column(
        Integer,
        ForeignKey(USERS_ID),
        nullable=False)

    evaluation = relationship(
        "Evaluation",
        back_populates="submissions"
    )

    user = relationship(
        "User",
        back_populates="submissions"
    )
