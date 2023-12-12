from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

# database url
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://crud:hdoB7WSac90rKCYV@localhost:3306/crud_system'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root@localhost:3306/crud_system'
SQLALCHEMY_DATABASE_URL = "postgresql://crud_zwwh_user:wGzIWXXwyCZ0QGUALvSQXgHmnk4B3PfL@dpg-clgsoieg1b2c73aapuvg-a/crud_zwwh"
# import os
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# SQLALCHEMY_DATABASE_URL = 'sqlite:///'+os.path.join(BASE_DIR,'bazza.db?check_same_thread=False')
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
