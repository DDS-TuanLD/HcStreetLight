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