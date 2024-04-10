# Standard library imports
import csv
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
import webbrowser


# Third-party library imports
import openai
import tkinter as tk

from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
import tkinter.font as tkfont

# Local imports
import importlib
import inspect
from definitions.main_window import main_window
from definitions.logger import setup_logger
logger = setup_logger()

# specify the directory containing the definition files
directory = "definitions"

# get a list of all the files in the directory
files = os.listdir(directory)

# filter out any non-python files
files = [f for f in files if f.endswith(".py")]

# create a list to hold the definitions
definitions = []

# import each file and add its definitions and classes to the list
for f in files:
    module_name = f[:-3]  # remove the .py extension
    module = importlib.import_module(f"{directory}.{module_name}")
    for name, definition in inspect.getmembers(module, inspect.isroutine):
        if not name.startswith("_"):
            definitions.append(definition)
    for name, definition in inspect.getmembers(module, inspect.isclass):
        if not name.startswith("_"):
            definitions.append(definition)

# sort the definitions list by name
definitions = sorted(definitions, key=lambda d: d.__name__)

def get_definition(name):
    for definition in definitions:
        if definition.__name__ == name:
            return definition
    raise NameError(f"{name} not found in definitions")


# Initialize the logger
logger = setup_logger()


# Create the root window
root = tk.Tk()
root.title("FoolsGold PyWriter by Alex L.")
root.attributes("-fullscreen", True)
root.config(bg='#f4ecdf')
root.withdraw()

# Create the splash window
splash = tk.Toplevel()
splash.overrideredirect(True)
splash.geometry("{0}x{1}+0+0".format(splash.winfo_screenwidth(), splash.winfo_screenheight()))
splash_img = ImageTk.PhotoImage(Image.open("splash.png"))
splash_label = tk.Label(splash, image=splash_img)
splash_label.pack()
splash.attributes("-topmost", True)

# Center the splash window on the screen
splash.update_idletasks()
width = splash.winfo_width()
height = splash.winfo_height()
x = (splash.winfo_screenwidth() // 2) - (width // 2)
y = (splash.winfo_screenheight() // 2) - (height // 2)

# Define a function to hide the splash window
def hide_splash():
    for i in range(6):
        alpha = splash.attributes("-alpha")
        alpha -= 0.06
        splash.attributes("-alpha", alpha)
        splash.update_idletasks()
        time.sleep(0.009)
    splash.destroy()
    root.deiconify()


# Schedule the function to hide the splash window
splash.after(3000, hide_splash)

# Call the main_window function with the root window
main_window(root, definitions, logger)

# Start the event loop and display the window
root.mainloop()

