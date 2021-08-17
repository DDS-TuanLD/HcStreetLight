from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
from Database.Db import Db
import logging


class DelDevHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()
        try:
            devices = data["Device"]
        except:
            devices = []

        db.Services.DeviceService.RemoveManyDeviceByDeviceAddress(devices)

