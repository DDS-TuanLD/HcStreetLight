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

    async def __hc_handler_mqtt_data(self):
        while True:
            await asyncio.sleep(0.1)
            if not self.__mqttServices.receive_data_queue.empty():
                with self.__lock:
                    item = self.__mqttServices.receive_data_queue.get()
                    self.__mqttHandler.handler(item)
                    self.__mqttServices.receive_data_queue.task_done()

    async def run(self):
        self.__mqttServices.connect()
        task0 = asyncio.create_task(self.__hc_handler_mqtt_data())
        tasks = [task0]
        await asyncio.gather(*tasks)
