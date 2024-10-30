import time

from GUI.SerialGUI import SerialGUI
import sys
from PyQt5.QtWidgets import  QApplication

from channel.ChannelSimulator import ChannelSimulator

#
def main():

    app = QApplication(sys.argv)

    gui1 = SerialGUI(window_id=1)
    gui1.show()

    gui2 = SerialGUI(window_id=2)
    gui2.show()

    sys.exit(app.exec_())

# def send_packet(packet, channel_simulator, collision_window=2):
#     max_attempts = 16
#     reciev_packet=''
#     for byte in packet:
#         attempt = 0
#         while attempt < max_attempts:
#             if not channel_simulator.listen_channel():
#                 print(f"Канал занят. Ожидание передачи байта '{byte}'...")
#                 time.sleep(2)
#                 continue
#
#             print(f"Передача байта '{byte}'...")
#
#             if channel_simulator.detect_collision():
#                 print(f"Коллизия при передаче байта '{byte}'. Повторная попытка...")
#                 attempt += 1
#                 channel_simulator.exponential_backoff_delay(attempt)
#                 print(f"Ожидание окончания окна коллизии в {collision_window} секунд...")
#                 time.sleep(collision_window)
#                 continue
#
#             # Если передача успешна
#             print(f"Байт '{byte}' успешно передан.")
#             reciev_packet += byte
#             break
#     return reciev_packet
#
# # Пример использования
# if __name__ == "__main__":
#     channel_simulator = ChannelSimulator()
#     packet = "1234567890"
#     rp=send_packet(packet, channel_simulator)
#     print(rp)

if __name__ == "__main__":
    main()

