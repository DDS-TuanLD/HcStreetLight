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
        try:
            rqi = data["RQI"]
        except:
            rqi = ""

        mqttReceiveCommandResponse = {
            "RQI": rqi
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        rel = db.Services.NetworkService.FindNetworkById(Const.RIIM_NETWORK_ID)

        network = rel.first()

        if network is None:
            db.Services.NetworkServices.InsertNetwork({"NetworkId": Const.RIIM_NETWORK_ID})

            ok = self.__change_network_key()
            if ok:
                db.Services.NetworkService.UpdateNetworkByCondition(
                    db.Table.NetworkTable.c.NetworkId == Const.RIIM_NETWORK_ID, {"NetworkKey": data["Netkey"]})

            ok = self.__change_network_tx_power()
            if ok:
                db.Services.NetworkService.UpdateNetworkByCondition(
                    db.Table.NetworkTable.c.NetworkId == Const.RIIM_NETWORK_ID, {"TXPower": data["TXPower"]})
            return

        if network.get("NetworkKey") != data["Netkey"]:
            ok = self.__change_network_key()
            if ok:
                db.Services.NetworkService.UpdateNetworkByCondition(
                    db.Table.NetworkTable.c.NetworkId == Const.RIIM_NETWORK_ID, {"NetworkKey": data["Netkey"]})

        if network.get("TXPower") != data["TXPower"]:
            ok = self.__change_network_tx_power()
            if ok:
                db.Services.NetworkService.UpdateNetworkByCondition(
                    db.Table.NetworkTable.c.NetworkId == Const.RIIM_NETWORK_ID, {"TXPower": data["TXPower"]})

    def __change_network_key(self):
        return True

    def __change_network_tx_power(self):
        return True
