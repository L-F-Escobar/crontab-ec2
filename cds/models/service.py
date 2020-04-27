from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, Float
from sqlalchemy.ext.declarative import declarative_base
from cds.models.base import *

engine = database.main()

class Service(Base):
    ''' Service Entries '''
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer)
    customer_id = Column(Integer)
    ro = Column(Text)
    description = Column(Text)
    mileage = Column(Text)
    total = Column(Numeric(10,2))
    total_labour = Column(Numeric(10,2))
    total_parts = Column(Numeric(10,2))
    total_warranty = Column(Numeric(10,2))
    opened_at = Column(Text)
    completed_at = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Service {self.id}'

class ServiceAppointment(Base):
    ''' Service Entries '''
    __tablename__ = 'service_appointments'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer)
    customer_id = Column(Integer)
    number = Column(Text)
    appointment_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Service Appointent {self.number}'

Base.metadata.create_all(engine)
