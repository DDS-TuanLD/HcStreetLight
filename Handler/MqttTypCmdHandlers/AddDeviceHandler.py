import uuid
from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import logging
import Constants.Constant as Const
import json
from Database.Db import Db


class AddDeviceHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()
        rqi = data.get("RQI")
        mqttReceiveCommandResponse = {
            "RQI": rqi
        }
        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        current_devices_list = []

        rel = db.Services.DeviceService.FindAllDevice()
        devices_record = rel.fetchall()
        for d in devices_record:
            current_devices_list.append(d["DeviceAddress"])
        devices_add = list(set(data.get("Device", [])) - set(current_devices_list))
        devices_same = list(set(data.get("Device", [])).intersection(current_devices_list))
        devices_data_add = []
        devices_property_mapping_add = []
        if devices_add:
            for d in devices_add:
                devices_data_add.append({
                    'DeviceAddress': d,
                    'Ip': "",
                    'NetKey': "",
                    'PanId_1': "",
                    'PanId_2': "",
                    'Longitude': "0",
                    'Latitude': "0",
                    'TXPower': int(),
                    'VMax': float(),
                    'VMin': float(),
                    'IMax': float(),
                    'IMin': float(),
                    'CosMax': float(),
                    'CosMin': float(),
                    'PMax': float(),
                    'PMin': float(),
                    'TMax': int(),
                    'TMin': int(),
                    'LMax': float(),
                    'LMin': float(),
                    'ActiveTime': int(),
                    'CurrentRunningScene': int(),
                    'Status': int(),
                    'IsOnline': False,
                    'IsSync': True,
                    'DimInit': int(),
                    'PRating': int(),
                    'KWH': float(),
                    'FirmwareVersion': "1.1",
                })
                devices_property_mapping_add.append({
                    "DeviceAddress": d,
                    "PropertyId": Const.PROPERTY_RELAY_ID,
                    "PropertyValue": 0
                })
                devices_property_mapping_add.append({
                    "DeviceAddress": d,
                    "PropertyId": Const.PROPERTY_DIM_ID,
                    "PropertyValue": 0
                })

            db.Services.DeviceService.InsertMany(devices_data_add)
            db.Services.DevicePropertyService.InsertManyDevicePropertyMapping(devices_property_mapping_add)
        r = {
            "devices_same": devices_same,
            "devices_add": devices_add
        }
        self.__cmd_res(r)

    def __cmd_res(self, r: dict):
        db = Db()
        for d in r["devices_add"]:
            res = {
                "RQI": str(uuid.uuid4()),
                "TYPCMD": "NewDevice",
                "Device": d,
                "GPS": {
                    "Lat": "0",
                    "Long": "0"
                },
                "TXPower": 0,
                "FirmVer": "1.1"
            }

            self.globalVariable.mqtt_need_response_dict[res["RQI"]] = res
            self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))

        rel = db.Services.DeviceService.FindDeviceByCondition(
            db.Table.DeviceTable.c.DeviceAddress.in_(r["devices_same"])
        )
        devices = rel.fetchall()
        for d in devices:
            res = {
                "RQI": str(uuid.uuid4()),
                "TYPCMD": "NewDevice",
                "Device": d["DeviceAddress"],
                "GPS": {
                    "Lat": d["Latitude"],
                    "Long": d["Longitude"]
                },
                "TXPower": d["TXPower"],
                "FirmVer": d["FirmwareVersion"]
            }

            self.globalVariable.mqtt_need_response_dict[res["RQI"]] = res
            self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))

