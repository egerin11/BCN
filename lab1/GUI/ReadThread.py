from PyQt5.QtCore import QThread, pyqtSignal


class ReadThread(QThread):
    data_received = pyqtSignal(str, int)

    def __init__(self, port_descriptor):
        super().__init__()
        self.port = port_descriptor
        self.running = True

    def run(self):
        while self.running:
            try:
                data = self.port.read(100)
                if data:
                    byte_count = len(data)
                    try:
                        decoded_data = data.decode('utf-8')
                    except UnicodeDecodeError:
                        decoded_data = str(data)
                    self.data_received.emit(decoded_data, byte_count)
                self.msleep(100)
            except Exception as e:
                print(f"ReadThread encountered an error: {e}")
                self.stop()

    def stop(self):
        self.running = False
        if self.port.is_open:
            self.port.close()
