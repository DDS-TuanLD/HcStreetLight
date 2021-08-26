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
        relays_control = data.get("Control").get("RelayID", [])
        print(relays_control)
        r = {}
        for relay in relays_control:
            relay_name = "Relay_" + str(relay)
            print(relay_name)
            r[relay_name] = data.get("Control").get("Relay")
        print(r)
        self.__cmd_res(r)

    def __cmd_res(self, r: dict):
        db = Db()
        db.Services.GatewayService.UpdateGatewayById(Const.GATEWAY_ID, r)

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
        self.globalVariable.mqtt_need_response_dict[res["RQI"]] = res
        self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))

