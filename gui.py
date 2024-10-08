from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np

model = load_model('mnist.h5')


def predict_digit(img):
    # resize image to 28x28 pixels
    img = img.resize((28, 28), Image.LANCZOS)
    # convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    # invert image colors to match MNIST
    img = 255 - img
    # reshaping to support our model input and normalizing
    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0
    # predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Digit Recognizer")
        self.x = self.y = 0

        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Draw..", font=("Helvetica", 24))
        self.classify_btn = tk.Button(self, text="Recognize", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        self.label.config(text="Draw..")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        a, b, c, d = rect
        # rect=(a+2,b+2,c-2,d-2) #padding reduces accuracy
        im = ImageGrab.grab(rect)

        digit, acc = predict_digit(im)
        self.label.configure(text="Digit: " + str(digit) + '\nAccuracy: ' + str(int(acc * 100)) + '%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 9
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()