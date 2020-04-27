from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from cds.models.base import *

engine = database.main()

class Opportunity(Base):
    ''' Opportunity '''
    __tablename__ = 'opportunities'

    id = Column(Integer, primary_key=True)
    opportunity_type_id = Column(Integer, ForeignKey('opportunity_types.id'))
    build_vehicle_id = Column(Integer, ForeignKey('build_vehicles.id'))
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    name = Column(Text)
    vehicle_name = Column(Text)
    stock_type = Column(String(100))
    rating = Column(Integer)
    term = Column(Integer)
    apr = Column(Numeric(10,2))
    payments = Column(Numeric(10,2))
    payments_new = Column(Numeric(10,2))
    payments_made = Column(Integer)
    payments_left = Column(Integer)
    trade = Column(Numeric(10,2))
    equity = Column(Numeric(10,2))
    matches = Column(Integer)
    distance = Column(Numeric(10,2))
    warranty = Column(Text)
    warranty_mileage = Column(Integer)
    warranty_months = Column(Integer)
    service_last = Column(Numeric(10,2))
    service_total = Column(Numeric(10,2))
    appointment_at = Column(TIMESTAMP)
    serviced_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    type = relationship('OpportunityType', backref='opportunity_types')
    customer = relationship('Customer', backref='customers')
    vehicle = relationship('Vehicle', backref='vehicles')
    replacement = relationship('BuildVehicle', backref='build_vehicles')

    def __repr__(self):
        return f'Opportunity Type {self.id}'

class OpportunityType(Base):
    ''' Opportunity Types '''
    __tablename__ = 'opportunity_types'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    opportunities = relationship('Opportunity', backref='opportunities')

    def __repr__(self):
        return f'Opportunity Type {self.id}'

Base.metadata.create_all(engine)
