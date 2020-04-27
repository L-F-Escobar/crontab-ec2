from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cds.models.base import *

engine = database.main()

class Prospect(Base):
    ''' Prospect Data '''
    __tablename__ = 'prospects'

    id = Column(Integer, primary_key=True)
    number = Column(Text)
    type = Column(String(2))
    full_name = Column(Text)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name = Column(Text)
    address = Column(Text)
    city = Column(Text)
    province = Column(Text)
    country = Column(Text)
    postal_code = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    contact = relationship('ProspectContact', backref='prospect_contact')

    def __repr__(self):
        return f'Prospect {self.full_name}'

class ProspectContact(Base):
    ''' Prospect Contact Details '''
    __tablename__ = 'prospect_contact'

    id = Column(Integer, primary_key=True)
    prospect_id = Column(Integer, ForeignKey('prospects.id'))
    home = Column(String(100))
    cell = Column(String(100))
    work = Column(String(100))
    email = Column(String(100))
    can_mail = Column(Integer)
    can_email = Column(Integer)
    can_call = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Prospect Contact {self.id}'

Base.metadata.create_all(engine)
