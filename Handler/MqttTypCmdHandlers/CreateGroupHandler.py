import uuid
from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
from Database.Db import Db
import logging
import json
import Constants.Constant as Const


class CreateGroupHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        mqttReceiveCommandResponse = {
            "RQI": data["RQI"]
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        db = Db()
        groupId = data.get("GroupID")
        devices = data.get("Device", [])

        rel = db.Services.GroupService.FindGroupByCondition(
            db.Table.GroupTable.c.GroupId == groupId
        )
        group = rel.fetchone()

        if group is None:
            db.Services.GroupService.InsertGroup({"GroupId": groupId})

        group_device_mapping_dict_list = []
        for device in devices:
            group_device_mapping = {
                "GroupId": groupId,
                "DeviceAddress": device
            }
            group_device_mapping_dict_list.append(group_device_mapping)
        db.Services.GroupDeviceMappingService.InsertManyGroupDeviceMapping(group_device_mapping_dict_list)

        r = {
            "devices_success": devices,
            "devices_failure": []
        }
        self.__cmd_res(groupId, r)

    def __cmd_res(self, group: int, rel: dict):
        res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "CreateGroupRsp",
            "GroupID": group,
            "Devices": []
        }
        for d in rel.get("devices_success", []):
            device = {
                "Device": d,
                "Success": True
            }
            res["Devices"].append(device)
        for d in rel.get("devices_failure", []):
            device = {
                "Device": d,
                "Success": False
            }
            res["Devices"].append(device)
        self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))

