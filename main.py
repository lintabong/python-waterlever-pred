import ctypes
import cv2
import numpy
import copy
import tkinter
from PIL import Image, ImageTk

from helper import config

ctypes.windll.shcore.SetProcessDpiAwareness(1)

cam = 0

class CamFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        configuration = config.read()

        w = configuration["camFrame"]["width"]
        h = configuration["camFrame"]["height"]

        self.config(width=w, height=h, background="#5C6592")
        self.place(x=10, y=10)

        tkinter.Label(self, bg="#5C6592", fg="#ffffff", text="x1").place(x=w-200, y=10)
        tkinter.Label(self, bg="#5C6592", fg="#ffffff", text="y1").place(x=w-200, y=50)
        tkinter.Label(self, bg="#5C6592", fg="#ffffff", text="x2").place(x=w-200, y=90)
        tkinter.Label(self, bg="#5C6592", fg="#ffffff", text="y2").place(x=w-200, y=130)
        tkinter.Label(self, bg="#5C6592", fg="#ffffff", text="result").place(x=w-220, y=330)

        self.x = tkinter.Entry(self, width=17)
        self.y = tkinter.Entry(self, width=17)
        self.h = tkinter.Entry(self, width=17)
        self.w = tkinter.Entry(self, width=17)
        self.value = tkinter.Entry(self, width=17)

        self.x.place(x=w-170, y=10)
        self.y.place(x=w-170, y=50)
        self.w.place(x=w-170, y=90)
        self.h.place(x=w-170, y=130)
        self.value.place(x=w-170, y=330)

        tkinter.Button(
            self,
            text="Set",
            width=15, 
            height=2,
            command=self.setPoint).place(x=w-170, y=170)

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
        self.cam = cv2.VideoCapture(cam)

    def streaming_video(self):
        _, image = self.cam.read()
        image    = cv2.flip(image, 1)

        configuration = config.read()
        x = int(configuration["rectangle"]["x"])
        y = int(configuration["rectangle"]["y"])
        w = int(configuration["rectangle"]["w"])
        h = int(configuration["rectangle"]["h"])

        self.value.delete(0, tkinter.END)
        self.value.insert(0, self.process(image, x, y, w, h))

        cv2.line(image, (x, y), (x+w-x, y), (255, 0, 255), 2)
        cv2.line(image, (x, y+h-y), (x+w-x, y+h-y), (255, 0, 255), 2)
        cv2.line(image, (x, y), (x, y+h-y), (255, 0, 255), 2)
        cv2.line(image, (x+w-x, y), (x+w-x, y+h-y), (255, 0, 255), 2)
        cv2.line(image, (x+int((w-x)/2), y), (x+int((w-x)/2), h), (255, 0, 255), 2)

        camHeight = abs(configuration["camFrame"]["height"] - image.shape[0]) + 25
        percentage = 1 - camHeight/image.shape[0]        

        width   = int(image.shape[1]*percentage)
        height  = int(image.shape[0]*percentage)
        image   = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

        img    = Image.fromarray(image)
        imgtk  = ImageTk.PhotoImage(image=img)
        self.cam_space.imgtk = imgtk
        self.cam_space.configure(image=imgtk)

        self.cam_space.after(1, self.streaming_video)

    def setPoint(self):
        configuration = config.read()

        configuration["rectangle"]["x"] = int(self.x.get())
        configuration["rectangle"]["y"] = int(self.y.get())
        configuration["rectangle"]["w"] = int(self.w.get())
        configuration["rectangle"]["h"] = int(self.h.get())

        config.write(configuration)

    def process(self, img, x, y, w, h):
        hsv   = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        mask1 = cv2.inRange(hsv, (0, 10, 120), (150, 240, 255))

        img   = cv2.bitwise_and(img, img, mask=mask1)

        croppedImg = img[y:h, x:w]
        edges      = cv2.Canny(croppedImg, 0, 255)

        rho             = 1
        theta           = numpy.pi/180
        threshold       = 15
        min_line_length = 50
        max_line_gap    = 20

        lines = cv2.HoughLinesP(edges, rho, theta, threshold, numpy.array([]), min_line_length, max_line_gap)

        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    im = copy.deepcopy(croppedImg)
                    cv2.line(im, (x1, y1), (x2, y2), (255, 0, 0), 1)

        count = 0
        for i in range(len(img)):
            for j in range(len(img[i])):
                if i == x+w-x and numpy.mean(img[i][j]) < 255 and numpy.mean(img[i][j]) > 0:
                    count+=1

        value = round(100-(count/(h-y))*30, 2)
        return value


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
