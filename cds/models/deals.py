from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from cds.models.base import *

engine = database.main()

class Deal(Base):
    ''' Deal Data '''
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    customer_id = Column(Integer)
    number = Column(Text)
    type = Column(Text)
    mileage = Column(Text)
    price = Column(Numeric(10,2))
    cost = Column(Numeric(10,2))
    journal_amount = Column(Numeric(10,2))
    journal_cost = Column(Numeric(10,2))
    adjustments = Column(Numeric(10,2))
    adjusted_cost = Column(Numeric(10,2))
    trade_value = Column(Numeric(10,2))
    trade_gross = Column(Numeric(10,2))
    incentives = Column(Numeric(10,2))
    sold_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    financing = relationship('DealFinancing', backref='deal_financing', uselist=False)

    def __repr__(self):
        return f'Deal {self.id}'

class DealFinancing(Base):
    ''' Deal Financing Data '''
    __tablename__ = 'deal_financing'

    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey('deals.id'))
    type = Column(Text)
    bank_number = Column(Text)
    bank_name = Column(Text)
    bank_address = Column(Text)
    term = Column(Integer)
    rate = Column(Numeric(10,2))
    frequency = Column(Text)
    payment = Column(Numeric(10,2))
    amount = Column(Numeric(10,2))
    downpayment = Column(Numeric(10,2))
    capital_cost = Column(Numeric(10,2))
    residual_rate = Column(Numeric(10,2))
    residual_amount = Column(Numeric(10,2))
    mileage_allowed = Column(Numeric(10,2))
    mileage_rate = Column(Numeric(10,2))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Deal Finaning {self.id}'

class DealTrade(Base):
    __tablename__ = 'deal_trades'

    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer)
    vehicle_id = Column(Integer)
    vin = Column(Text)
    year = Column(Text)
    make = Column(Text)
    model = Column(Text)
    trim = Column(Text)
    mileage = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Deal Trade In {self.id}'

class DealCoBuyer(Base):
    __tablename__ = "deal_cobuyers"

    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer)
    first_name = Column(Text)
    last_name = Column(Text)
    full_name = Column(Text)
    address = Column(Text)
    city = Column(Text)
    province = Column(Text)
    country = Column(Text)
    postal_code = Column(Text)
    home = Column(Text)
    cell = Column(Text)
    work = Column(Text)
    email = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Deal CoBuyer {self.full_name}'

class DealEmployee(Base):
    __tablename__ = 'deal_employees'

    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer)
    type = Column(String(100))
    number = Column(Text)
    name = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Deal Employee {self.name}'

class DealWarranty(Base):
    ''' Deal Additional Warranty Data '''
    __tablename__ = 'deal_warranties'

    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer)
    name = Column(Text)
    term = Column(Integer)
    mileage = Column(Integer)
    sale = Column(Numeric(10,2))
    cost = Column(Numeric(10,2))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Deal Warranty {self.name}'

Base.metadata.create_all(engine)
