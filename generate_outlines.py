# Standard library imports
import csv
import datetime
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
import openai

# Local imports
import importlib
import inspect
from definitions import *

# define function to generate outlines
def generate_outlines():
    # load interview from file
    with open("interview.txt", "r") as f:
        interview = f.read()
    
    show_api_warning(main_window)

    # generate outlines using GPT API
    prompt = (f"Generate 3 outlines for a book based on this interview:\n\n{interview}\n\n")
    completions = openai.Completion.create(engine="selected_model", prompt=prompt, max_tokens=2048, n=3, stop=None, temperature=0.5)
    
    # parse outline choices from API response
    outlines = []
    for choice in completions.choices:
        outline = choice.text.strip().replace("\n", " ")
        outlines.append(outline)
    
    # display outline choices in a new window
    outline_window = tk.Toplevel(master=main_window)
    outline_window.title("Choose an Outline")
    
    ttk.Label(outline_window, text="Select an outline:").grid(column=0, row=0, padx=10, pady=10)
    
    var1 = tk.StringVar(value=outlines[0])
    ttk.Radiobutton(outline_window, text=outlines[0], variable=var1, value=outlines[0]).grid(column=0, row=1, padx=10, pady=10, sticky="w")
    
    var2 = tk.StringVar(value=outlines[1])
    ttk.Radiobutton(outline_window, text=outlines[1], variable=var1, value=outlines[1]).grid(column=0, row=2, padx=10, pady=10, sticky="w")
    
    var3 = tk.StringVar(value=outlines[2])
    ttk.Radiobutton(outline_window, text=outlines[2], variable=var1, value=outlines[2]).grid(column=0, row=3, padx=10, pady=10, sticky="w")
    
    def save_outline():
        # write selected outline to file
        with open("outline.txt", "w") as f:
            f.write(var1.get())
        outline_window.destroy()
    
    ttk.Button(outline_window, text="Save Outline", command=save_outline).grid(column=0, row=4, padx=10, pady=10)


