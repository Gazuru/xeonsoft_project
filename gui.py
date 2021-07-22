import filecmp
import os
import pickle
import re
import threading
import time

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog

import api_handler
import file_transfer
import stream_grabber


class Upload:
    """
    A fájlfeltöltést megvalósító osztály, nem tölt be semmilyen funkciót jelenleg.
    """
    network_path = None

    @staticmethod
    def clear():
        Upload.network_path = None


class Application(tk.Frame):
    """
    Az applikációt létrehozó és képviselő osztály
    """
    device_frames = []
    current_stream = None
    loaded_file = None

    def __init__(self, master=None):
        """
        Az osztály konstruktora
        :param master: az az objektum, amely ennek a felületi elemnek az őse
        """
        super().__init__(master)
        self.master = master

        self.create_menu()
        self.create_widgets()
        self.pack()

    def create_notebook(self):
        """
        A lapozható oldalakat létrehozó metódus
        """
        self.notebook = ttk.Notebook(self.master)
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_thread)
        self.notebook.pack(pady=10, padx=10, fill='both', expand=True)
        self.main_frame = ttk.Frame(self.notebook)
        self.main_frame.grid(column=0, row=0)
        # self.master.columnconfigure(0, weight=1)
        # self.master.rowconfigure(0, weight=1)
        self.notebook.add(self.main_frame, text="Main")

    def create_device_adder(self):
        """
        Új eszköz hozzádásához szükséges szövegmező, illetve gomb létrehozása.
        """
        self.new_device_ip = tk.StringVar()
        self.new_device_ip_entry = tk.Entry(self.main_frame, textvariable=self.new_device_ip)
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(2, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=7)
        self.new_device_ip_entry.grid(column=1, row=1, pady=10, padx=10)
        self.new_device_ip_entry.focus()
        self.new_device_ip_button = tk.Button(self.main_frame, text="Add", command=self.add_new_device)
        self.new_device_ip_button.grid(column=1, row=2)

    def create_widgets(self):
        """
        A felhasználói felületen megtalálható kezelőelemek létrehozása
        """
        self.create_notebook()
        self.create_device_adder()

    def create_menu(self):
        """
        A felület tetején lévő menü létrehozását megvalósító metódus
        """
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        fileMenu = tk.Menu(menu, tearoff=0)
        # TODO menüelemek funkcióinak implementációja
        fileMenu.add_command(label="Save", command=self.save)
        fileMenu.add_command(label="Load", command=self.load)
        fileMenu.add_command(label="Clear", command=Application.clear)

        menu.add_cascade(label="File", menu=fileMenu)

    def add_new_device(self):
        """
        Eseménykezelő metódus az eszköz hozzáadó gombhoz
        """
        ip_addr = self.new_device_ip.get()

        # Csak akkor adódik hozzá a megfelelő eszközt képviselő objektum, ha megfelelő formátumú IP-címet adott meg a
        # felhasználó
        if bool(re.match("^[0-9]{1,3}(\.[0-9]{1,3}){3}$", ip_addr)):
            Application.device_frames.append(DeviceFrame(Device(ip_addr), self.notebook))
            self.new_device_ip_entry.delete(0, 'end')
        else:
            tk.messagebox.showerror(title="Error", message="Invalid IP format!")
            self.new_device_ip_entry.delete(0, 'end')

    @staticmethod
    def end_current():
        """
        Statikus metódus, az applikációban megjelenő élőkép befejezését oldja meg
        """
        if Application.current_stream:
            Application.current_stream.end_stream()
            Application.current_stream = None

    def tab_thread(self, event):
        """
        Amikor a felhasználó vált a lapozható tabok között, ez a metódus fut le.
        Ez egy új szálon elindítja az 'on_tab_switch' metódust, amelyik létrehozza az élőképet.
        """
        thread = threading.Thread(target=self.on_tab_switch)
        thread.daemon = True
        thread.start()

    def on_tab_switch(self):
        """
        Amikor a tab váltás történik, ezt hívja meg a 'tab_thread metódus
        :return: Amennyiben a főtabra vált a felhasználó, visszatér és nem történik semmi
        """
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

    @staticmethod
    def clear():
        """
        A 'Clear' menüelem eseménykezelő metódusa, kitörli az összes, nem fő tabot
        """
        if Application.loaded_file is not None:
            Application.loaded_file = None
        for i in range(len(Application.device_frames) - 1, -1, -1):
            Application.device_frames[i].kill()

    @staticmethod
    def check_save():
        """
        Ez a metódus azt ellenőrzi le, hogy szükséges-e menteni
        :return: True, hogyha nem szükséges menteni
                 False, hogyha szükséges menteni
        """
        if Application.device_frames:
            ips = []
            for device_frame in Application.device_frames:
                ips.append(device_frame.device.ip_address)
            if Application.loaded_file is not None:
                try:
                    with open('/tmp/tmp.cfg', "wb") as tmp:
                        pickle.dump(ips, tmp, protocol=pickle.HIGHEST_PROTOCOL)

                    if filecmp.cmp('/tmp/tmp.cfg', Application.loaded_file, shallow=True):
                        os.remove('/tmp/tmp.cfg')
                        return True
                    os.remove('/tmp/tmp.cfg')
                    return False
                except Exception as e:
                    print("Error:", e)
            else:
                return False
        else:
            return True

    @staticmethod
    def save():
        """
        A mentést megvalósító metódus
        :return: Abban az esetben tér vissza, ha nem sikerült fájlt megnyitni.
        """
        if Application.device_frames:
            ips = []
            for device_frame in Application.device_frames:
                ips.append(device_frame.device.ip_address)
            filename = tk.filedialog.asksaveasfilename(defaultextension='.cfg', filetypes=[('Config Files', '*.cfg')],
                                                       initialdir=os.path.dirname(os.path.abspath(__file__)))
            if filename is not None:
                with open(filename, "wb") as file:
                    try:
                        pickle.dump(ips, file, protocol=pickle.HIGHEST_PROTOCOL)
                        Application.loaded_file = file
                    except Exception as e:
                        print("Error:", e)
            else:
                return
        else:
            tk.messagebox.showinfo(title="Info", message="Nothing to be saved!")

    def load(self):
        """
        Mentés-fájl betöltését megvalósító metódus
        :return: Az 'on_load' metódus visszatérési értékének függvényében visszatér, valamint akkor, ha üres fájlt
                 próbál betölteni a felhasználó
        """
        if not on_load():
            return
        Application.loaded_file = tk.filedialog.askopenfilename(filetypes=[('Config Files', '*.cfg')],
                                                                initialdir=os.path.dirname(os.path.abspath(__file__)))
        if Application.loaded_file is not None and Application.loaded_file != '':
            for i in range(len(Application.device_frames) - 1, -1, -1):
                Application.device_frames[i].kill()
            with open(Application.loaded_file, "rb") as file:
                try:
                    ips = pickle.load(file)
                    if ips:
                        for address in ips:
                            Application.device_frames.append(DeviceFrame(Device(address), self.notebook))
                    else:
                        return
                except Exception as e:
                    print("Error:", e)
        else:
            return


