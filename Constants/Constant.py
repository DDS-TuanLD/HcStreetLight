# Mqtt connection option
MQTT_PORT = 1883
MQTT_QOS = 2
MQTT_KEEP_ALIVE = 60
MQTT_CLOUD_TO_DEVICE_REQUEST_TOPIC = "cloud/device/request"
MQTT_CLOUD_TO_DEVICE_RESPONSE_TOPIC = "cloud/device/response"
MQTT_DEVICE_TO_CLOUD_REQUEST_TOPIC = "device/cloud/request"
MQTT_DEVICE_TO_CLOUD_RESPONSE_TOPIC = "device/cloud/response"
MQTT_USER = "RD"
MQTT_PASS = "1"

# Sqlite connection option
DB_NAME = "rd.sqlite"

# Hc
HC_PING_TO_CLOUD_INTERVAL = 300
HC_REPORT_DEVICE_STATE_INTERVAL = 300
HC_REPORT_DEVICE_REPORT_INTERVAL = 300
HC_UPDATE_DEVICES_ONLINE_STATUS_TO_GLOBAL_DICT_INTERVAL = 60
HC_CHECK_HEARTBEAT_INTERVAL = 180
HC_RETRY_SEND_MQTT_MESSAGE_INTERVAL = 10
# Network
RIIM_NETWORK_ID = 1
GATEWAY_ID = 1
FIRMWARE_FIRST_VERSION = 1.0

# PropertyIdMapping
PROPERTY_DIM_ID = 0
PROPERTY_RELAY_ID = 1
PROPERTY_TEMP_ID = 2
PROPERTY_LUX_ID = 3
PROPERTY_U_ID = 4
PROPERTY_I_ID = 5
PROPERTY_COS_ID = 6
PROPERTY_P_ID = 7
PROPERTY_KWH_ID = 8
PROPERTY_TYPE_ID = 9

PropertyIdMapping = {
    PROPERTY_DIM_ID: {
        "name": "dim",
        "unit": "percentage"
    },
    PROPERTY_RELAY_ID: {
        "name": "relay",
        "unit": "boolean"
    }
}

# UART
UART_PORT = "COM8"
UART_BAUD = 115200
UART_TIMEOUT = 1

UART_MESS_HEADER_RIIM_TO_AI_1 = 0xaa
UART_MESS_HEADER_RIIM_TO_AI_2 = 0xf5
UART_MESS_HEADER_AI_TO_RIIM_1 = 0x55
UART_MESS_HEADER_AI_TO_RIIM_2 = 0xaa

#device
TIME_SLOT = 10
MAX_RETRY_TIME = 3