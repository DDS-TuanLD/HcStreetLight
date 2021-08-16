from Table.TableManager import TableManager
from sqlalchemy.engine.base import Connection
from ModelServices.DeviceServices import DeviceServices


class MetaService(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaService, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ServicesManager(metaclass=MetaService):
    def __init__(self, table: TableManager, context: Connection):
        self.__deviceService = DeviceServices(table.DeviceTable, context)

    @property
    def DeviceService(self):
        return self.__deviceService
