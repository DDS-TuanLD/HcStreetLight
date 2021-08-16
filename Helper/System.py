from Database.Db import Db
import logging
from GlobalVariables.GlobleVariables import GlobalVariables


class System:
    __db = Db()
    __globalVariables = GlobalVariables()
    __logger = logging.Logger

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

    def update_device_online_status_to_global_dicts(self):
        devices = self.__db.Services.DeviceService.FindAllDevice()
        none_of_devices = (devices.first() is None)
        if none_of_devices:
            return
        for device in devices:
            device_address = device['DeviceAddress']
            device_online_status = device['IsOnline']
            self.__globalVariables.device_online_status_dicts[device_address] = device_online_status
