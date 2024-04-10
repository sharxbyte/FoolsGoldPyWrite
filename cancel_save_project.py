# Standard library imports
import tkinter as tk

# Third-party library imports
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
from definitions import *

def cancel_save_project():
    project_title_entry.delete(0, tk.END)
    project_title_window.destroy()

    project_title_window = tk.Toplevel(master=main_window)
    project_title_window.title("New Project")
    project_title_window.geometry("300x100")

    project_title_label = ttk.Label(main_window, text="Project: None")
    project_title_label.place(relx=0.5, rely=0.1, anchor="center")

    project_title_entry = ttk.Entry(project_title_window, width=30)
    project_title_entry.pack(padx=10, pady=10)

    save_button = ttk.Button(project_title_window, text="Save", command=save_project)
    save_button.pack(side="right", padx=10, pady=10)

    cancel_button = ttk.Button(project_title_window,text="Cancel",
    command=cancel_save_project)

    cancel_button.pack(side="right", padx=10, pady=10)
    project_title_entry.focus_set()

    # Arrange widgets in grid
    project_title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    project_title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    save_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    cancel_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    new_project_window.protocol("WM_DELETE_WINDOW", new_project_window.destroy)

    # Create a new directory, log.txt file, and clear any interview data from the tables
    create_new_project()

    # Check that the API key is still valid
    check_api_key_validity()

