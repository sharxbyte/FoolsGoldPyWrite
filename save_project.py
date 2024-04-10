#Standard library imports
import datetime
import logging
import os
import shutil
import subprocess
import sys
import time
import webbrowser

#Third-party library imports
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

#Local imports
import importlib
import inspect

# Open a window with a prompt for a "project title", and buttons to save or cancel. This will be displayed at the top of the main window until the new project button is clicked again.
def save_project(root, definitions, logger):
    title = project_title_entry.get()
    if title == "":
        messagebox.showwarning("Error", "Please enter a project title.")
    else:
        project_title_label.configure(text=f"Project: {workingtitle}")
        project_title_entry.delete(0, tk.END)
        project_title_window.destroy()
