from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = database.main()
Base = declarative_base()

class Alert(Base):
    ''' Alert '''
    __tablename__ = 'alert'

    id = Column(Integer, primary_key=True)
    alert_type_id = Column(Integer, ForeignKey('alert_types.id'))
    user_id = Column(Integer)
    message = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    type = relationship('AlertType', backref='alert_types')

    def __repr__(self):
        return f'Alert {self.id}'

class AlertType(Base):
    ''' Alert Types '''
    __tablename__ = 'alert_types'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    alerts = relationship('Alert', backref='alert')

    def __repr__(self):
        return f'Alert Type {self.id}'

Base.metadata.create_all(engine)