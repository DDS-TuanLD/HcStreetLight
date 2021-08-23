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
from Database.Db import Db


class RdHc(IController):
    __mqttServices: ITransport
    __lock: threading.Lock
    __logger: logging.Logger
    __mqttHandler: IHandler
    __systemHelper: System
    __globalVariables: GlobalVariables
    __uart: ITransport
    __buf: list

    def __init__(self, log: logging.Logger, mqtt: ITransport,
                 mqtt_handler: IHandler, uart: ITransport, uart_handler: IHandler):
        self.__logger = log
        self.__mqttServices = mqtt
        self.__lock = threading.Lock()
        self.__mqttHandler = mqtt_handler
        self.__systemHelper = System(self.__logger)
        self.__globalVariables = GlobalVariables()
        self.__uart = uart
        self.__uartHandler = uart_handler

    def __hc_report_network_info(self):
        print("hc report network info")
        res = self.__systemHelper.report_network_info()
        self.__mqttServices.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))

    def __hc_load_devices_heartbeat_to_global_dict(self):
        self.__systemHelper.load_devices_heartbeat_to_global_dict()

    def __hc_add_basic_info_to_db(self):
        self.__systemHelper.add_basic_info_to_db()

    async def __hc_receive_uart_data(self):
        while True:
            await asyncio.sleep(0.1)
            while self.__uart.is_readable():
                c = self.__uart.receive()
                if c == bytes():
                    break
                self.__uart.receive_data_buf.append(int.from_bytes(c, 'big'))

    async def __hc_handler_uart_data(self):
        count = 0
        trace_mes_len = 0
        while True:
            await asyncio.sleep(0.1)
            if len(self.__uart.receive_data_buf) > 3:
                try:
                    p = self.__uart.receive_data_buf.index(Const.UART_MESS_HEADER_RIIM_TO_AI_1, count)
                    if self.__uart.receive_data_buf[p + 1] == Const.UART_MESS_HEADER_RIIM_TO_AI_2:
                        if p == 0:
                            trace_mes_len = self.__uart.receive_data_buf[p + 2]
                        if len(self.__uart.receive_data_buf) < trace_mes_len + 3:
                            break
                        buf = self.__uart.receive_data_buf[0: trace_mes_len + 3]
                        ok = self.__systemHelper.check_uart_crc_mess(buf)
                        if ok:
                            self.__uartHandler.handler(buf)
                            for i in range(0, trace_mes_len + 3):
                                self.__uart.receive_data_buf.pop(0)
                            trace_mes_len = 0
                        if not ok:
                            count += 1
                        if p != 0:
                            if trace_mes_len == 0:
                                for i in range(0, p):
                                    self.__uart.receive_data_buf.pop(0)
                            if trace_mes_len != 0:
                                if (p >= trace_mes_len + 3) or (trace_mes_len + 3 > p >= trace_mes_len + 1):
                                    for i in range(0, p):
                                        self.__uart.receive_data_buf.pop(0)
                                    trace_mes_len = count = 0
                        continue
                    if self.__uart.receive_data_buf[p + 1] != Const.UART_MESS_HEADER_RIIM_TO_AI_2:
                        count += p
                except:
                    if count > 0:
                        count = 0

    async def __hc_retry_send_mqtt_mess(self):
        while True:
            if len(self.__globalVariables.mqtt_need_response_dict) > 0:
                self.__globalVariables.mqtt_need_response_dict.clear()
                await asyncio.sleep(Const.HC_RETRY_SEND_MQTT_MESSAGE_INTERVAL)

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

    async def __hc_send_device_report(self):
        while True:
            print("hc report device report")
            res = self.__systemHelper.report_device_report()
            self.__mqttServices.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))
            await asyncio.sleep(Const.HC_REPORT_DEVICE_REPORT_INTERVAL)

    async def __hc_report_devices_state(self):
        while True:
            print("hc report device state")
            device_state_mes = self.__systemHelper.report_devices_state()
            self.__mqttServices.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(device_state_mes))
            await asyncio.sleep(Const.HC_REPORT_DEVICE_STATE_INTERVAL)

    async def __hc_check_connect_with_cloud(self):
        while True:
            print("hc ping to cloud")
            res = {
                "RQI": str(uuid.uuid4()),
                "TYPCMD": "Ping"
            }
            self.__globalVariables.mqtt_need_response_dict[res["RQI"]] = res
            self.__mqttServices.send(Const.MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC, json.dumps(res))
            await asyncio.sleep(Const.HC_PING_TO_CLOUD_INTERVAL)

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
        # self.__uart.connect()
        self.__hc_add_basic_info_to_db()
        self.__hc_report_network_info()
        self.__systemHelper.update_devices_online_status_to_global_dict()
        self.__hc_load_devices_heartbeat_to_global_dict()
        task0 = asyncio.create_task(self.__hc_handler_mqtt_data())
        task1 = asyncio.create_task(self.__hc_check_connect_with_cloud())
        task2 = asyncio.create_task(self.__hc_report_devices_state())
        task3 = asyncio.create_task(self.__hc_update_devices_online_status_from_db_to_global_dict())
        task4 = asyncio.create_task(self.__hc_check_heartbeat_and_update_devices_online_status_to_db())
        task5 = asyncio.create_task(self.__hc_send_device_report())
        # task6 = asyncio.create_task(self.__hc_receive_uart_data())
        # task7 = asyncio.create_task(self.__hc_handler_uart_data())
        tasks = [task0, task1, task2, task3, task4, task5]
        await asyncio.gather(*tasks)
