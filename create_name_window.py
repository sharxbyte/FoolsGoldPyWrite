# Standard library imports
import datetime
import json
import logging
import os
import shutil
import subprocess
import sys
import time
import webbrowser

# Third-party library imports
import openai
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog

# Local imports
import importlib
import inspect
from definitions import *

def create_name_window():
    global name_window
    
    # Create a new window to enter the character's name
    name_window = tk.Toplevel()
    name_window.title("Enter Name")

    # Create a label and entry box for the character's name
    name_label = tk.Label(name_window, text="Enter name:")
    name_label.pack(side=tk.LEFT, padx=10, pady=10)

    name_entry = tk.Entry(name_window)
    name_entry.pack(side=tk.LEFT, padx=10, pady=10)

    # Define a function to save the name and close the window
    def save_name():
        global character_name
        character_name = name_entry.get()
        name_window.destroy()

    # Create a button to save the name
    save_button = tk.Button(name_window, text="Save", command=save_name)
    save_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Set focus to the name entry box
    name_entry.focus_set()

    # Start the tkinter event loop for the name window
    try:
        name_window.mainloop()
    except:
        messagebox.showerror("Error", "An error occurred while creating the name window.")
        name_window.destroy()
