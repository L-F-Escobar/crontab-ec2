from cds.db import database
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cds.models.base import *

engine = database.main()

class Conversation(Base):
    ''' Conversation Data '''
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    prospect_id = Column(Integer, ForeignKey('prospects.id'))
    user_id = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    prospect = relationship('Prospect', backref='prospects')
    messages = relationship('Message', backref='messages')

    def __repr__(self):
        return f'Conversation {self.id}'

class MessageType(Base):
    ''' Message Type Data '''
    __tablename__ = 'message_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relationships
    message_list = relationship('Message', backref='message_list')

    def __repr__(self):
        return f'Message Type {self.name}'

class Message(Base):
    ''' Message Data '''
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    messages_type_id = Column(Integer, ForeignKey('message_types.id'))
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    sid = Column(String(100))
    body = Column(Text)
    outbound = Column(Integer)
    order = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Messages {self.id}'

Base.metadata.create_all(engine)
