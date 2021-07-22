import cv2
import threading
import tkinter as tk

from PIL import ImageTk, Image
from tkinter import messagebox


class CaptureLabel(tk.Label):
    """
    A tkinter package Label osztályából leszármazó osztály, mely megjeleníti a DeviceFrame-en a hozzá tartozó eszköz
    élő képét
    """
    def __init__(self, ip_addr, master=None):
        """
        Az osztály konstruktora
        :param ip_addr: A megjelenítendő eszköz IP-címe
        :param master: A szülő objektum, amelyikhez ez a Label tartozni fog
        """
        super().__init__(master)
        self.master = master
        src = str('http://' + ip_addr + ':8080/stream/video.mjpeg')

        self.timeout = self.after(3000, self.error)
        self.cam = cv2.VideoCapture(src)
        self.after_cancel(self.timeout)
        self.thread = threading.Thread(target=self.video_stream())

        if self.cam.isOpened():
            self.grid(row=0, column=0, rowspan=3, sticky='NWES')

            self.thread.daemon = True
            self.thread.start()

    def error(self):
        """
        Ez a metódus fut le, ha nem sikerül a timeout időn belül megnyitni az élőképet
        """
        messagebox.showerror(title="Error", message="Invalid address!")
        self.master.destroy()

    def video_stream(self):
        """
        Az élőkép megjelenítését végző metódus
        """
        _, frame = self.cam.read()
        cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        image = Image.fromarray(cv2img)
        imagetk = ImageTk.PhotoImage(image=image)
        self.imgtk = imagetk
        self.configure(image=imagetk)
        self.master.after(10, self.video_stream)

    def end_stream(self):
        """
        Az élőkép lekérésének befejezését megvalósító metódus
        """
        self.cam.release()
        self.thread.join()
        self.destroy()


#
# A program belépési pontja
#
if __name__ == '__main__':
    root = tk.Tk()
    main_frame = tk.Frame(root, width=600, height=500)
    main_frame.grid(row=0, column=0, padx=10, pady=2, rowspan=3)
    CaptureLabel('192.168.1.67', main_frame)
    main_frame.mainloop()

    """req = urllib.request.urlopen('http://192.168.1.67:4664')
    arr = numpy.asarray(bytearray(req.read()), dtype=numpy.uint8)
    img = cv2.imdecode(arr, -1)
    cv2.imshow("ASD", img)
"""
