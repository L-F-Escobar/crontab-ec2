from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric
from sqlalchemy.ext.declarative import declarative_base

engine = database.main()
Base = declarative_base()

class Appointments(Base):
    ''' Appointment Table '''
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    customer_id = Column(Integer)
    note = Column(Text)
    appointment_time = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Appointment {self.id}'

Base.metadata.create_all(engine)