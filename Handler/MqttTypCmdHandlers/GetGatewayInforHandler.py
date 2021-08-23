import json
import uuid

from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
from Database.Db import Db
import Constants.Constant as Const
import logging


class GetGatewayInForHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()
        rqi = data.get("RQI")
        mqttReceiveCommandResponse = {
            "RQI": rqi
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        rel1 = db.Services.NetworkService.FindNetworkById(Const.RIIM_NETWORK_ID)
        riim_net_info = dict(rel1.first())
        network_info_res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "NetInfor",
            "NETKEY": riim_net_info.get("NetworkKey"),
            "TXPower": riim_net_info.get("TXPower"),
            "MAC": riim_net_info.get("GatewayMac"),
            "FirmVer": riim_net_info.get("FirmwareVersion")
        }
        self.globalVariable.mqtt_need_response_dict[network_info_res["RQI"]] = network_info_res
        self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(network_info_res))

        rel2 = db.Services.GatewayService.FindGatewayById(Const.GATEWAY_ID)

        gateway_info = dict(rel2.first())

        gateway_info_res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "GWRelayStt",
            "Relay_1": gateway_info.get("Relay_1"),
            "Relay_2": gateway_info.get("Relay_2"),
            "Relay_3": gateway_info.get("Relay_3"),
            "Relay_4": gateway_info.get("Relay_4")
        }

        self.globalVariable.mqtt_need_response_dict[gateway_info_res["RQI"]] = gateway_info_res
        self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(gateway_info_res))

