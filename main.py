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
from Helper.UartMessageHelper import UartMessageHelper
from ctypes import *
from cffi import FFI

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

# ffi = FFI()
#
# ffi.cdef("""
# typedef struct uart_valid_data_out uart_valid_data_out;
# struct uart_valid_data_out
# {
#     uint8_t     haveData;
#     uint8_t 	Header[2];
#     uint8_t 	Length;
#     uint8_t 	Opcode[2];
#     uint8_t		Message[118];
# };
# uart_valid_data_out GWIF_ProcessData (void);
# """
#          )
#
# so_file = "/root/RIIM_AI_VER19.so"
#
# ctypes_lib = CDLL(so_file)
# ctypes_lib.GWIF_Init()
#
# cffi_lib = ffi.dlopen(so_file)
# uart_valid_data_out = ffi.new("struct uart_valid_data_out *")

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
    asyncio.run(hc.hc_thread_report_interval())


# def thread_5():
#     while True:
#         with threading.Lock():
#             ctypes_lib.GWIF_Read2Buffer()
#             ctypes_lib.GWIF_CheckData()
#
#
# def thread_6():
#     r = list()
#     while True:
#         uart_valid_data_out = cffi_lib.GWIF_ProcessData()
#         if uart_valid_data_out.haveData == 1:
#             r.append(uart_valid_data_out.Header[0])
#             r.append(uart_valid_data_out.Header[1])
#             r.append(uart_valid_data_out.Opcode[0])
#             r.append(uart_valid_data_out.Opcode[1])
#             r.append(uart_valid_data_out.Length)
#             for i in range(0, uart_valid_data_out.Length):
#                 r.append(uart_valid_data_out.Message[i])
#             print(f"valid data list:{r}")
#             r.clear()


def thread_7():
    pass

def thread_8():
    pass

def main():
    threads = list()

    threads.append(threading.Thread(target=thread_1, args=()))
    threads.append(threading.Thread(target=thread_2, args=()))
    # threads.append(threading.Thread(target=thread_4, args=()))
    # threads.append(threading.Thread(target=thread_5, args=()))
    # threads.append(threading.Thread(target=thread_6, args=()))

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
