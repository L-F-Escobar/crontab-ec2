from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cds.models.base import *

engine = database.main()

class Lead(Base):
    ''' Lead Data '''
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True)
    prospect_id = Column(Integer, ForeignKey('prospects.id'))
    full_name = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    body = Column(Text)
    lead = Column(Text)
    submitted_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    prospect = relationship('Prospect', backref='prospect')

    def __repr__(self):
        return f'Lead {self.id}'

Base.metadata.create_all(engine)
