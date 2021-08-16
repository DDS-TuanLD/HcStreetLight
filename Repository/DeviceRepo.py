from sqlalchemy import Table
from sqlalchemy.sql.expression import BinaryExpression
from sqlalchemy.engine.base import Connection


class DeviceRepo:
    __deviceTable: Table
    __context: Connection

    def __init__(self, DeviceTable: Table, context: Connection):
        self.__deviceTable = DeviceTable
        self.__context = context

    def FindAll(self):
        ins = self.__deviceTable.select()
        rel = self.__context.execute(ins)
        return rel