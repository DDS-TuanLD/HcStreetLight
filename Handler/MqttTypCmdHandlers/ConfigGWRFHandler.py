import uuid
import threading
from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import Constants.Constant as Const
import json
import logging
from Database.Db import Db


class ConfigGWRFHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()

        mqttReceiveCommandResponse = {
            "RQI": data.get("RQI")
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))
        rel = db.Services.NetworkService.FindNetworkById(Const.RIIM_NETWORK_ID)

        network = rel.fetchone()

        if network is None:
            db.Services.NetworkService.InsertNetwork({
                "NetworkId": Const.RIIM_NETWORK_ID,
                "NetworkKey": data.get("Netkey"),
                "TXPower": data.get("TXPower")
            })
        if network is not None:
            if network["NetworkKey"] != data.get("Netkey"):
                ok = self.__change_network_key()
                if ok:
                    with threading.Lock():
                        db.Services.NetworkService.UpdateNetworkByCondition(
                            db.Table.NetworkTable.c.NetworkId == Const.RIIM_NETWORK_ID, {"NetworkKey": data.get("Netkey")})

            if network["TXPower"] != data.get("TXPower"):
                ok = self.__change_network_tx_power()
                if ok:
                    with threading.Lock():
                        db.Services.NetworkService.UpdateNetworkByCondition(
                            db.Table.NetworkTable.c.NetworkId == Const.RIIM_NETWORK_ID, {"TXPower": data.get("TXPower")})
        self.__cmd_res()

    def __change_network_key(self):
        return True

    def __change_network_tx_power(self):
        return True

    def __cmd_res(self):
        db = Db()
        with threading.Lock():
            rel = db.Services.NetworkService.FindNetworkById(Const.RIIM_NETWORK_ID)
        network = dict(rel.fetchone())
        res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "NetInfor",
            "NETKEY": network.get("NetworkKey"),
            "TXPower": network.get("TXPower"),
            "MAC": network.get("GatewayMac"),
            "FirmVer": network.get("FirmwareVersion")
        }
        self.globalVariable.mqtt_need_response_dict[res["RQI"]] = res
        self.mqtt.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))

