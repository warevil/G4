import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if (os.environ.get('RUN_ON_HEROKU') == "TRUE"):
    print("Runs on Heroku")
    # --- pro ---
    SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URI")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # --- dev ---
    print("Runs on local")
    SQLALCHEMY_DATABASE_URL = 'sqlite:///./learnabc.db'
    engine = create_engine(SQLALCHEMY_DATABASE_URL,  connect_args={
        'check_same_thread': False})


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
