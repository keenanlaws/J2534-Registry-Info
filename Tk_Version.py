# j2534_gui_tkinter.py
import tkinter as tk

class J2534DeviceList:
    def __init__(self):
        self.REG_PATH = (
            r"Software\PassThruSupport.04.04"
            if platform.architecture()[0] == '32bit'
            else r"Software\Wow6432Node\PassThruSupport.04.04"
        )

        self.protocols = [
            'CAN', 'ISO14230', 'ISO15765', 'ISO9141',
            'J1850PWM', 'J1850VPW', 'SCI_A_ENGINE', 'SCI_A_TRANS',
            'SCI_B_ENGINE', 'SCI_B_TRANS', 'MSCAN', 'MSISO15765', 'SW_CAN_PS'
        ]

        self.devices: List[Dict[str, Union[str, List[str]]]] = []
        self._load_devices()

    def _load_devices(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.REG_PATH) as base_key:
                num_devices = winreg.QueryInfoKey(base_key)[0]

                for i in range(num_devices):
                    device_key_name = winreg.EnumKey(base_key, i)
                    with winreg.OpenKey(base_key, device_key_name) as device_key:
                        try:
                            name = winreg.QueryValueEx(device_key, "Name")[0]
                            dll = winreg.QueryValueEx(device_key, "FunctionLibrary")[0]
                            vendor = winreg.QueryValueEx(device_key, "Vendor")[0]
                        except FileNotFoundError:
                            continue  # Skip incomplete registry entries

                        supported = [
                            proto for proto in self.protocols
                            if self._query_registry_value(device_key, proto)
                        ]

                        self.devices.append({
                            "vendor": vendor,
                            "name": name,
                            "dll": dll,
                            "protocols": supported
                        })

        except Exception as e:
            print(f"Failed to enumerate J2534 tools: {e}")

    @staticmethod
    def _query_registry_value(key, name) -> bool:
        try:
            winreg.QueryValueEx(key, name)
            return True
        except FileNotFoundError:
            return False

    def list_protocols(self) -> None:
        for idx, dev in enumerate(self.devices):
            print(f"[{idx}] {dev['vendor']} - {dev['name']}")
            print(f"     DLL Path: {dev['dll']}")
            print(f"     Supported Protocols: {', '.join(dev['protocols'])}\n")

    def dll_path(self, index: int) -> str:
        return self._safe_get(index, "dll")

    def vendor(self, index: int) -> str:
        return self._safe_get(index, "vendor")

    def name(self, index: int) -> str:
        return self._safe_get(index, "name")

    def supported_protocols(self, index: int) -> Union[List[str], str]:
        return self._safe_get(index, "protocols")

    def _safe_get(self, index: int, key: str) -> Union[str, List[str]]:
        try:
            return self.devices[index][key]
        except IndexError:
            return "Selected Tool Index Error.."


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
