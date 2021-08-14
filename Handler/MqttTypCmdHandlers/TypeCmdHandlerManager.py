from Handler.MqttTypCmdHandlers.ConfigGWRFHandler import ConfigGWRFHandler
from Handler.MqttTypCmdHandlers.DelDevHandler import DelDevHandler
from Constracts import ITransport
import logging


class TypeCmdHandlerManager:
    __configGWRFHandler: ConfigGWRFHandler
    __delDevHandler: DelDevHandler

    def __init__(self, log: logging.Logger, mqtt: ITransport):
        self.__configGWRFHandler = ConfigGWRFHandler(log, mqtt)
        self.__delDevHandler = DelDevHandler(log, mqtt)

    @property
    def ConfigGWRF_Handler(self):
        return self.__configGWRFHandler

    @property
    def DelDev_Handler(self):
        return self.__delDevHandler
