import tkinter as tk
import cv2
import os
import datetime
from PIL import Image, ImageTk

# Creates path
ImageFolder = 'Images'
path = os.path.join(os.getcwd(), ImageFolder)
# Creates the folder for the images if it doesn't exist
if not os.path.exists(path):
    os.makedirs(path)
	
# Initializes the video capture
width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Initializes the GUI
root = tk.Tk()
vidFeed = tk.Label(root)
vidFeed.pack()

# Binds escape to exit the program
root.bind('<Escape>', lambda e: root.destroy())

# Captures a frame and displays it
def showFrame():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    vidFeed.imgtk = imgtk
    vidFeed.configure(image=imgtk)
    vidFeed.after(10, showFrame)
	
# Takes the screenshot and saves it
def screenshot():
    ts = datetime.datetime.now()
    filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
    p = os.path.join(path,filename)
    _, frame = cap.read()
    cv2.imwrite(p, frame)
	
# Sets up the button for taking a screenshot	
picBtn = tk.Button(root, text="Snapshot", command=screenshot)
picBtn.pack(fill="both", expand=True, padx=200, pady=5)

# Sets up the quit button
quitBtn = tk.Button(root, text="Quit", command=root.destroy)
quitBtn.pack(fill="both", expand=True, padx=350, pady=10)

# Displays the current frame
showFrame()
root.mainloop()
