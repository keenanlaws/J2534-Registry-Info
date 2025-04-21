# j2534_gui_pyqt5.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QGroupBox
)

from ToolProtocolInfo.J2534DeviceList import J2534DeviceList


class J2534Viewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("J2534 Interface Viewer")
        self.resize(600, 400)

        self.tool_info = J2534DeviceList()

        # Widgets
        self.device_list = QListWidget()
        self.details = QLabel("Select a tool to view details.")
        self.details.setWordWrap(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.device_list)
        layout.addWidget(self._build_group("Tool Details", self.details))
        self.setLayout(layout)

        self._populate_list()
        self.device_list.currentRowChanged.connect(self.display_details)

    def _populate_list(self):
        for device in self.tool_info.devices:
            self.device_list.addItem(f"{device['vendor']} - {device['name']}")

    def display_details(self, index):
        if index < 0:
            return

        device = self.tool_info.devices[index]
        text = (
            f"<b>Vendor:</b> {device['vendor']}<br>"
            f"<b>Name:</b> {device['name']}<br>"
            f"<b>DLL:</b> {device['dll']}<br>"
            f"<b>Supported Protocols:</b> {', '.join(device['protocols'])}"
        )
        self.details.setText(text)

    def _build_group(self, title, widget):
        group = QGroupBox(title)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        group.setLayout(layout)
        return group


if __name__ == "__main__":
    tool_info = J2534DeviceList()
    app = QApplication(sys.argv)
    viewer = J2534Viewer()
    viewer.show()
    sys.exit(app.exec_())
