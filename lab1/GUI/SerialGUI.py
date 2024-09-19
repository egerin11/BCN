from PyQt5.QtWidgets import (
   QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QMessageBox, QComboBox, QLineEdit
)

from GUI.ReadThread import ReadThread
from port import CheckPort
from port.PortManager import PortManager

class SerialGUI(QWidget):
    used_ports = []

    def __init__(self, window_id):
        super().__init__()
        self.window_id = window_id
        self.setWindowTitle(f"Serial Port Manager - Window {window_id}")
        self.port_manager = PortManager()
        # self.rw_file = RWFile()  # Uncomment if using RWFile
        self.read_threads = []
        self.port_pairs = []
        self.send_ports = []
        self.receive_ports = []
        self.current_send_port_name = None
        self.current_receive_port_name = None
        self.init_ui()
        self.initialize_ports()

    def init_ui(self):
        layout = QVBoxLayout()

        self.send_port_label = QLabel("Порт для отправки:")
        self.send_port_combo = QComboBox()

        self.receive_port_label = QLabel("Порт для приема:")
        self.receive_port_combo = QComboBox()

        self.received_byte_data_label = QLabel("Количество байт:")
        self.received_byte_data = QListWidget()
        self.received_byte_data.setFixedSize(300, 50)
        self.baud_rate_label = QLabel("Скорость передачи:")
        self.send_baud_rate_combo = QComboBox()
        self.baud_rates = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
        self.send_baud_rate_combo.addItems(map(str, self.baud_rates))
        self.receive_baud_rate_combo=QComboBox()
        self.receive_baud_rate_combo.addItems(map(str, self.baud_rates))

        layout.addWidget(self.baud_rate_label)
        layout.addWidget(self.send_baud_rate_combo)
        layout.addWidget(self.receive_baud_rate_combo)
        self.start_button = QPushButton("Начать")
        self.stop_button = QPushButton("Остановить")
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.start_communication)
        self.stop_button.clicked.connect(self.stop_communication)

        self.received_data_label = QLabel("Полученные данные:")
        self.received_data_display = QListWidget()

        layout.addWidget(self.send_port_label)
        layout.addWidget(self.send_port_combo)

        layout.addWidget(self.receive_port_label)
        layout.addWidget(self.receive_port_combo)

        layout.addWidget(self.baud_rate_label)
        layout.addWidget(self.send_baud_rate_combo)
        layout.addWidget(self.receive_baud_rate_combo)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.received_data_label)
        layout.addWidget(self.received_data_display)

        layout.addWidget(self.received_byte_data_label)
        layout.addWidget(self.received_byte_data)

        self.send_data_label = QLabel("Отправить данные:")
        self.send_data_input = QLineEdit()
        self.send_button = QPushButton("Отправить")
        self.send_button.clicked.connect(self.send_data)
        self.send_baud_rate_combo.currentIndexChanged.connect(self.update_baud_rate)
        self.receive_baud_rate_combo.currentIndexChanged.connect(self.update_baud_rate)


        layout.addWidget(self.send_data_label)
        layout.addWidget(self.send_data_input)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def initialize_ports(self):

        check_ports = CheckPort.Port.find_pts_ports()
        ports = CheckPort.Port.check_ports(check_ports)

        if len(ports) < 4:
            QMessageBox.critical(self, "Ошибка", "Недостаточно доступных портов.")
            return

        pair1 = (ports[0], ports[1])
        pair2 = (ports[2], ports[3])
        print(pair1)
        self.port_pairs = [pair1, pair2]
        self.send_ports = [pair1[0], pair2[0]]
        self.receive_ports = [pair2[1], pair1[1]]
        SerialGUI.used_ports.extend([
            self.send_ports[self.window_id - 1],
            self.receive_ports[self.window_id - 1]
        ])

        self.send_port_combo.addItem(self.send_ports[self.window_id - 1])
        self.receive_port_combo.addItem(self.receive_ports[self.window_id - 1])

    def start_communication(self):
        send_port_name = self.send_port_combo.currentText()
        receive_port_name = self.receive_port_combo.currentText()

        if not send_port_name or not receive_port_name:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите оба порта.")
            return

        if send_port_name == receive_port_name:
            QMessageBox.warning(self, "Ошибка", "Порты для отправки и приема не должны совпадать.")
            return

        try:
            receive_port = self.port_manager.get_port_descriptor(receive_port_name, type=False)

            if any(thread.port == receive_port for thread in self.read_threads):
                QMessageBox.warning(self, "Ошибка", f"Порт {receive_port_name} уже используется.")
                return

            read_thread = ReadThread(receive_port)
            read_thread.data_received.connect(self.display_received_data)
            read_thread.data_received.connect(self.display_received_byte_data)
            read_thread.start()
            self.read_threads.append(read_thread)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            QMessageBox.information(
                self,
                "Успех",
                f"Начата коммуникация:\nОтправка: {send_port_name}\nПрием: {receive_port_name}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось начать коммуникацию: {e}")

    def display_received_data(self, data, byte_count):
        self.received_data_display.addItem(data)

    def display_received_byte_data(self, data, byte_count):
        self.received_byte_data.addItem(f"{byte_count} байт получено")

    def stop_communication(self):
        for thread in self.read_threads:
            thread.stop()
            thread.wait()
        self.read_threads.clear()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        QMessageBox.information(self, "Успех", "Коммуникация остановлена.")

    def update_baud_rate(self):
        sender = self.sender()

        if sender == self.send_baud_rate_combo:
            selected_baud_rate = self.baud_rates[self.send_baud_rate_combo.currentIndex()]
            port_name = self.send_port_combo.currentText()
            if not port_name:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите порт для отправки.")
                return
            try:
                self.port_manager.update_port_config(port_name, baudrate=selected_baud_rate)
                QMessageBox.information(self, "Успех",
                                        f"Скорость передачи порта {port_name} обновлена на {selected_baud_rate} бит/с")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось обновить скорость передачи: {e}")

        elif sender == self.receive_baud_rate_combo:
            selected_baud_rate = self.baud_rates[self.receive_baud_rate_combo.currentIndex()]
            port_name = self.receive_port_combo.currentText()
            if not port_name:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите порт для приема.")
                return
            try:
                self.port_manager.update_port_config(port_name, baudrate=selected_baud_rate)
                QMessageBox.information(self, "Успех",
                                        f"Скорость передачи порта {port_name} обновлена на {selected_baud_rate} бит/с")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось обновить скорость передачи: {e}")

    def send_data(self):
        send_port_name = self.send_port_combo.currentText()
        data = self.send_data_input.text()
        if not send_port_name:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите порт для отправки.")
            return
        if not data:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите данные для отправки.")
            return
        try:
            send_port = self.port_manager.get_port_descriptor(send_port_name, type=True)
            send_port.write(data.encode('utf-8'))
            QMessageBox.information(self, "Успех", f"Отправлено: {data}")
            self.send_data_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось отправить данные: {e}")

    def closeEvent(self, event):
        self.stop_communication()
        self.port_manager.close_all_ports()
        event.accept()
