from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric
from sqlalchemy.ext.declarative import declarative_base
from cds.models.base import *

engine = database.main()

class Dealer(Base):
    ''' Dealer Information '''
    __tablename__ = 'dealers'

    id = Column(Integer, primary_key=True)
    key = Column(String(20))
    name = Column(Text)
    address = Column(Text)
    city = Column(Text)
    province = Column(Text)
    country = Column(Text)
    postal_code = Column(Text)
    brand = Column(Text)
    logo = Column(Text)
    longitude = Column(Text)
    latitude = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    def __repr__(self):
        return f'Dealer {self.name}'

class DealerSetting(Base):
    ''' Dealer Settings '''
    __tablename__ = 'dealer_settings'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Dealer Settings {self.id}'

Base.metadata.create_all(engine)
