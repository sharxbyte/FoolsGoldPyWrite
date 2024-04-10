# Standard library imports
import logging
import tkinter as tk
import time

# Third-party library imports
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Local imports
import importlib


def open_reference_info(event):
    # Get the clicked table widget
    clicked_table = event.widget

    # Get the selected item from the clicked table
    selected_item = clicked_table.selection()

    logger.setLevel(logging.CRITICAL)  # Disable logging

    character_id = event.widget.focus()
    if not character_id:
        return

    reference_info = event.widget.item(character_id)["values"]

    # Get the character information from the dictionary
    character_info = get_character_info(character_id)

    def update_reference_info():
        updated_info = [get_value() for get_value in get_value_functions]
        for i, new_value in enumerate(updated_info):
            event.widget.item(character_id, values=reference_info[:i] + [new_value] + reference_info[i + 1:])

        # Create Notes text box
        notes_label = tk.Label(open_reference_info, text="Notes:")
        notes_label.grid(row=len(reference_info), column=0, padx=10, pady=10)

        character_text_box = tk.Text(open_reference_info, height=5, width=40)
        character_text_box.grid(row=len(reference_info), column=1, padx=10, pady=10)

        # Create a new frame to hold the buttons
        button_frame = ttk.Frame(open_reference_info)
        button_frame.grid(row=len(reference_info) + 1, column=0, columnspan=2, pady=10)

        # Add a "Save" button to the frame
        save_button = ttk.Button(button_frame, text="Save Character", command=lambda: save_details(character_id, character_text_box.get("1.0", tk.END)))
        save_button.grid(row=0, column=0, padx=5, pady=10)

        # Add a "Cancel" button to the frame
        cancel_button = ttk.Button(button_frame, text="Cancel", command=open_reference_info.destroy)
        cancel_button.grid(row=0, column=1, padx=5, pady=10)

    # Create a new window to display the reference info
    reference_info_window = tk.Toplevel(non_fiction_window)
    reference_info_window.title(f"Reference Info: {reference_info[0]}")

    # Create a button to resume the interview
    resume_interview_button = ttk.Button(open_reference_info, text="Resume Interview", command=lambda: resume_interview(character_id))
    resume_interview_button.grid(side="bottom", pady=10)

    # Center the window on the screen
    screen_width = open_reference_info.winfo_screenwidth()
    screen_height = open_reference_info.winfo_screenheight()
    window_width = open_reference_info.winfo_reqwidth()
    window_height = open_reference_info.winfo_reqheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    open_reference_info.geometry(f"+{x}+{y}")

    get_value_functions = []
    for i, (field, value) in enumerate(reference_info):
        label = tk.Label(open_reference_info, text=field + ":")
        label.grid(row=i, column=0, sticky="E", padx=(10, 0), pady=(10, 0))
        text_box = tk.Entry(open_reference_info)
        text_box.insert(tk.END, value)
        text_box.grid(row=i, column=1, padx=(0, 10), pady=(10, 0))

        def get_value():
            return text_box.get()

        get_value_functions.append(get_value)

    # Create Notes text box
    notes_label = tk.Label(open_reference_info, text="Notes:")
    notes_label.grid(row=len(reference_info), column=0, padx=10, pady=10)

    character_text_box = tk.Text(open_reference_info, height=5, width=40)
    character_text_box.grid(row=len(reference_info), column=1, padx=10, pady=10)

    # Create a new frame to hold the buttons
    button_frame = ttk.Frame(open_reference_info)
    button_frame.grid(row=len(reference_info) + 1, column=0, columnspan=2, pady=10)

    # Add a "Save" button to the frame
    save_button = ttk.Button(button_frame, text="Save Character", command=lambda: save_details(character_id, character_text_box.get("1.0", tk.END)))
    save_button.grid(row=0, column=0, padx=5, pady=10)

    # Add a "Cancel" button to the frame
    cancel_button = ttk.Button(button_frame, text="Cancel", command=open_reference_info.destroy)
    cancel_button.grid(row=0, column=1, padx=5, pady=10)

    logger.setLevel(logging.INFO)  # Enable logging again


