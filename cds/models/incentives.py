from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, Float
from sqlalchemy.ext.declarative import declarative_base
from cds.models.base import *

engine = database.main()

class Incentive(Base):
    ''' Incentive Program Details '''
    __tablename__ = 'incentives'

    id = Column(Integer, primary_key=True)
    program = Column(Text)
    type = Column(String(100))
    incentive = Column(Text)
    year = Column(Text)
    make = Column(Text)
    model = Column(Text)
    trim = Column(Text)
    trim_id = Column(String(100))
    term = Column(Integer)
    rate = Column(Numeric(10,2))
    residual = Column(Numeric(10,2))
    factor = Column(Float(28))
    cash = Column(Numeric(10,2))
    active = Column(Integer)
    start_at = Column(TIMESTAMP)
    end_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Incentive {self.name}'

Base.metadata.create_all(engine)
