from sqlalchemy import Float, Integer
from sqlalchemy import Table, Column, String, MetaData


class EventTriggerDeviceSetupValue:
    def __init__(self, metadata: MetaData):
        self.eventTriggerDeviceSetupValue = Table('EventTriggerDeviceSetupValue', metadata,
                                                  Column('EventTriggerId', Integer, primary_key=True, nullable=False),
                                                  Column('DeviceAddress', String, primary_key=True, nullable=False),
                                                  Column('PropertyId', Integer),
                                                  Column('PropertyValue', Float),
                                                  )
