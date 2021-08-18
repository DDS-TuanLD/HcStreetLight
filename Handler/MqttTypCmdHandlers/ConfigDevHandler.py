from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import logging
import Constants.Constant as Const
import json
from Database.Db import Db


class ConfigDevHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()

        mqttReceiveCommandResponse = {
            "RQI": data.get("RQI")
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        groups: list
        devices: list

        groups = data.get("Group", [])
        devices = data.get("Device", [])

        for group in groups:
            rel = db.Services.GroupDeviceMappingService.FindGroupDeviceMappingByCondition(
                db.Table.GroupDeviceMappingTable.c.GroupId == group
            )

            for r in rel:
                devices.append(r["DeviceAddress"])

        unique_devices = set(devices)
        update_data = {
            "PRating": data.get("PRating"),
            "TxPower": data.get("TXPower"),
            "DimInit": data.get("DimInit"),
            "Umax": data.get("VMax"),
            "Umin": data.get("VMin"),
            "Imax": data.get("IMax"),
            "Imin": data.get("IMin"),
            "Cosmax": data.get("CosMax"),
            "Cosmin": data.get("CosMin"),
            "Pmax": data.get("Pmax"),
            "Pmin": data.get("Pmin"),
            "Tmax": data.get("TMax"),
            "Tmin": data.get("TMin")
        }

        db.Services.DeviceService.UpdateDeviceByCondition(
            db.Table.DeviceTable.c.DeviceAddress.in_(unique_devices), update_data
        )

    def __cmd_res(self):
        pass
