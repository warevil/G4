
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from .database import Base


class Curso(Base):
    __tablename__ = "cursos"

    curso_id = Column(Integer,primary_key=True, index=True)
    creador_id=Column(Usuario, ForeignKey("usuarios.usuario_id"))
    titulo = Column(String, index=True)
    descripcion = Column(String)
    owner = relationship("User", back_populates="items")
    


class Grupo(Base):
    __tablename__ = "grupos"

    grupo_id = Column(Integer,primary_key=True, index=True)
    curso_id=Column(Curso, ForeignKey("cursos.curso_id"))
    public_id=Column(Integer)
    owner=relationship("Curso", back_populates="items")

class Comentario(Base):
    __tablename__ = "comentarios"

    comentario_id = Column(Integer,primary_key=True, index=True)
    publicacion_id=Column(Publicacion, ForeignKey("publicaciones.publicacion_id"))
    autor_id=Column(Autor, ForeignKey("autores.autor_id"))
    contenido = Column(String, index=True)
    likes_num = Column(Integer)
    dislikes_num=Column(Integer)
    esRespuesta=Column(Boolean)
    owner1=relationship("Publicacion", back_populates="items")
    owner2=relationship("Autor", back_populates="items")

class Respuesta(Base):
    __tablename__ = "respuestas"

    comentario_id=Column(Comentario, ForeignKey("comentarios.publicacion_id")) 
    respuesta_id=Column(Publicacion, ForeignKey("publicaciones.publicacion_id"))

