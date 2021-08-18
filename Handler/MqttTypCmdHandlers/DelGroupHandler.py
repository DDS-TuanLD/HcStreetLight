from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import logging
import Constants.Constant as Const
import json
from Database.Db import Db
import uuid


class DelGroupHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()
        rqi = data.get("RQI")
        mqttReceiveCommandResponse = {
            "RQI": rqi
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        group_delete = data.get("GroupID")
        db.Services.GroupDeviceMappingService.RemoveGroupDeviceMappingByCondition(
            db.Table.GroupDeviceMappingTable.c.GroupId == group_delete
        )
        self.__cmd_res(group_delete)

    def __cmd_res(self, group: int):
        res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "DelGroupRsp",
            "GroupID": group,
            "Success": True
        }
        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(res))

