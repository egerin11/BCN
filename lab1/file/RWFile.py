import os
from dotenv import load_dotenv

load_dotenv()


class RWFile:
    def __init__(self):
        self.PORTS_FILE = os.getenv('PORTS_FILE')
        self.current_position = 0

    def save_ports_to_file(self, port):
        with open(self.PORTS_FILE, 'a+') as f:
            f.write(f"{port}\n")

    def read_port_from_file(self):
        with open(self.PORTS_FILE, 'r') as f:
            f.seek(self.current_position)
            lines = f.readlines()

        return lines

    def clear_ports_file(self):
        open(self.PORTS_FILE, 'w').close()