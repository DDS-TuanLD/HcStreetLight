from sqlalchemy import Float, Boolean
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
                            Column('TxPower', Float),
                            Column('Umax', Float),
                            Column('Umin', Float),
                            Column('Imax', Float),
                            Column('Imin', Float),
                            Column('Cosmax', Float),
                            Column('Cosmin', Float),
                            Column('Pmax', Float),
                            Column('Pmin', Float),
                            Column('Tmax', Float),
                            Column('Tmin', Float),
                            Column('Lmax', Float),
                            Column('Lmin', Float),
                            Column('FirmwareVersion', Float),
                            Column('IsOnline', Boolean),
                            Column('IsSync', Boolean),
                            )
