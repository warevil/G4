from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from .database import Base


class Publicacion(Base):
    __tablename__ = "publicaciones"


    publicacion_id = Column(Integer, primary_key=True, index=True)

    autor
    curso
    titulo = Column(String, index=True)
    descripcion = Column(String, index=True)


    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"


    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)

    description = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))


    owner = relationship("User", back_populates="items")


class Item(Base):
    __tablename__ = "items"


    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)

    description = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))


    owner = relationship("User", back_populates="items")
