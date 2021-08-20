from Database.Db import Db
import logging
from GlobalVariables.GlobalVariables import GlobalVariables
import uuid
import Constants.Constant as Const


class System:
    __globalVariables = GlobalVariables()
    __logger = logging.Logger
    __db = Db()

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

    def add_basic_info_to_db(self):
        rel = self.__db.Services.GatewayService.FindGatewayById(Const.GATEWAY_ID)
        gateway = rel.fetchone()

        rel2 = self.__db.Services.NetworkService.FindNetworkById(Const.RIIM_NETWORK_ID)
        network = rel2.fetchone()

        if gateway is None:
            self.__db.Services.GatewayService.InsertGateway({
                "GatewayId": Const.GATEWAY_ID,
            })
        if network is None:
            self.__db.Services.NetworkService.InsertNetwork({
                "NetworkId": Const.RIIM_NETWORK_ID,
                "FirmwareVersion": Const.FIRMWARE_FIRST_VERSION
            })

    def report_devices_state(self) -> dict:
        rel = self.__db.Services.DeviceService.FindAllDevice()
        devices = rel.fetchall()

        rel2 = self.__db.Services.DevicePropertyService.FindAllDevicePropertyMapping()
        devicesPropertyMapping = rel2.fetchall()

        rel3 = self.__db.Services.GatewayService.FindGatewayById(Const.GATEWAY_ID)
        gateway = rel3.fetchone()

        devices_address = []

        res = {
            "RQI": str(uuid.uuid4()),
            "TYPCMD": "DeviceStatus",
            "Gateway": {
                "Temp": gateway["Temp"],
                "Lux": gateway["Lux"],
                "U": gateway["U"],
                "I": gateway["I"],
                "Cos": gateway["Cos"],
                "P": gateway["P"],
                "Minute": gateway["Minute"],
                "KWh": gateway["KWH"]
            },
            "Devices": []
        }

        temp = {}

        if len(devices) != 0:
            for device in devices:
                devices_address.append(device["DeviceAddress"])
                temp[device["DeviceAddress"]] = {
                    "Device": device["DeviceAddress"],
                    "Online": device["IsOnline"],
                    "Status": device["IsBroken"],
                    "Scene": [],
                    "Relay": device["Relay"],
                    "DIM": None,
                    "Temp": None,
                    "Lux": None,
                    "U": None,
                    "I": None,
                    "Cos": None,
                    "P": None,
                    "KWh": device["KWH"]
                }

        if len(devicesPropertyMapping) != 0:
            for devicePropertyMapping in devicesPropertyMapping:
                r = devicePropertyMapping
                if r["PropertyId"] == Const.PROPERTY_DIM_ID:
                    temp[r["DeviceAddress"]]["DIM"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_RELAY_ID:
                    temp[r["DeviceAddress"]]["Relay"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_P_ID:
                    temp[r["DeviceAddress"]]["P"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_TEMP_ID:
                    temp[r["DeviceAddress"]]["Temp"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_LUX_ID:
                    temp[r["DeviceAddress"]]["Lux"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_U_ID:
                    temp[r["DeviceAddress"]]["U"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_I_ID:
                    temp[r["DeviceAddress"]]["I"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_COS_ID:
                    temp[r["DeviceAddress"]]["Cos"] = r["PropertyValue"]
                    continue
                if r["PropertyId"] == Const.PROPERTY_KWH_ID:
                    temp[r["DeviceAddress"]]["KWh"] = r["PropertyValue"]
                    continue

        rel4 = self.__db.Services.EventTriggerOutputDeviceMappingService.FindEventTriggerOutputDeviceMappingByCondition(
            self.__db.Table.EventTriggerOutputDeviceMappingTable.c.DeviceAddress.in_(devices_address)
        )
        scenes = rel4.fetchall()

        if len(scenes) != 0:
            for scene in scenes:
                temp[scene["DeviceAddress"]]["Scene"].append(scene["EventTriggerId"])
        for t in temp:
            res["Devices"].append(temp[t])
        return res

    def report_network_info(self) -> dict:
        rel = self.__db.Services.NetworkService.FindNetworkById(Const.RIIM_NETWORK_ID)
        network = rel.fetchone()
        res = {}
        if network is None:
            res = {
                "RQI": str(uuid.uuid4()),
                "TYPCMD": "NetInfor",
                "NETKEY": None,
                "TXPower": None,
                "MAC": None,
                "FirmVer": None
            }
        if network is not None:
            res = {
                "RQI": str(uuid.uuid4()),
                "TYPCMD": "NetInfor",
                "NETKEY": network["NetworkKey"],
                "TXPower": network["TXPower"],
                "MAC": network["GatewayMac"],
                "FirmVer": network["FirmwareVersion"]
            }
        return res

    def update_devices_online_status_to_global_dict(self):
        devices = self.__db.Services.DeviceService.FindAllDevice()
        if devices is None:
            return
        for device in devices:
            device_address = device['DeviceAddress']
            device_online_status = device['IsOnline']
            self.__globalVariables.devices_online_status_dict[device_address] = device_online_status

    def load_devices_heartbeat_to_global_dict(self):
        devices = self.__db.Services.DeviceService.FindAllDevice()
        if devices:
            return
        for device in devices:
            device_address = device['DeviceAddress']
            device_heartbeat_waiting_count = 0
            self.__globalVariables.devices_heartbeat_dict[device_address] = device_heartbeat_waiting_count

    def update_device_online_status_to_db(self, device_address: str, is_online: bool):
        self.__db.Services.DeviceService.UpdateDeviceByCondition(
            self.__db.Table.DeviceTable.c.DeviceAddress == device_address, {"IsOnline": is_online})
