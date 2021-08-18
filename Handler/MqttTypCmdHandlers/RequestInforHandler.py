import uuid

from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
from Database.Db import Db
import logging
import json
import Constants.Constant as Const


class RequestInforHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()

        mqttReceiveCommandResponse = {
            "RQI": data["RQI"]
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        rel = db.Services.DeviceService.FindAllDevice()
        devices = rel.fetchall()
        devices_info = []
        if devices is not None:
            for device in devices:
                device_info = {
                    "Device": device["DeviceAddress"],
                    "GPS": {
                        "Lat": device["Latitude"],
                        "Long": device["Longitude"]
                    },
                    "TXPower": device["TxPower"],
                    "FirmVer": device["FirmwareVersion"]
                }
                devices_info.append(device_info)
        self.__cmd_res(devices_info)

    def __cmd_res(self, devices_info: list):
        mes_res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "RequestInforRsp",
            "Devices": devices_info
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mes_res))

