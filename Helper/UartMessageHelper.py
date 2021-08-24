UART_MESS_HEADER_AI_TO_RIIM_1 = 0x55
UART_MESS_HEADER_AI_TO_RIIM_2 = 0xaa

UART_OPCODE_AI_TO_RIIM_ASK_BORDER_ROUTER = [0x00, 0x01]
UART_OPCODE_AI_TO_RIIM_ASK_MESH_ROUTER = [0x00, 0x02]
UART_OPCODE_AI_TO_RIIM_ASK_MESH_ROUTER_COORDINATOR_INFO = [0x00, 0x03]
UART_OPCODE_AI_TO_RIIM_ASK_BORDER_ROUTER_COORDINATOR_INFO = [0x00, 0x04]
UART_OPCODE_AI_TO_RIIM_ASK_DEVICE_ACTION_TIME = [0x00, 0x05]
UART_OPCODE_AI_TO_RIIM_SET_TX_POWER_BOUDER_ROUTER = [0x00, 0x06]
UART_OPCODE_AI_TO_RIIM_SET_TX_POWER_MESH_ROUTER = [0x00, 0x07]
UART_OPCODE_AI_TO_RIIM_SET_NET_KEY_BORDER_ROUTER = [0x00, 0x08]
UART_OPCODE_AI_TO_RIIM_SET_NET_KEY_MESH_ROUTER = [0x00, 0x09]
UART_OPCODE_AI_TO_RIIM_DEL_DEVICE = [0x00, 0x0a]
UART_OPCODE_AI_TO_RIIM_PING_DEVICE = [0x00, 0x0b]
UART_OPCODE_AI_TO_RIIM_ADD_DEVICE_TO_GROUP = [0x00, 0x0c]
UART_OPCODE_AI_TO_RIIM_DEL_DEVICE_FROM_GROUP = [0x00, 0x0d]
UART_OPCODE_AI_TO_RIIM_DEL_GROUP = [0x00, 0x0e]
UART_OPCODE_AI_TO_RIIM_REQ_DEVICE_REBOOT = [0x00, 0x0f]
UART_OPCODE_AI_TO_RIIM_SET_TX_POWER_DEVICE = [0x00, 0x10]
UART_OPCODE_AI_TO_RIIM_SET_WARNING_PARA_DEVICE = [0x00, 0x11]
UART_OPCODE_AI_TO_RIIM_SET_SCENE_DEVICE = [0x00, 0x12]
UART_OPCODE_AI_TO_RIIM_DEL_SCENE_DEVICE = [0x00, 0x13]
UART_OPCODE_AI_TO_RIIM_ACT_SCENE_DEVICE = [0x00, 0x14]
UART_OPCODE_AI_TO_RIIM_ACT_DIM_ALL = [0x00, 0x15]
UART_OPCODE_AI_TO_RIIM_ACT_DIM_DEVICE = [0x00, 0x16]
UART_OPCODE_AI_TO_RIIM_ACT_DIM_GROUP = [0x00, 0x17]
UART_OPCODE_AI_TO_RIIM_SET_STARTER_DIM_DEVICE = [0x00, 0x18]
UART_OPCODE_AI_TO_RIIM_SET_RESPONSE_TIME = [0x00, 0x19]
UART_OPCODE_AI_TO_RIIM_ACT_SCENE_GROUP = [0x00, 0x1a]
UART_OPCODE_AI_TO_RIIM_ACT_SCENE_ALL = [0x00, 0x1b]
UART_OPCODE_AI_TO_RIIM_SET_WARNING_PARA_ALL_DEVICE = [0x00, 0x1c]
UART_OPCODE_AI_TO_RIIM_SET_WARNING_PARA_GROUP = [0x00, 0x1d]
UART_OPCODE_AI_TO_RIIM_SET_TX_POWER_GROUP = [0x00, 0x1e]
UART_OPCODE_AI_TO_RIIM_SET_TX_POWER_ALL = [0x00, 0x1f]

TX_POWER = {}

class UartMessageHelper:

    def check_uart_crc_mess(self, buf: list):
        temp = 0
        for i in range(2, len(buf) - 1):
            temp += buf[i]
        return (temp & 0xff) == buf[len(buf) - 1]

    def create_uart_crc_byte(self, buf: list):
        temp = 0
        for i in range(2, len(buf) - 1):
            temp += buf[i]
        return temp & 0xff

    def create_uart_message(self, opcode: list, para: list) -> list:
        send_data = []
        mes_len = len(opcode) + len(para) + 1
        send_data.append(UART_MESS_HEADER_AI_TO_RIIM_1)
        send_data.append(UART_MESS_HEADER_AI_TO_RIIM_2)
        send_data.append(mes_len)
        send_data.append(opcode)
        send_data.append(para)
        send_data.append(0)
        send_data[len(send_data) - 1] = self.create_uart_crc_byte(send_data)
        return send_data

    def create_request_border_router_info(self) -> list:
        send_data = self.create_uart_message(UART_OPCODE_AI_TO_RIIM_ASK_BORDER_ROUTER, [])
        return send_data

    def create_request_mesh_router_info(self, IpV6: list) -> list:
        send_data = self.create_uart_message(UART_OPCODE_AI_TO_RIIM_ASK_MESH_ROUTER, IpV6)
        return send_data

    def create_request_border_router_coor_info(self) -> list:
        send_data = self.create_uart_message(UART_OPCODE_AI_TO_RIIM_ASK_BORDER_ROUTER_COORDINATOR_INFO, [])
        return send_data

    def create_request_mesh_router_coor_info(self) -> list:
        send_data = self.create_uart_message(UART_OPCODE_AI_TO_RIIM_ASK_MESH_ROUTER_COORDINATOR_INFO, [])
        return send_data

    def create_request_device_time_action(self, IpV6: list) -> list:
        send_data = self.create_uart_message(UART_OPCODE_AI_TO_RIIM_ASK_DEVICE_ACTION_TIME, IpV6)
        return send_data

    def create_request_set_tx_power_border_router(self, tx_power: int):
        pass

    def create_request_set_tx_power_mesh_router(self):
        pass

    def create_request_set_net_key_border_router(self):
        pass

    def create_request_set_net_key_mesh_router(self):
        pass

    def create_request_delete_device(self):
        pass

    def create_request_ping_device(self):
        pass

    def create_request_add_device_to_group(self):
        pass

    def create_request_delete_device_from_group(self):
        pass

    def create_request_delete_group(self):
        pass

    def create_request_device_reboot(self):
        pass

    def create_request_set_prating_device(self):
        pass

    def create_request_set_warning_parameter_device(self):
        pass

    def create_request_set_scene_device(self):
        pass

    def create_request_del_scene_device(self):
        pass

    def create_request_active_scene_device(self):
        pass

    def create_request_dim_all_device(self):
        pass

    def create_request_dim_device(self):
        pass

    def create_request_dim_group(self):
        pass

    def create_request_set_starter_dim_device(self):
        pass

    def create_request_set_device_time_response(self):
        pass

    def create_request_active_scene_group(self):
        pass

    def create_request_active_scene_all(self):
        pass

    def create_request_warning_parameter_all(self):
        pass

    def create_request_warning_parameter_group(self):
        pass

    def create_request_tx_power_group(self):
        pass

    def create_request_tx_power_all(self):
        pass