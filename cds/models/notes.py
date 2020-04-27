from cds.db import database
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

engine = database.main()
Base = declarative_base()

class Note(Base):
    ''' Customer / Prospect Note Table '''
    __tablename__ = 'customer_notes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    customer_id = Column(Integer)
    prospect_id = Column(Integer)
    note = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Note {self.id}:{self.note}'

Base.metadata.create_all(engine)
