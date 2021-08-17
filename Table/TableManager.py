from sqlalchemy import MetaData
from Table.Group import Group
from Table.Device import Device
from Table.EventTriggerInputDeviceMapping import EventTriggerInputDeviceMapping
from Table.EventTriggerInputDeviceSetupValue import EventTriggerInputDeviceSetupValue
from Table.Network import Network
from Table.Property import Property
from Table.Schedule import Schedule
from Table.DevicePropertiesMapping import DevicePropertiesMapping
from Table.EventTrigger import EventTrigger
from Table.Gateway import Gateway
from Table.EventTriggerOutputDeviceMapping import EventTriggerOutputDeviceMapping
from Table.EventTriggerOutputDeviceSetupValue import EventTriggerOutputDeviceSetupValue
from Table.EventTriggerOutputGroupMapping import EventTriggerOutputGroupMapping
from Table.EventTriggerOutputGroupSetupValue import EventTriggerOutputGroupSetupValue
from Table.GroupDeviceMapping import GroupDeviceMapping


class TableManager:
    def __init__(self, metadata: MetaData):
        self.__groupTable = Group(metadata)
        self.__deviceTable = Device(metadata)
        self.__eventTriggerInputDeviceMappingTable = EventTriggerInputDeviceMapping(metadata)
        self.__eventTriggerInputDeviceSetupValueTable = EventTriggerInputDeviceSetupValue(metadata)
        self.__networkTable = Network(metadata)
        self.__propertyTable = Property(metadata)
        self.__scheduleTable = Schedule(metadata)
        self.__devicePropertiesMappingTable = DevicePropertiesMapping(metadata)
        self.__eventTriggerTable = EventTrigger(metadata)
        self.__gatewayTable = Gateway(metadata)
        self.__eventTriggerOutputDeviceMappingTable = EventTriggerOutputDeviceMapping(metadata)
        self.__eventTriggerOutputDeviceSetupValueTable = EventTriggerOutputDeviceSetupValue(metadata)
        self.__eventTriggerOutputGroupMappingTable = EventTriggerOutputGroupMapping(metadata)
        self.__eventTriggerOutputGroupSetupValueTable = EventTriggerOutputGroupSetupValue(metadata)
        self.__groupDeviceMappingTable = GroupDeviceMapping(metadata)

    @property
    def GroupTable(self):
        return self.__groupTable.group

    @property
    def DeviceTable(self):
        return self.__deviceTable.device

    @property
    def GroupDeviceMappingTable(self):
        return self.__groupDeviceMappingTable.groupDeviceMapping

    @property
    def EventTriggerInputDeviceMappingTable(self):
        return self.__eventTriggerInputDeviceMappingTable.eventTriggerInputDeviceMapping

    @property
    def EventTriggerInputDeviceSetupValueTable(self):
        return self.__eventTriggerInputDeviceSetupValueTable.eventTriggerInputDeviceSetupValue

    @property
    def NetworkTable(self):
        return self.__networkTable.network

    @property
    def PropertyTable(self):
        return self.__propertyTable.property

    @property
    def ScheduleTable(self):
        return self.__scheduleTable.schedule

    @property
    def DevicePropertiesMappingTable(self):
        return self.__devicePropertiesMappingTable.devicePropertiesMapping

    @property
    def EventTriggerTable(self):
        return self.__eventTriggerTable.eventTrigger

    @property
    def GatewayTable(self):
        return self.__gatewayTable.gateway

    @property
    def EventTriggerOutputDeviceMappingTable(self):
        return self.__eventTriggerOutputDeviceMappingTable.eventTriggerOutputDeviceMapping

    @property
    def EventTriggerOutputDeviceSetupValueTable(self):
        return self.__eventTriggerOutputDeviceSetupValueTable.eventTriggerOutputDeviceSetupValue

    @property
    def EventTriggerOutputGroupMappingTable(self):
        return self.__eventTriggerOutputGroupMappingTable.eventTriggerOutputGroupMapping

    @property
    def EventTriggerOutputGroupSetupValueTable(self):
        return self.__eventTriggerOutputGroupSetupValueTable.eventTriggerOutputGroupSetupValue
