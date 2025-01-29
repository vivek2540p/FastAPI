from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db'
# SQLALCHEMY_DATABASE_URL='postgresql://postgres:1234@localhost/TodoAppDatabase'
# SQLALCHEMY_DATABASE_URL='mysql+pymysql://root:1234@127.0.0.1:3307/TodoAppDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
