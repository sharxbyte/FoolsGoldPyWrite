import csv
import logging
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def resume_interview():
    # Get the character ID from the details window title
    character_id = details_window.title().split(": ")[-1]

    # Read the character data from the log file
    with open("log.txt", "r") as f:
        character_data = f.read()

    # Find the character data based on the character ID
    start_tag = f"<{character_id}>"
    end_tag = f"</{character_id}>"
    start_index = character_data.index(start_tag) + len(start_tag)
    end_index = character_data.index(end_tag)

    # Extract the character data from the log file
    character_text = character_data[start_index:end_index]

    # Parse the character data into a dictionary
    character_info = {}
    for line in character_text.split("\n"):
        if ":" in line:
            key, value = line.split(":")
            character_info[key.strip()] = value.strip()

    # Find the first empty text box in the interview section
    interview_frame = details_window.nametowidget(".!frame.!toplevel.!frame3.!frame.!notebook.!frame.!labelframe")
    for widget in interview_frame.winfo_children():
        if isinstance(widget, tk.Entry):
            if not widget.get():
                widget.focus()
                return

    # If all text boxes are filled, focus on the first text box
    interview_frame.winfo_children()[0].focus()
