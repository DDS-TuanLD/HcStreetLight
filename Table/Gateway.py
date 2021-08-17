from sqlalchemy import Integer, Boolean
from sqlalchemy import Table, Column, String, MetaData


class Gateway:
    def __init__(self, metadata: MetaData):
        self.gateway = Table('Gateway', metadata,
                             Column('GatewayId', Integer, primary_key=True, nullable=False),
                             Column('Relay_1', Boolean),
                             Column('Relay_2', Boolean),
                             Column('Relay_3', Boolean),
                             Column('Relay_4', Boolean)
                             )
