# Standard library imports
import datetime
import logging
import os
import shutil
import sys
import time

# Third-party library imports
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Local imports
from definitions import *
import importlib
import inspect

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        error_window = tk.Toplevel(master=main_window)
        error_window.title("Error")
        error_label = ttk.Label(error_window, text="Please complete the steps in order before attempting this action.")
        error_label.grid(padx=10, pady=10)
        ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.grid(padx=10, pady=10)
        return False
    else:
        return True
