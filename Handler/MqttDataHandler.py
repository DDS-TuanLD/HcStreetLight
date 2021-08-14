import json
import logging
import Constants.Constant as Const
from Constracts.IHandler import IHandler
from Constracts.ITransport import ITransport
from Handler.MqttTypCmdHandlers.TypeCmdHandlerManager import TypeCmdHandlerManager

class MqttDataHandler(IHandler):
    __logger: logging.Logger
    __mqtt: ITransport
    __mqttTypeCmdHandlerManager: TypeCmdHandlerManager

    def __init__(self, log: logging.Logger, mqtt: ITransport):
        self.__logger = log
        self.__mqtt = mqtt
        self.__mqttTypeCmdHandlerManager = TypeCmdHandlerManager(log, mqtt)

    def handler(self, item):
        print("data from mqtt: " + item)
        self.__logger.debug("data from mqtt: " + item)

        topic = item['topic']
        msg = item['msg']
        switcher = {
            Const.MQTT_CLOUD_TO_DEVICE_REQUEST_TOPIC: self.__handler_cloud_to_device_request_topic,
            Const.MQTT_DEVICE_TO_CLOUD_RESPONSE_TOPIC: self.__handler_device_to_cloud_response_topic
        }
        func = switcher.get(topic)
        func(msg)
        return

    def __handler_cloud_to_device_request_topic(self, data):
        rqi: str
        cmd: str

        try:
            json_data = json.loads(data)
            try:
                rqi = json_data["RQI"]
            except:
                rqi = ""

            try:
                cmd = json_data["TYPCMD"]
            except:
                cmd = ""

            mqttReceiveCommandResponse = {
                "RQI": rqi
            }

            self.__mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

            switcher = {
                "ConfigGWRF": self.__mqttTypeCmdHandlerManager.ConfigGWRF_Handler.handler,
                # "DelDev":,
                # "GetGatewayInfor":,
                # "PingDevice":,
                # "PingGateway":,
                # "RequestInfor":,
                # "CreateGroup":,
                # "DelDevFrGroup":,
                # "DelGroup":,
                # "RebootGateway":,
                # "RebootDevice":,
                # "GatewayCommander":,
                # "DeviceCommander":,
                # "ConfigDev":,
                # "SetScene":,
                # "DelScene":,
                # "DelDeviceInScene":,
                # "ControlRelay":,
                # "ControlDevice":,
                # "ActiveScene":,
                # "StopScene":,
                # "DeviceFirmURL":,
                # "GatewayFirmURL":
            }

            func = switcher.get(cmd)
            func(data)

        except:
            self.__logger.error(f"mqtt data receiver in topic {Const.MQTT_CLOUD_TO_DEVICE_REQUEST_TOPIC} invalid")
            print(f"mqtt data receiver in topic {Const.MQTT_CLOUD_TO_DEVICE_REQUEST_TOPIC} invalid")

    def __handler_device_to_cloud_response_topic(self, data):
        pass