from Constracts.IHandler import IHandler
import logging
from Constracts.ITransport import ITransport


class MqttDataHandler(IHandler):
    __logger: logging.Logger
    __mqtt: ITransport

    def __init__(self, log: logging.Logger, mqtt: ITransport):
        self.__logger = log
        self.__mqtt = mqtt

    def handler(self, item):
        switcher = {

        }
        func = switcher.get()
        func()
        return

