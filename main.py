import asyncio
import time
from Controllers.RdHc import RdHc
import threading
from Database.Db import Db
import logging
from logging.handlers import TimedRotatingFileHandler
from HcServices.Mqtt import Mqtt
from Handler.MqttDataHandler import MqttDataHandler
from Handler.UartDataHandler import UartDataHandler
import os
from HcServices.Uart import Uart

file_dir = os.path.dirname(__file__)

logging_handler = logging.handlers.TimedRotatingFileHandler(filename=file_dir + '/Logging/runtime.log', when="MIDNIGHT",
                                                            backupCount=4)
logging_formatter = logging.Formatter(fmt=(
    '%(asctime)s:\t'
    '%(levelname)s:\t'
    '%(filename)s:'
    '%(funcName)s():'
    '%(lineno)d\t'
    '%(message)s'
))
logger = logging.getLogger("my_log")
logging_handler.setFormatter(logging_formatter)
logger.addHandler(logging_handler)
logger.setLevel(logging.DEBUG)

mqtt = Mqtt(logger)
mqtt.connect()
mqttHandler = MqttDataHandler(logger, mqtt)

uart = Uart(logger)
# uart.connect()
uartHandler = UartDataHandler(logger, uart)

db = Db()
db.init()

hc = RdHc(logger, mqtt, mqttHandler, uart, uartHandler)

hc.hc_add_basic_info_to_db()
hc.hc_report_network_info()
hc.hc_update_devices_online_status_to_global_dict()
hc.hc_load_devices_heartbeat_to_global_dict()


# lock = threading.Lock()
#
#
# def thread_test_1():
#     while True:
#         time.sleep(3)
#         with lock:
#             db.Services.GroupService.InsertGroup({
#                 "Name": "group1"
#             })
#
#
# def thread_test_2():
#     while True:
#         time.sleep(3)
#         with lock:
#             rel = db.Services.GroupService.FindAllGroup()
#         groups = rel.fetchall()
#         for g in groups:
#             print(g)
#
#
# def thread_test_3():
#     while True:
#         time.sleep(3)
#         with lock:
#             db.Services.GroupService.InsertGroup({
#                 "Name": "group2"
#             })


def thread_1():
    hc.hc_handler_mqtt_data()


def thread_2():
    asyncio.run(hc.hc_thread_report_interval_and_receive_uart_data())


# def thread_3():
#     hc.hc_report_devices_state()
#
#
# def thread_4():
#     hc.hc_update_devices_online_status_from_db_to_global_dict()
#
#
# def thread_5():
#     hc.hc_check_heartbeat_and_update_devices_online_status_to_db()
#
#
# def thread_6():
#     hc.hc_send_device_report()


def thread_7():
    hc.hc_receive_uart_data()


def thread_8():
    hc.hc_handler_uart_data()


def main():
    threads = list()

    threads.append(threading.Thread(target=thread_1, args=()))
    threads.append(threading.Thread(target=thread_2, args=()))
    # threads.append(threading.Thread(target=thread_3, args=()))
    # threads.append(threading.Thread(target=thread_4, args=()))
    # threads.append(threading.Thread(target=thread_5, args=()))
    # threads.append(threading.Thread(target=thread_6, args=()))
    # threads.append(threading.Thread(target=thread_7, args=()))
    # threads.append(threading.Thread(target=thread_8, args=()))

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    # threads.append(threading.Thread(target=thread_test_1, args=()))
    # threads.append(threading.Thread(target=thread_test_2, args=()))
    # threads.append(threading.Thread(target=thread_test_3, args=()))
    #
    # [thread.start() for thread in threads]
    # [thread.join() for thread in threads]


if __name__ == "__main__":
    main()
