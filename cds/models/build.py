from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cds.models.base import *

engine = database.main()

class BuildVehicle(Base):
    ''' Build Vehicles '''
    __tablename__ = 'build_vehicles'

    id = Column(Integer, primary_key=True)
    year = Column(Text)
    make = Column(Text)
    model = Column(Text)
    trim = Column(Text)
    trim_id = Column(Text)
    body_type = Column(Text)
    model_code = Column(Text)
    msrp = Column(Numeric(10,2))
    invoice = Column(Numeric(10,2))
    freight = Column(Numeric(10,2))
    _type = Column('type', Text)
    doors = Column(Text)
    engine = Column(Text)
    horsepower = Column(Text)
    displacement = Column(Text)
    torque = Column(Text)
    fuel = Column(Text)
    transmission = Column(Text)
    drivetrain = Column(Text)
    efficiency_city = Column(Text)
    efficiency_hwy = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    @hybrid_property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = self.get_type(type)

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

    def __repr__(self):
        return f'Build Vehicle {self.year} {self.make} {self.model}'

class BuildVehicleFeature(Base):
    ''' Build Vehicle Features '''
    __tablename__ = 'build_vehicle_features'

    id = Column(Integer, primary_key=True)
    build_vehicle_id = Column(Integer)
    option = Column(Text)
    value = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Build Features {self.name}'

class BuildVehicleWarranty(Base):
    ''' Build Vehicle Warranty '''
    __tablename__ = 'build_vehicle_warranties'

    id = Column(Integer, primary_key=True)
    build_vehicle_id = Column(Integer)
    type = Column(Text)
    value = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Build Warranty {self.name}'

class BuildVehiclePhoto(Base):
    ''' Build Vehicle Photos '''
    __tablename__ = 'build_vehicle_photos'

    id = Column(Integer, primary_key=True)
    build_vehicle_id = Column(Integer)
    type = Column(String(100))
    code = Column(String(5))
    url = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Build Photo {self.url}'

Base.metadata.create_all(engine)
