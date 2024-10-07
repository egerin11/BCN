from GUI.SerialGUI import SerialGUI
import sys
from PyQt5.QtWidgets import  QApplication

from packet.Packet import Packet


def main():

    app = QApplication(sys.argv)

    gui1 = SerialGUI(window_id=1)
    gui1.show()

    gui2 = SerialGUI(window_id=2)
    gui2.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

