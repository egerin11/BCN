import json
import os
from port import InitPort


class PortManager:
    PORT_INFO_FILE = 'port_info.json'

    def __init__(self):
        self.port_descriptors = {}
        self.load_port_info()

    def load_port_info(self):
        if os.path.exists(self.PORT_INFO_FILE):
            try:
                with open(self.PORT_INFO_FILE, 'r') as f:
                    self.port_info = json.load(f)
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON. Файл пуст или содержит некорректный JSON.")
                self.port_info = {}
            except Exception as e:
                print(f"Ошибка при загрузке данных порта: {e}")
                self.port_info = {}
        else:
            self.port_info = {}

    def save_port_info(self):
        with open(self.PORT_INFO_FILE, 'w+') as f:
            json.dump(self.port_info, f)

    def get_port_descriptor(self, port_name, type: bool = True):
        if port_name not in self.port_descriptors:
            if port_name in self.port_info:
                port_config = self.port_info[port_name]
                self.port_descriptors[port_name] = InitPort.InitPort(port_name, **port_config)
            else:
                self.port_descriptors[port_name] = InitPort.InitPort(port_name,
                                                                     baudrate=9600,
                                                                     bytesize=8,
                                                                     parity='N',
                                                                     stopbits=1,
                                                                     timeout=1,
                                                                     xonxoff=False,
                                                                     rtscts=False)
                self.port_info[port_name] = {
                    'baudrate': 9600,
                    'bytesize': 8,
                    'parity': 'N',
                    'stopbits': 1,
                    'timeout': 1,
                    'xonxoff': False,
                    'rtscts': False,
                    'type': type
                }
                self.save_port_info()
        # setattr(self.port_descriptors[port_name],'type',type)
        return self.port_descriptors[port_name]

    def update_port_config(self, port_name, **kwargs):
        if port_name in self.port_info:
            self.port_info[port_name].update(kwargs)
            self.save_port_info()
            if port_name in self.port_descriptors:
                self.port_descriptors[port_name].apply_new_settings(**kwargs)
            print(f"Updated configuration for port {port_name}: {kwargs}")
        else:
            print(f"Port {port_name} not found in port info")

    def close_all_ports(self):
        for port in self.port_descriptors.values():
            port.close()
        self.port_descriptors.clear()
