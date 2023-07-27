import os
import time
import cv2
import tkinter
import json
import ctypes
import threading
from tkinter import END
from datetime import datetime
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory

from helper import config

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class CamFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.config(width=700, height=400, background="#5C6592")
        self.place(x=10, y=10)

        self.x = tkinter.Entry(self, width=15)
        self.y = tkinter.Entry(self, width=15)
        self.h = tkinter.Entry(self, width=15)
        self.w = tkinter.Entry(self, width=15)

        self.x.place(x=440, y=10)
        self.y.place(x=440, y=50)
        self.w.place(x=440, y=90)
        self.h.place(x=440, y=130)

        configuration = config.read()

        self.x.insert(0, configuration["rectangle"]["x"])
        self.y.insert(0, configuration["rectangle"]["y"])
        self.w.insert(0, configuration["rectangle"]["w"])
        self.h.insert(0, configuration["rectangle"]["h"])

        self.cam_space = tkinter.Label(self)
        self.cam_space.place(x=10, y=10)

        self.connect_camera()
        self.streaming_video()

    def connect_camera(self):
        self.cam = cv2.VideoCapture(0)

    def streaming_video(self):
        _, image = self.cam.read()
        image    = cv2.flip(image, 1)

        configuration = config.read()
        x = configuration["rectangle"]["x"]
        y = configuration["rectangle"]["y"]
        w = configuration["rectangle"]["w"]
        h = configuration["rectangle"]["h"]

        cv2.line(image, (x, y), (x+w-x, y), (255, 0, 255), 2)
        cv2.line(image, (x, y+h-y), (x+w-x, y+h-y), (255, 0, 255), 2)
        cv2.line(image, (x, y), (x, y+h-y), (255, 0, 255), 2)
        cv2.line(image, (x+w-x, y), (x+w-x, y+h-y), (255, 0, 255), 2)
        cv2.line(image, (x+int((w-x)/2), y), (x+int((w-x)/2), h), (255, 0, 255), 2)

        image  = cv2.resize(image, (400, 380))

        img    = Image.fromarray(image)
        imgtk  = ImageTk.PhotoImage(image=img)
        self.cam_space.imgtk = imgtk
        self.cam_space.configure(image=imgtk)

        self.cam_space.after(1, self.streaming_video)


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        configuration = config.read()

        w = configuration["width"]
        h = configuration["height"]
        x = int((self.winfo_screenwidth()/2) - (w/2))
        y = int((self.winfo_screenheight()/2) - (h/2))

        self.title("Waterlevel Prediction")
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(False, False)

        CamFrame(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
