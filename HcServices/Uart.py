import serial
from Constracts.ITransport import ITransport
import Constants.Constant as Const
import logging


class Uart(ITransport):
    __context: serial.Serial
    __logger: logging.Logger

    def __init__(self, log: logging.Logger):
        super().__init__()
        self.__logger = log

    def send(self, destination: str, data: bytes):
        self.__context.write(data)

    def receive(self) -> bytes:
        return self.__context.read(1)

    def is_readable(self) -> bool:
        return self.__context.readable()

    def connect(self):
        self.__context = serial.Serial(port=Const.UART_PORT, baudrate=Const.UART_BAUD, timeout=Const.UART_TIMEOUT)
        return

    def disconnect(self):
        return

    def reconnect(self):
        return

