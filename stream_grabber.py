import threading
import tkinter
from threading import Thread
from PIL import ImageTk, Image
import tkinter as tk
import cv2


class RTSPVideoWriterObject(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)

        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        self.codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        # self.output_video = cv2.VideoWriter('output.avi', self.codec, 30, (self.frame_width, self.frame_height))

        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        if self.status:
            cv2.imshow('frame', self.frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            # self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # self.output_video.write(self.frame)
        pass


def connect_stream(ip_address):
    video_stream_widget = RTSPVideoWriterObject('http://' + ip_address + ':8080/stream/video.mjpeg')
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass


def start_stream(ip):
    threading.Thread(target=connect_stream(ip)).start()


def stop_stream(stream):
    stream.join()


class CaptureLabel(tk.Label):
    def __init__(self, ip_addr, master=None):
        super().__init__(master)
        self.master = master
        src = str('http://' + ip_addr + ':8080/stream/video.mjpeg')
        self.cam = cv2.VideoCapture(src)

        self.grid(row=0, column=0, rowspan=3)

        self.delay = 15
        self.thread = threading.Thread(target=self.video_stream())
        self.thread.daemon = True
        self.thread.start()

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
