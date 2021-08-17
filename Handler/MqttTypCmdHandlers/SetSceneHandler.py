from Constracts.IMqttTypeCmdHandler import IMqttTypeCmdHandler
from Constracts import ITransport
import logging
import Constants.Constant as Const
import json
from Database.Db import Db
from sqlalchemy import and_


class SetSceneHandler(IMqttTypeCmdHandler):
    def __init__(self, log: logging.Logger, mqtt: ITransport):
        super().__init__(log, mqtt)

    def handler(self, data):
        db = Db()

        mqttReceiveCommandResponse = {
            "RQI": data.get("RQI")
        }

        self.mqtt.send(Const.MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC, json.dumps(mqttReceiveCommandResponse))

        rel = db.Services.EventTriggerService.FindEventTriggerById(data["ID"])
        event = rel.fetchone()
        
        if event is None:
            db.Services.EventTriggerService.InsertEventTrigger(
                {
                    "EventTriggerId": data.get("ID"),
                    "ScriptType": data.get("script_type"),
                    "IsEnable": True,
                    "ScheduleRaw": data.get("input_condition").get("schedule")
                }
            )
            devices_input_condition = list(data.get("input_condition").get("device_condition"))
            
            devices_mapping_input_insert = []
            devices_setup_input_insert = []
            
            for device_input_condition in devices_input_condition:
                device_mapping_input_insert = {
                    "EventTriggerId": data["ID"],
                    "DeviceAddress": device_input_condition["Device"],
                }

                device_setup_input_insert = {
                    "EventTriggerId": data["ID"],
                    "DeviceAddress": device_input_condition["Device"],
                    "PropertyId": device_input_condition["condition"]["attribute"],
                    "PropertyValue": device_input_condition["condition"]["value"],
                    "Operation": device_input_condition["condition"]["operation"]
                }
                devices_setup_input_insert.append(device_setup_input_insert)
                devices_mapping_input_insert.append(device_mapping_input_insert)
           
            db.Services.EventTriggerInputDeviceMappingService.InsertManyEventTriggerInputDeviceMapping(
                devices_mapping_input_insert)
            db.Services.EventTriggerInputDeviceSetupValueService.InsertManyEventTriggerInputDeviceSetupValue(
                devices_setup_input_insert
            )

        if event is not None:

            db.Services.EventTriggerService.UpdateEventTriggerCondition(
                db.Table.EventTriggerTable.c.EventTriggerId == data["ID"],
                {
                    "EventTriggerId": data["ID"],
                    "ScriptType": data["script_type"],
                    "IsEnable": event["IsEnable"],
                    "ScheduleRaw": data["input_condition"]["schedule"]
                }
            )

            devices_input_condition = list(data.get("input_condition").get("device_condition"))
            devices_mapping_input_insert = []
            devices_setup_input_insert = []

            for device_input_condition in devices_input_condition:
                device_mapping_input_insert = {
                    "EventTriggerId": data["ID"],
                    "DeviceAddress": device_input_condition["Device"],
                }

                device_setup_input_insert = {
                    "EventTriggerId": data["ID"],
                    "DeviceAddress": device_input_condition["Device"],
                    "PropertyId": device_input_condition["condition"]["attribute"],
                    "PropertyValue": device_input_condition["condition"]["value"],
                    "Operation": device_input_condition["condition"]["operation"]
                }

                devices_setup_input_insert.append(device_setup_input_insert)
                devices_mapping_input_insert.append(device_mapping_input_insert)

            db.Services.EventTriggerInputDeviceMappingService.RemoveEventTriggerInputDeviceMappingByCondition(
                db.Table.EventTriggerInputDeviceMappingTable.c.EventTriggerId == data["ID"],
            )

            db.Services.EventTriggerInputDeviceSetupValueService.RemoveEventTriggerInputDeviceSetupValueByCondition(
                db.Table.EventTriggerInputDeviceSetupValueTable.c.EventTriggerId == data["ID"],
            )

            db.Services.EventTriggerInputDeviceMappingService.InsertManyEventTriggerInputDeviceMapping(
                devices_mapping_input_insert)
            db.Services.EventTriggerInputDeviceSetupValueService.InsertManyEventTriggerInputDeviceSetupValue(
                devices_setup_input_insert
            )