class Device:
    """
    Az osztály, mely egy, a hálózaton elérhető kamerával felszerelt eszközt képvisel
    """

    def __init__(self, ip):
        """
        Az osztály konstruktora
        :param ip: Az eszköz IP-címe
        """
        self.ip_address = ip
        print("Device created with IP " + str(self.ip_address))


class DeviceFrame(tk.Frame):
    """
    Az osztály, mely egy Device objektum megjelenítéséért felel a felhasználói felületen
    """

    def __init__(self, device, master=None):
        """
        Az osztály konstruktora, mely létrehozza és felkonfigurálja a GUI elemeit
        :param device: Az eszköz, mely élőképének megjelenítéséért felel az osztály
        :param master: Az osztály szülő objektuma
        """
        super().__init__(master)
        self.master = master
        self.device = device
        self.handler = api_handler.ApiObject(device)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=1, rowspan=3, pady=10, padx=10, sticky="ES")
        """refresh = tk.Button(self.button_frame, text="Refresh", command=self.refresh)
        refresh.pack(side="top", fill="x")
        # Valamiért nem működik az elvárt módon a frissítés, ezért átmenetileg kiveszem
        """
        close = tk.Button(self.button_frame, text="Close", command=self.kill)
        close.pack(side="bottom", fill="x")
        # self.create_file_buttons()

        num = 0

        for i in range(len(Application.device_frames) + 1):
            found = True
            for tab in self.master.tabs():
                if self.master.tab(tab, "text") == "Device " + str(i + 1):
                    found = False
            if found:
                num = i
                break

        self.master.add(self, text="Device " + str(num + 1))

        self.master.select(self)

    def kill(self):
        """
        A bezáró gomb megnyomása esetén lefutó kódrészlet, mely eltávolítja az applikációból az objektumot
        """
        Application.end_current()
        Application.device_frames.remove(self)
        self.destroy()

    def refresh(self):
        """
        Jelenleg nem működő metódus, mely az éppen megjelenő élőkép újratöltéséért felel
        """
        main = None
        for tab in self.master.tabs():
            if self.master.tab(tab, "text") == "Main":
                main = tab
                break
        self.master.select(main)
        time.sleep(0.1)
        self.master.select(self)

    def create_file_buttons(self):
        """
        Jelenleg nem használt metódus, a fájlok feltöltéséért felelős gombok létrehozását oldja meg
        """
        open_network_button = tk.Button(self.button_frame, text="Open Network File", command=self.create_network_opener)
        open_network_button.pack(fill="x", side="bottom")
        upload_files_button = tk.Button(self.button_frame, text="Upload", command=self.upload_thread)
        upload_files_button.pack(fill="x", side="bottom")

    def upload_thread(self):
        """
        Jelenleg nem használt metódus, mely egy külön szálon oldja meg a fájlok feltöltését
        """
        threading.Thread(target=self.start_upload).start()

    def start_upload(self):
        """
        Jelenleg nem használt metódus, elindítja a szükséges fájlok feltöltését
        """
        ft = file_transfer.FileTransfer(self.device.ip_address, 'pi', 'GazuruXeon21')
        ft.upload('D:/Python/xeonsoft_project/README.md', '~/Desktop')
        ft.disconnect()

    @staticmethod
    def create_network_opener():
        """
        Jelenleg nem használt metódus, a neurális hálózat bináris fájljának feltöltéséhez szükséges gombot hozza létre
        """
        if Upload.network_path:
            Upload.network_path = None
        Upload.network_path = filedialog.askopenfilenames(title="Open network file",
                                                          initialdir=os.path.dirname(os.path.abspath(__file__)))


