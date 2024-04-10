# Standard library imports
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Third-party library imports
from tkinter import messagebox
from tkinter import simpledialog

def update_fplot_data():
    global fplot_data, character_info

    # Get the current fplot data from the file or database
    fplot_data = get_fplot_data()

    # Update the fplot data with the interview data
    for question, answer in character_info.items():
        fplot_data[question] = answer

    # Save the updated fplot data to the file or database
    save_fplot_data(fplot_data)
