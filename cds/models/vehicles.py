from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from cds.models.base import *

engine = database.main()

class Vehicle(Base):
    ''' Vehicles '''
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    vin = Column(Text)
    stock = Column(Text)
    stock_type = Column(Text)
    year = Column(Text)
    make = Column(Text)
    model = Column(Text)
    trim = Column(Text)
    trim_id = Column(Text)
    price = Column(Numeric(10, 2))
    cost = Column(Numeric(10, 2))
    invoice = Column(Numeric(10, 2))
    msrp = Column(Numeric(10, 2))
    holdback = Column(Numeric(10, 2))
    model_code = Column(Text)
    package_code = Column(Text)
    _type = Column('type', Text)
    body_type = Column(Text)
    engine = Column(Text)
    horsepower = Column(Text)
    displacement = Column(Text)
    drivetrain = Column(Text)
    fuel = Column(Text)
    doors = Column(Text)
    ext_color = Column(Text)
    int_color = Column(Text)
    _transmission = Column('transmission', Text)
    kilometres = Column(Text)
    efficiency_city = Column(Text)
    efficiency_hwy = Column(Text)
    photo = Column(Text)
    _searchable = Column('searchable', Text)
    decoded_at = Column(TIMESTAMP)
    stocked_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Deal
    deal = relationship('Deal', backref='vehicle', uselist=False)

    def __repr__(self):
        return f'Vehicle - {self.vin}'

    @hybrid_property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = self.get_type(type)

    @hybrid_property
    def transmission(self):
        return self._transmission

    @transmission.setter
    def transmission(self, transmission):
        self._transmission = self.get_transmission(transmission)

    @hybrid_property
    def searchable(self):
        return self._searchable

    @type.setter
    def searchable(self, searchable):
        self._searchable = self.get_searchable(searchable)

    def get_type(self, type):
        types = {
            'SUV'   : 'SUV',
            'TRUCK' : 'Truck',
            'SEDAN' : 'Car',
            'HATCH' : 'Car',
            'VAN'   : 'Van'
        }

        for key, value in types.items():
            if key in type.upper():
                return value

        return ''

    def get_searchable(self, searchable):
        valid = ['id', 'photo', 'decoded_at', 'created_at', 'updated_at', 'deleted_at']
        searchable = ''

        for field in self.__table__.columns:
            if str(field).replace('vehicles.', '') not in valid:
                value = getattr(self, str(field).replace('vehicles.', ''))
                if value and value != '':
                    searchable = searchable + str(value) + ','

        return searchable

    def get_transmission(self, transmission):
        if 'MANU' in transmission.upper():
            return 'Manual'

        return "Automatic"

class VehicleFeature(Base):
    ''' Vehicle Feature Table '''
    __tablename__ = 'vehicle_features'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    option = Column(Text)
    value = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Vehicle Feature - {self.type}'

class VehicleValue(Base):
    ''' Vehicle Valuation Table '''
    __tablename__ = 'vehicle_values'

    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer)
    value = Column(Numeric(10, 2))
    great = Column(Numeric(10, 2))
    good = Column(Numeric(10, 2))
    average = Column(Numeric(10, 2))
    rough = Column(Numeric(10, 2))
    active = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Vehicle Valuation - {self.value}'

Base.metadata.create_all(engine)
