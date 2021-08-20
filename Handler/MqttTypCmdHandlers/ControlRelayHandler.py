from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import logging
import json
from Database.Db import Db
import uuid
import Constants.Constant as Const


class ControlRelayHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()
        rqi = data.get("RQI")
        mqttReceiveCommandResponse = {
            "RQI": rqi
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))
        rel = db.Services.GatewayService.FindGatewayById(Const.GATEWAY_ID)
        gateway = rel.fetchone()
        print(str(gateway))
        if gateway is not None:
            db.Services.GatewayService.UpdateGatewayById(Const.GATEWAY_ID, data.get("Control"))
        if gateway is None:
            db.Services.GatewayService.InsertGateway({
                "GatewayId": Const.GATEWAY_ID,
                "Relay_1": data.get("Control").get("Relay_1"),
                "Relay_2": data.get("Control").get("Relay_2"),
                "Relay_3": data.get("Control").get("Relay_3"),
                "Relay_4": data.get("Control").get("Relay_4")
            })

        self.__cmd_res()

    def __cmd_res(self):
        db = Db()
        rel = db.Services.GatewayService.FindGatewayById(Const.GATEWAY_ID)
        gateway = dict(rel.fetchone())
        res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "GWRelayStt",
            "Relay_1": gateway.get("Relay_1"),
            "Relay_2": gateway.get("Relay_2"),
            "Relay_3": gateway.get("Relay_3"),
            "Relay_4": gateway.get("Relay_4")
        }
        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(res))

