from sqlalchemy import Float
from sqlalchemy import Table, Column, String, MetaData


class Network:
    def __init__(self, metadata: MetaData):
        self.network = Table('Network', metadata,
                             Column('NetworkId', String, primary_key=True, nullable=False),
                             Column('NetworkType', String),
                             Column('NetworkKey', String),
                             Column('TXPower', Float),
                             Column('GatewayMac', String),
                             Column('FirmwareVersion', String),
                             )
