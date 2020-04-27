from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = database.main()
Base = declarative_base()

class User(Base):
    '''  User information and configuration settings for use throughout the site. '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    password = Column(String(200))
    user_id = Column(Integer)
    phone = Column(Text)
    photo = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    config = relationship('UserConfig', backref='user_config')

    def __repr__(self):
        return f'User {self.id}'

class UserConfig(Base):
    '''  User information and configuration settings for use throughout the site. '''
    __tablename__ = 'user_config'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    option = Column(Text)
    vale = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'UserConfig {self.id}'

Base.metadata.create_all(engine)
