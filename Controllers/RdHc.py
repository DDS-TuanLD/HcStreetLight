import asyncio
from Database.Db import Db
import logging
import threading
from Constracts.ITransport import ITransport
from Constracts.IController import IController
from Constracts.IHandler import IHandler


class RdHc(IController):
    __mqttServices: ITransport
    __lock: threading.Lock
    __logger: logging.Logger
    __mqttHandler: IHandler

    def __init__(self, log: logging.Logger, mqtt: ITransport,
                 mqtt_handler: IHandler):
        self.__logger = log
        self.__mqttServices = mqtt
        self.__lock = threading.Lock()
        self.__mqttHandler = mqtt_handler

    async def run(self):
        pass