from sqlalchemy import Float, Integer
from sqlalchemy import Table, Column, String, MetaData


class EventTriggerGroupSetupValue:
    def __init__(self, metadata: MetaData):
        self.eventTriggerGroupSetupValue = Table('EventTriggerGroupSetupValue', metadata,
                                                 Column('EventTriggerId', Integer, primary_key=True, nullable=False),
                                                 Column('GroupId', Integer, primary_key=True, nullable=False),
                                                 Column('PropertyId', Integer),
                                                 Column('PropertyValue', Float),
                                                 )
