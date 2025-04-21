# j2534_gui_tkinter.py
import tkinter as tk

from ToolProtocolInfo.J2534DeviceList import J2534DeviceList


class J2534Viewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("J2534 Interface Viewer")
        self.geometry("600x400")

        self.tool_info = J2534DeviceList()

        # Widgets
        self.device_list = tk.Listbox(self)
        self.details = tk.Label(self, text="Select a tool to view details.", justify="left", anchor="nw", wraplength=550)

        # Layout
        self.device_list.pack(fill=tk.X, padx=10, pady=5)
        self.details.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self._populate_list()
        self.device_list.bind("<<ListboxSelect>>", self.display_details)

    def _populate_list(self):
        for device in self.tool_info.devices:
            self.device_list.insert(tk.END, f"{device['vendor']} - {device['name']}")

    def display_details(self, event):
        selection = self.device_list.curselection()
        if not selection:
            return

        index = selection[0]
        device = self.tool_info.devices[index]
        text = (
            f"Vendor: {device['vendor']}\n"
            f"Name: {device['name']}\n"
            f"DLL: {device['dll']}\n"
            f"Supported Protocols: {', '.join(device['protocols'])}"
        )
        self.details.config(text=text)


if __name__ == "__main__":
    app = J2534Viewer()
    app.mainloop()
