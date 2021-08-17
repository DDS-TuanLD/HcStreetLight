from Database.Db import Db
import logging
from GlobalVariables.GlobalVariables import GlobalVariables


class System:
    __globalVariables = GlobalVariables()
    __logger = logging.Logger
    __db = Db()

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

    def update_devices_online_status_to_global_dict(self):
        devices = self.__db.Services.DeviceService.FindAllDevice()
        if devices is None:
            return
        for device in devices:
            device_address = device['DeviceAddress']
            device_online_status = device['IsOnline']
            self.__globalVariables.devices_online_status_dict[device_address] = device_online_status

    def load_devices_heartbeat_to_global_dict(self):
        devices = self.__db.Services.DeviceService.FindAllDevice()
        if devices:
            return
        for device in devices:
            device_address = device['DeviceAddress']
            device_heartbeat_waiting_count = 0
            self.__globalVariables.devices_heartbeat_dict[device_address] = device_heartbeat_waiting_count

    def update_device_online_status_to_db(self, device_address: str, is_online: bool):
        self.__db.Services.DeviceService.UpdateDeviceByCondition(
            self.__db.Table.DeviceTable.c.DeviceAddress == device_address, {"IsOnline": is_online})