#
# A fő ablak
#
root = tk.Tk(className="\XeonSoft_Project")


def on_load():
    """
    Az a metódus, ami eldönti, hogy egy esetleges betöltés esetén szükséges-e a korábban betöltött fájlt menteni
    :return: True, ha nem szükséges
             False, ha szükséges
    """
    if Application.check_save():
        return True
    else:
        reply = messagebox.askyesnocancel("Load new config",
                                          "You have unsaved changes.\nDo you want to save before loading a new configuration?")
        if reply:
            Application.save()
            return True
        elif reply is None:
            return False
        else:
            return True


def on_closing():
    """
    A bezáráskor megjelenő párbeszédablak megjelenítését, az abban található gombok által megvalósított viselkedést
    implementálja
    """

    # Mentés kérdésének feltevése
    if Application.check_save():
        root.destroy()
    else:
        reply = messagebox.askyesnocancel("Quit", "You have unsaved changes.\nDo you want to save before closing?")
        # Igen
        if reply:
            Application.save()
            root.destroy()
        # Mégse
        elif reply is None:
            pass
        # Nem
        else:
            root.destroy()


def init_gui():
    """
    A grafikus felület inicializálása, létrehozása
    """
    root.geometry('740x530')
    root.minsize(740, 530)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = Application(master=root)
    app.mainloop()


#
# A program belépési pontja
#
if __name__ == '__main__':
    init_gui()
