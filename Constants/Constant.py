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
HC_PING_TO_CLOUD_INTERVAL = 15
HC_REPORT_DEVICE_STATE_INTERVAL = 60
HC_UPDATE_DEVICES_ONLINE_STATUS_TO_GLOBAL_DICT_INTERVAL = 60
HC_CHECK_HEARTBEAT_INTERVAL = 180

# Network
RIIM_NETWORK_ID = 1
GATEWAY_ID = 1

# PropertyIdMapping
PROPERTY_DIM_ID = 0
PROPERTY_RELAY_ID = 1

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