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
                            Column('Longitude', String),
                            Column('Latitude', String),
                            Column('TXPower', Integer),
                            Column('VMax', Float),
                            Column('VMin', Float),
                            Column('IMax', Float),
                            Column('IMin', Float),
                            Column('CosMax', Float),
                            Column('CosMin', Float),
                            Column('PMax', Float),
                            Column('PMin', Float),
                            Column('TMax', Integer),
                            Column('TMin', Integer),
                            Column('LMax', Float),
                            Column('LMin', Float),
                            Column('ActiveTime', Integer),
                            Column('CurrentRunningScene', Integer),
                            Column('Status', Integer),
                            Column('IsOnline', Boolean),
                            Column('IsSync', Boolean),
                            Column('DimInit', Integer),
                            Column('PRating', Float),
                            Column('KWH', Float),
                            Column('FirmwareVersion', String),
                            )
