import uuid
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
            "TXPower": data.get("TXPower"),
            "DimInit": data.get("DimInit"),
            "VMax": data.get("VMax"),
            "VMin": data.get("VMin"),
            "IMax": data.get("IMax"),
            "IMin": data.get("IMin"),
            "CosMax": data.get("CosMax"),
            "CosMin": data.get("CosMin"),
            "PMax": data.get("Pmax"),
            "PMin": data.get("Pmin"),
            "TMax": data.get("TMax"),
            "TMin": data.get("TMin")
        }

        db.Services.DeviceService.UpdateDeviceByCondition(
            db.Table.DeviceTable.c.DeviceAddress.in_(unique_devices), update_data
        )

        result = {
            "devices_success": unique_devices,
            "devices_failure": []
        }
        self.__cmd_res(result)

    def __cmd_res(self, result: dict):
        db = Db()
        res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "DeviceConfig",
            "Devices": []
        }
        rel = db.Services.DeviceService.FindDeviceByCondition(
            db.Table.DeviceTable.c.DeviceAddress.in_(result["devices_success"])
        )

        for d in rel:
            temp = {
                "Device": d["DeviceAddress"],
                "PRating": d["PRating"],
                "TXPower": d["TXPower"],
                "DimInit": d["DimInit"],
                "VMax": d["VMax"],
                "VMin": d["VMin"],
                "IMax": d["IMax"],
                "IMin": d["IMin"],
                "CosMax": d["CosMax"],
                "CosMin": d["CosMin"],
                "Pmax": d["PMax"],
                "Pmin": d["PMin"],
                "TMax": d["TMax"],
                "TMin": d["TMin"]
            }
            res["Devices"].append(temp)

        self.globalVariable.mqtt_need_response_dict[res["RQI"]] = res
        self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))
