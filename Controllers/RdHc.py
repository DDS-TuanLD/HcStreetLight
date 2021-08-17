import asyncio
import json
import logging
import threading
from Constracts.ITransport import ITransport
from Constracts.IController import IController
from Constracts.IHandler import IHandler
from Helper.System import System
from GlobalVariables.GlobalVariables import GlobalVariables
import Constants.Constant as Const
import uuid


class RdHc(IController):
    __mqttServices: ITransport
    __lock: threading.Lock
    __logger: logging.Logger
    __mqttHandler: IHandler
    __systemHelper: System
    __globalVariables: GlobalVariables

    def __init__(self, log: logging.Logger, mqtt: ITransport,
                 mqtt_handler: IHandler):
        self.__logger = log
        self.__mqttServices = mqtt
        self.__lock = threading.Lock()
        self.__mqttHandler = mqtt_handler
        self.__systemHelper = System(self.__logger)
        self.__globalVariables = GlobalVariables()

    def __hc_report_network_info(self):
        pass

    def __hc_load_devices_heartbeat_to_global_dict(self):
        self.__systemHelper.load_devices_heartbeat_to_global_dict()

    async def __hc_check_heartbeat_and_update_devices_online_status_to_db(self):
        while True:
            await asyncio.sleep(Const.HC_CHECK_HEARTBEAT_INTERVAL)
            for device in self.__globalVariables.devices_heartbeat_dict:
                if self.__globalVariables.devices_heartbeat_dict[device] < 3:
                    self.__globalVariables.devices_heartbeat_dict[device] = \
                        self.__globalVariables.devices_heartbeat_dict[device] + 1
                if self.__globalVariables.devices_heartbeat_dict[device] == 3:
                    if self.__globalVariables.devices_online_status_dict[device]:
                        self.__systemHelper.update_device_online_status_to_db(device_address=device, is_online=False)

    async def __hc_update_devices_online_status_from_db_to_global_dict(self):
        while True:
            await asyncio.sleep(Const.HC_UPDATE_DEVICES_ONLINE_STATUS_TO_GLOBAL_DICT_INTERVAL)
            self.__systemHelper.update_devices_online_status_to_global_dict()

    async def __hc_report_devices_state(self):
        await asyncio.sleep(Const.HC_REPORT_DEVICE_STATE_INTERVAL)
        device_state_mes = {}
        self.__mqttServices.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(device_state_mes))

    async def __hc_check_connect_with_cloud(self):
        await asyncio.sleep(Const.HC_PING_TO_CLOUD_INTERVAL)
        ping_mes = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "Ping"
        }
        self.__mqttServices.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(ping_mes))

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
        self.__hc_report_network_info()
        self.__systemHelper.update_devices_online_status_to_global_dict()
        self.__hc_load_devices_heartbeat_to_global_dict()
        task0 = asyncio.create_task(self.__hc_handler_mqtt_data())
        task1 = asyncio.create_task(self.__hc_check_connect_with_cloud())
        task2 = asyncio.create_task(self.__hc_report_devices_state())
        task3 = asyncio.create_task(self.__hc_update_devices_online_status_from_db_to_global_dict())
        task4 = asyncio.create_task(self.__hc_check_heartbeat_and_update_devices_online_status_to_db())
        tasks = [task0, task1, task2, task3, task4]
        await asyncio.gather(*tasks)
