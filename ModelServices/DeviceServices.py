from Repository.DeviceRepo import DeviceRepo
from sqlalchemy import Table
from sqlalchemy.engine.base import Connection


class MetaDeviceServices(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaDeviceServices, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DeviceServices(metaclass=MetaDeviceServices):
    __deviceRepo: DeviceRepo

    def __init__(self, DeviceTable: Table, context: Connection):
        self.__deviceRepo = DeviceRepo(DeviceTable, context)

    def FindAllDevice(self):
        rel = self.__deviceRepo.FindAll()
        return rel