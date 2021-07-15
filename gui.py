import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
import threading
import re
import os
import stream_grabber
import file_transfer


class Upload:
    network_path = None

    @staticmethod
    def clear():
        Upload.network_path = None


#
# Az osztály, mely a felhasználói felület megvalósításáért felel.
#
class Application(tk.Frame):
    device_frames = []
    device_nums = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.create_widgets()
        self.pack()

    #
    # A lapozható oldalakat létrehozó metódus
    #
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_thread)
        self.notebook.pack(pady=10, padx=10, fill='both', expand=True)
        self.main_frame = ttk.Frame(self.notebook)
        self.main_frame.grid(column=0, row=0)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.notebook.add(self.main_frame, text="Main")

    #
    # Új eszköz hozzádásához szükséges szövegmező, illetve gomb létrehozása.
    #
    def create_device_adder(self):
        self.new_device_ip = tk.StringVar()
        self.new_device_ip_entry = tk.Entry(self.main_frame, textvariable=self.new_device_ip)
        self.new_device_ip_entry.grid(column=0, row=0, pady=10, padx=10)
        self.new_device_ip_button = tk.Button(self.main_frame, text="Add", command=self.add_new_device)
        self.new_device_ip_button.grid(column=0, row=1, pady=10)

    #
    # A felhasználói felületen megtalálható kezelőelemek létrehozása
    #
    def create_widgets(self):
        self.create_notebook()
        self.create_device_adder()

    #
    # Eseménykezelő metódus az eszköz hozzáadó gombhoz
    #
    def add_new_device(self):
        ip_addr = self.new_device_ip.get()

        # Csak akkor adódik hozzá a megfelelő eszközt képviselő objektum, ha megfelelő formátumú IP-címet adott meg a
        # felhasználó
        if bool(re.match("[0-9]{1,3}(\.[0-9]{1,3}){3}", ip_addr)):
            self.device_frames.append(DeviceFrame(Device(ip_addr), self.notebook))
            self.new_device_ip_entry.delete(0, 'end')
        else:
            print("Invalid IP address format")

    current_stream = None

    @staticmethod
    def end_current():
        Application.current_stream.end_stream()
        Application.current_stream = None

    def tab_thread(self, event):
        threading.Thread(target=self.on_tab_switch).start()

    def on_tab_switch(self):
        Upload.clear()
        current_id = self.notebook.index("current")
        if Application.current_stream:
            self.end_current()

        if current_id == 0:
            return
        else:
            tab = self.notebook.nametowidget(self.notebook.select())

            if tab:
                Application.current_stream = stream_grabber.CaptureLabel(tab.device.ip_address, tab)


#
# Az osztály, mely egy, a hálózaton elérhető kamerával felszerelt eszközt képvisel
#
class Device:
    def __init__(self, ip):
        self.ip_address = ip
        self.was_loaded = False
        print("Device created with IP " + str(self.ip_address))


#
# TODO elkészíteni ezt a classt, mely váltogatni képest text input bekérése és fájl kiválasztása között
#
class KeyTypeFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master


#
# Az osztály, mely egy Device objektum megjelenítéséért felel a felhasználói felületen
#
class DeviceFrame(tk.Frame):
    def __init__(self, device, master=None):
        super().__init__(master)
        self.master = master
        self.device = device

        # self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.button_frame = tk.Frame(self)
        self.close = tk.Button(self.button_frame, text="Close", command=self.close)
        self.close.pack(fill="x", side="bottom")
        self.create_file_buttons()
        self.master.add(self, text="Device " + str(Application.device_nums + 1))

        Application.device_nums += 1

        self.master.select(self)
        self.button_frame.grid(row=2, column=1, pady=10, padx=10)

    #
    # A bezáró gomb megnyomása esetén lefutó kódrészlet, mely eltávolítja az applikációból az objektumot
    #
    def close(self):
        Application.end_current()
        Application.device_frames.remove(self)
        self.destroy()

    def create_file_buttons(self):
        open_network_button = tk.Button(self.button_frame, text="Open Network File", command=self.create_network_opener)
        open_network_button.pack(fill="x", side="bottom")
        upload_files_button = tk.Button(self.button_frame, text="Upload", command=self.upload_thread)
        upload_files_button.pack(fill="x", side="bottom")

    def upload_thread(self):
        threading.Thread(target=self.start_upload).start()

    def start_upload(self):
        ft = file_transfer.FileTransfer(self.device.ip_address, 'pi', 'GazuruXeon21')
        ft.upload('D:/Python/xeonsoft_project/README.md', '~/Desktop')
        ft.disconnect()

    def create_network_opener(self):
        if Upload.network_path:
            Upload.network_path = None
        Upload.network_path = filedialog.askopenfilename(title="Open network file", defaultextension='.par',
                                                         initialdir=os.path.dirname(os.path.abspath(__file__)),
                                                         filetypes=[('Parchive Index File', '.par')])


#
# A fő ablak
#
root = tk.Tk(className="\XeonSoft_Project")


#
# A bezáráskor megjelenő párbeszédablak megjelenítését, az abban található gombok által megvalósított viselkedést
# implementálja
#
def on_closing():
    reply = messagebox.askyesnocancel("Quit", "You have unsaved changes.\nDo you want to save before closing?")
    if reply:
        # TODO Implement saving
        root.destroy()
        pass
    elif reply is None:
        pass
    else:
        root.destroy()


#
# A grafikus felület inicializálása, létrehozása
#
def init_gui():
    root.geometry('1024x768')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = Application(master=root)
    app.mainloop()


#
# A program belépési pontja
#
if __name__ == '__main__':
    init_gui()
