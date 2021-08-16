from sqlalchemy import Float, Integer
from sqlalchemy import Table, Column, String, MetaData


class EventTriggerDeviceMapping:
    def __init__(self, metadata: MetaData):
        self.eventTriggerDeviceMapping = Table('EventTriggerDeviceMapping', metadata,
                                               Column('EventTriggerId', Integer, primary_key=True, nullable=False),
                                               Column('DeviceAddress', String, primary_key=True, nullable=False),
                                               )
