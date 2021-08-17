from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import logging
import json
import Constants.Constant as Const
from Database.Db import Db
from sqlalchemy import and_


class DelDevFrGroupHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        mqttReceiveCommandResponse = {
            "RQI": data["RQI"]
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        db = Db()

        devices = data["Device"]
        groupId = data["GroupID"]

        db.Services.GroupDeviceMappingService.RemoveGroupDeviceMappingByCondition(
            and_(db.Table.GroupDeviceMappingTable.c.GroupId == groupId,
                 db.Table.GroupDeviceMappingTable.c.DeviceAddress.in_(devices)
                 )
        )