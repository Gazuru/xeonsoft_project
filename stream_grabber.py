import threading
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox
import cv2


class CaptureLabel(tk.Label):
    def __init__(self, ip_addr, master=None):
        super().__init__(master)
        self.master = master
        src = str('http://' + ip_addr + ':8080/stream/video.mjpeg')

        self.timeout = self.after(3000, self.error)
        self.cam = cv2.VideoCapture(src)
        self.after_cancel(self.timeout)
        self.thread = threading.Thread(target=self.video_stream())

        if self.cam.isOpened():
            self.grid(row=0, column=0, rowspan=3, sticky='NWS')

            self.thread.daemon = True
            self.thread.start()

    def error(self):
        messagebox.showerror(title="Error", message="Invalid address!")
        self.master.destroy()

    def video_stream(self):
        _, frame = self.cam.read()
        cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        image = Image.fromarray(cv2img)
        imagetk = ImageTk.PhotoImage(image=image)
        self.imgtk = imagetk
        self.configure(image=imagetk)
        self.master.after(10, self.video_stream)

    def end_stream(self):
        self.thread.join()
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    main_frame = tk.Frame(root, width=600, height=500)
    main_frame.grid(row=0, column=0, padx=10, pady=2, rowspan=3)

    CaptureLabel('192.168.1.67', main_frame)
    main_frame.mainloop()
