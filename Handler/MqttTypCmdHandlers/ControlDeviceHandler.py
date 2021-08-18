from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import logging
import Constants.Constant as Const
import json
from Database.Db import Db
import uuid
from sqlalchemy import and_, bindparam


class ControlDeviceHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()
        rqi = data.get("RQI")
        mqttReceiveCommandResponse = {
            "RQI": rqi
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        devices_control_list: list
        groups_control_list: list

        devices_control_list = data.get("Device", [])
        groups_control_list = data.get("group", [])
        devices_property = []

        for g in groups_control_list:
            rel = db.Services.GroupDeviceMappingService.FindGroupDeviceMappingByCondition(
                db.Table.GroupDeviceMappingTable.c.GroupId == g
            )
            for r in rel:
                devices_control_list.append(r["DeviceAddress"])

        unique_devices_control_list = set(devices_control_list)
        for d in unique_devices_control_list:
            device_dim_property = {
                "b_DeviceAddress": d,
                    "b_PropertyId": Const.PROPERTY_DIM_ID,
                "b_PropertyValue": data.get("DIM")
            }
            device_relay_property = {
                "b_DeviceAddress": d,
                "b_PropertyId": Const.PROPERTY_RELAY_ID,
                "b_PropertyValue": data.get("Relay")
            }
            devices_property.append(device_dim_property)
            devices_property.append(device_relay_property)
        db.Services.DevicePropertyService.UpdateManyDevicePropertyMappingCustomByConditionType1(devices_property)
        self.__cmd_res(data.get("ID"), list(unique_devices_control_list))

    def __cmd_res(self, scene: int, devices: list):
        db = Db()
        res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "ControlDeviceRsp",
            "Devices": [],
        }
        rel = db.Services.DevicePropertyService.FindDevicePropertyMappingByCondition(
            db.Table.DevicePropertyMappingTable.c.DeviceAddress.in_(devices)
        )
        temp = {}
        for device in devices:
            temp[device] = {}

        for r in rel:
            if r["PropertyId"] == Const.PROPERTY_DIM_ID:
                temp[r["DeviceAddress"]]["DIM"] = r["PropertyValue"]
                continue
            if r["PropertyId"] == Const.PROPERTY_RELAY_ID:
                temp[r["DeviceAddress"]]["Relay"] = r["PropertyValue"]
                continue
        for t in temp:
            res["Devices"].append({
                "Device": t,
                "Relay": temp[t]["Relay"],
                "DIM": temp[t]["DIM"]
            })
        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(res))
