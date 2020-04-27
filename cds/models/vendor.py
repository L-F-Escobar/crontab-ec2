from cds.db import database
from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from cds.models.base import *

engine = database.main()

class Vendor(Base):
    ''' Vendor Information '''
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    logo = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    feeds = relationship('Feed', backref='feeds')

    def __repr__(self):
        return f'Vendor: {self.name}'

class FeedType(Base):
    ''' Feed Types : Sales Service Appointments Customers Inventory'''
    __tablename__ = 'feed_types'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Feed Type: {self.name}'

class Feed(Base):
    ''' Feeds : Represent a file or API transmission from a vendor. Feeds will have FeedType and a Vendor attached to them '''
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    feed_type_id = Column(Integer, ForeignKey('feed_types.id'))
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    name = Column(Text)
    api = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    feed_config = relationship('FeedConfig', backref='feed_config')
    type = relationship('FeedType', backref='feed_types')
    vendor = relationship('Vendor', backref='vendors')

    def __repr__(self):
        return f'Feed id: {self.id}'

class FeedConfig(Base):
    ''' FeedConfig : stores either a flat file that requires FTP creds or an API endpoint that has a key '''
    __tablename__ = 'feed_config'

    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey('feeds.id'))
    option = Column(String(100))
    value = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Feed Config id: {self.feed_id}'

Base.metadata.create_all(engine)
