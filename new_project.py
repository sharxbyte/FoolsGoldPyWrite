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

# Function to update project details and update main window label
def save_project_details(work_type_entry, author_name_entry, work_title_entry, year_entry, update_main_window_info):
    work_type = work_type_entry.get()
    author_name = author_name_entry.get()
    work_title = work_title_entry.get()
    year = year_entry.get()

    if not all([work_type, author_name, work_title, year]):
        messagebox.showwarning("Error", "Please fill in all fields.")
        return

    # Update the project information in the main window
    update_main_window_info(work_type, author_name, work_title, year)
    project_info_window.destroy()

# Function to create a window for updating project information
def update_project_info(update_main_window_info):
    global project_info_window

    project_info_window = tk.Toplevel()
    project_info_window.title("Update Project Information")

    # Create entry fields for work type, author name, work title, and year
    tk.Label(project_info_window, text="Work Type:").grid(row=0, column=0)
    work_type_entry = tk.Entry(project_info_window)
    work_type_entry.grid(row=0, column=1)

    tk.Label(project_info_window, text="Author Name:").grid(row=1, column=0)
    author_name_entry = tk.Entry(project_info_window)
    author_name_entry.grid(row=1, column=1)

    tk.Label(project_info_window, text="Work Title:").grid(row=2, column=0)
    work_title_entry = tk.Entry(project_info_window)
    work_title_entry.grid(row=2, column=1)

    tk.Label(project_info_window, text="Year:").grid(row=3, column=0)
    year_entry = tk.Entry(project_info_window)
    year_entry.grid(row=3, column=1)

    # Save and Cancel buttons
    save_button = tk.Button(project_info_window, text="Save", command=lambda: save_project_details(work_type_entry, author_name_entry, work_title_entry, year_entry, update_main_window_info))
    save_button.grid(row=4, column=0)

    cancel_button = tk.Button(project_info_window, text="Cancel", command=project_info_window.destroy)
    cancel_button.grid(row=4, column=1)

