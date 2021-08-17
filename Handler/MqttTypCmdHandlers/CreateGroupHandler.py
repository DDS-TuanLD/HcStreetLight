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
        try:
            groupId = data["GroupID"]
        except:
            groupId = ""

        try:
            devices = data["Device"]
        except:
            devices = []

        if groupId is None or devices is None:
            return

        db.Services.GroupService.InsertGroup({"GroupId": groupId})

        group_device_mapping_dict_list = []
        for device in devices:
            group_device_mapping = {
                "GroupId": groupId,
                "DeviceAddress": device
            }
            group_device_mapping_dict_list.append(group_device_mapping)
        db.Services.GroupDeviceMappingService.InsertManyGroupDeviceMapping(group_device_mapping_dict_list)


