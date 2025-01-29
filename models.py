from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime,  Boolean, Float

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default='user')
    phone_number = Column(String)
     
    

class Todos(Base):
    __tablename__ = 'todos'  
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean,default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    