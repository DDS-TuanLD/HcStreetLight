from sqlalchemy import MetaData
from Table.Group import Group
from Table.Device import Device
from Table.GroupDeviceMapping import GroupDeviceMapping
from Table.EventTriggerGroupMapping import EventTriggerGroupMapping
from Table.EventTriggerDeviceMapping import EventTriggerDeviceMapping
from Table.EventTriggerGroupSetupValue import EventTriggerGroupSetupValue
from Table.EventTriggerDeviceSetupValue import EventTriggerDeviceSetupValue
from Table.Network import Network
from Table.Property import Property
from Table.Schedule import Schedule
from Table.DevicePropertiesMapping import DevicePropertiesMapping
from Table.EventTrigger import EventTrigger


class TableManager:
    def __init__(self, metadata: MetaData):
        self.__groupTable = Group(metadata)
        self.__deviceTable = Device(metadata)
        self.__groupDeviceMappingTable = GroupDeviceMapping(metadata)
        self.__eventTriggerGroupMappingTable = EventTriggerGroupMapping(metadata)
        self.__eventTriggerDeviceMappingTable = EventTriggerDeviceMapping(metadata)
        self.__eventTriggerGroupSetupValueTable = EventTriggerGroupSetupValue(metadata)
        self.__eventTriggerDeviceSetupValueTable = EventTriggerDeviceSetupValue(metadata)
        self.__networkTable = Network(metadata)
        self.__propertyTable = Property(metadata)
        self.__scheduleTable = Schedule(metadata)
        self.__devicePropertiesMappingTable = DevicePropertiesMapping(metadata)
        self.__eventTriggerTable = EventTrigger(metadata)

    @property
    def GroupTable(self):
        return self.__groupTable.group

    @property
    def DeviceTable(self):
        return self.__deviceTable.device

    @property
    def GroupDeviceMappingTable(self):
        return  self.__groupDeviceMappingTable.groupDeviceMapping

    @property
    def EventTriggerGroupMappingTable(self):
        return self.__eventTriggerGroupMappingTable.eventTriggerGroupMapping

    @property
    def EventTriggerDeviceMappingTable(self):
        return self.__eventTriggerDeviceMappingTable.eventTriggerDeviceMapping

    @property
    def EventTriggerGroupSetupValueTable(self):
        return self.__eventTriggerGroupSetupValueTable.eventTriggerGroupSetupValue

    @property
    def EventTriggerDeviceSetupValueTable(self):
        return self.__eventTriggerDeviceSetupValueTable.eventTriggerDeviceSetupValue

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
