from sqlalchemy import Float, Boolean, Integer
from sqlalchemy import Table, Column, String, MetaData


class Device:
    def __init__(self, metadata: MetaData):
        self.device = Table('Device', metadata,
                            Column('DeviceAddress', String, primary_key=True, nullable=False),
                            Column('Ip', String),
                            Column('NetKey', String),
                            Column('PanId_1', String),
                            Column('PanId_2', String),
                            Column('Longitude', Float),
                            Column('Latitude', Float),
                            Column('Longitude', Float),
                            Column('TXPower', Float),
                            Column('VMax', Float),
                            Column('VMin', Float),
                            Column('IMax', Float),
                            Column('IMin', Float),
                            Column('CosMax', Float),
                            Column('CosMin', Float),
                            Column('PMax', Float),
                            Column('PMin', Float),
                            Column('TMax', Float),
                            Column('TMin', Float),
                            Column('LMax', Float),
                            Column('LMin', Float),
                            Column('ActiveTime', Integer),
                            Column('Relay', Boolean),
                            Column('IsBroken', Boolean),
                            Column('IsOnline', Boolean),
                            Column('IsSync', Boolean),
                            Column('DimInit', Integer),
                            Column('PRating', Float),
                            Column('KWH', Integer),
                            Column('FirmwareVersion', String),
                            )
