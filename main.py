from Controllers.RdHc import RdHc
import asyncio
from Database.Db import Db
import logging
from logging.handlers import TimedRotatingFileHandler
from HcServices.Mqtt import Mqtt
from Handler.MqttDataHandler import MqttDataHandler
import os

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

mqttHandler = MqttDataHandler(logger, mqtt)

db = Db()
hc = RdHc(logger, mqtt, mqttHandler)


async def main():
    db.init()
    await hc.run()

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
