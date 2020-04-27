from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from cds.models.base import *
from sqlalchemy.orm import relationship

engine = database.main()

class Customer(Base):
    ''' Customers '''
    __tablename__ = 'customers'

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
    longitude = Column(Text)
    latitude = Column(Text)
    distance = Column(Text)
    _searchable = Column('searchable', Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    status = relationship('CustomerStatus', backref='customer_status')

    @hybrid_property
    def searchable(self):
        return self._searchable

    @searchable.setter
    def searchable(self, searchable):
        self._searchable = self.get_searchable(searchable)

    def get_searchable(self, searchable):
        valid = ['id', 'created_at', 'updated_at']
        searchable = ''

        for field in self.__table__.columns:
            if str(field).replace('customers.', '') not in valid:
                value = getattr(self, str(field).replace('customers.', ''))
                if value and value != '':
                    searchable = searchable + str(value) + ','

        return searchable

    def __repr__(self):
        return f'Customer {self.full_name}'

class CustomerContact(Base):
    ''' Customer Contact Details '''
    __tablename__ = 'customer_contact'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
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
        return f'Customer Contact {self.id}'

class CustomerVehicle(Base):
    ''' Customer Contact Details '''
    __tablename__ = 'customer_vehicles'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer)
    customer_id = Column(Integer)
    deleted_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Customer Vehicle {self.customer_id} / {self.vehicle_id}'

class CustomerStatus(Base):
    ''' Customer status details '''
    __tablename__ = 'customer_status'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    status = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Customer: {self.customer_id}. Status: {self.status}'

Base.metadata.create_all(engine)
