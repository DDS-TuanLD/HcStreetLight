from sqlalchemy import Float, Integer
from sqlalchemy import Table, Column, String, MetaData


class EventTriggerGroupMapping:
    def __init__(self, metadata: MetaData):
        self.eventTriggerGroupMapping = Table('EventTriggerGroupMapping', metadata,
                                              Column('EventTriggerId', Integer, primary_key=True, nullable=False),
                                              Column('GroupId', Integer, primary_key=True, nullable=False),
                                              )
