#Standard library imports
import os
import shutil


#Third-party library imports
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk


# Open a window with a prompt for a "project title", and buttons to save or cancel. This will be displayed at the top of the main window until the new project button is clicked again.
def save_project(root, definitions, logger):
    title = project_title_entry.get()
    if title == "":
        messagebox.showwarning("Error", "Please enter a project title.")
    if not title:
        title = "workingtitle"
    project_title_label.configure(text=f"Project: {title}")
    project_title_entry.delete(0, tk.END)
    project_title_window.destroy()

def save_log_file(root, definitions, logger):
    global log_loaded, log_file

    # If log is not loaded, return
    if not log_loaded:
        return

    # Prompt user to save the log file
    filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
    selected_file = filedialog.asksaveasfilename(title="Save Log", filetypes=filetypes)
    
    if not selected_file:
        return

    # Check if the log file exists
    if os.path.exists(log_file):
        # Save the log file
        shutil.copyfile(log_file, selected_file)
    else:
        messagebox.showerror("Error", "Log file not found.")
