# Standard library imports
import csv
import datetime
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import webbrowser

# Third-party library imports
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Local imports
import importlib
import inspect

def show_api_warning():
    # Create a new window
    warning_window = tk.Toplevel()
    warning_window.title("API Warning")

    # Calculate the window size as 30% of the screen size
    screen_width = warning_window.winfo_screenwidth()
    screen_height = warning_window.winfo_screenheight()
    window_width = int(screen_width * 0.30)
    window_height = int(screen_height * 0.30)
    warning_window.maxsize(window_width, window_height)

    # Center the window
    position_right = int(warning_window.winfo_screenwidth()/2 - warning_window.winfo_width()/2)
    position_down = int(warning_window.winfo_screenheight()/2 - warning_window.winfo_height()/2)
    warning_window.geometry(f"+{position_right}+{position_down}")
    
    # Create warning message
    message = "By clicking 'Okay' you acknowledge that you will be accessing the OpenAI API, which is not free. You are solely responsible for your use of the program and any associated costs. Please review the OpenAI pricing page for more information."
    label = ttk.Label(warning_window, text=message, font=("Courier Std", 12), justify="center", wraplength=window_width-40)
    label.grid(column=0, row=0, padx=5, pady=10)

    # Create hyperlink
    hyperlink = tk.Label(warning_window, text="OpenAI pricing page", fg="blue", cursor="hand2")
    hyperlink.grid(column=0, row=1, padx=20, pady=10)

    # Open hyperlink in browser when clicked
    def open_link(event):
        webbrowser.open_new("https://openai.com/pricing/")
    hyperlink.bind("<Button-1>", open_link)

    # Create 'Okay' and 'Cancel' buttons
    okay_button = ttk.Button(warning_window, text="Okay", command=load_api_window)
    okay_button.grid(row=2, column=0, pady=10)
    cancel_button = ttk.Button(warning_window, text="Cancel", command=sys.exit)
    cancel_button.grid(row=2, column=1, pady=10, padx=10)

    # Make the warning window a modal window
    warning_window.grab_set()

    # Display the warning window on top of everything else
    warning_window.lift()
    warning_window.wm_attributes("-topmost", True)
    warning_window.attributes("-topmost", True)
