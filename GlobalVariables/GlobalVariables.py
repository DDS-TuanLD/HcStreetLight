class MetaGlobalVariables(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaGlobalVariables, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GlobalVariables(metaclass=MetaGlobalVariables):
    def __init__(self):
        self.__devices_online_status_dict = {}
        self.__devices_heartbeat_dict = {}
        self.__mqtt_need_response_dict = {}

    @property
    def devices_online_status_dict(self):
        return self.__devices_online_status_dict

    @property
    def devices_heartbeat_dict(self):
        return self.__devices_heartbeat_dict

    @property
    def mqtt_need_response_dict(self):
        return self.__mqtt_need_response_dict
