import datetime


class MetaGlobalVariables(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaGlobalVariables, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GlobalVariables(metaclass=MetaGlobalVariables):
    def __init__(self):
        self.__device_online_status_dicts = {}

    @property
    def device_online_status_dicts(self):
        return self.__device_online_status_dicts
