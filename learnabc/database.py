import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = None

"""
El dino de heroku define una variable de entorno RUN_ON_HEROKU para saber
que lo estamos corriendolo en heroku, las lineas de acontinuacion es verificar
este comportamiento para mostrarlo por consola como un log de la ejecucion de
la aplicacion.

Yields:
    [type]: [description]
"""
# --- pro --- run on heroku
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URI") or 'sqlite:///./learnabc.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not (os.environ.get('RUN_ON_HEROKU') == "TRUE"):
    # --- dev --- run on local
    print("Runs on local")
    engine = create_engine(SQLALCHEMY_DATABASE_URL,  connect_args={
        'check_same_thread': False})

""" 
Creamos una clase de SesionLocal vinculando el engine con el que deseamos 
trabajar, ya sea postgre si estamos en Heroku o SQLite si estamos en local
"""
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

"""
Creamos un objeto Base para declarar posterior mente nuestros modelos de
base de datos usando sqlalchemy.
"""
Base = declarative_base()


def get_db():
    """
    Método para obtener una nueva session a la base de datos.

    Yields:
        [type]: [description]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
