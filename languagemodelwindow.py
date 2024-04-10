# Standard library imports
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Local imports
import importlib
from definitions import *

class CustomTitleBar(ttk.Frame):
        def __init__(self, master=None, **kwargs):
            super().__init__(master=master, **kwargs)

            # Add the window icon
            window_icon = tk.PhotoImage(file="icon.gif")
            self.icon_label = ttk.Label(self, image=window_icon)
            self.icon_label.image = window_icon
            self.icon_label.pack(side="left", padx=5, pady=5)

            # Add the window title
            self.title_label = ttk.Label(self, text=master.title(), foreground='#1f1714')
            self.title_label.pack(side="left", padx=5, pady=5)

            # Add the close button
            self.close_button = ttk.Button(self, text="X", command=self.close_window)
            self.close_button.pack(side="right", padx=5, pady=5)

        def close_window(self):
            self.master.destroy()


class languagemodelwindow:
    def __init__(self, parent):
        self.parent = parent
        self.selected_model = tk.StringVar()
        self.selected_model.set("gpt-3.5-turbo")

        self.window = tk.Toplevel(self.parent)

        # Create a label to display instructions
        instructions_label = tk.Label(self.window, text="Please select a language model:")
        instructions_label.pack(padx=10, pady=10)

        # Create a dropdown to select the language model
        model_options = ["text-davinci-003", "gpt-3.5-turbo", "gpt-4", "other"]
        model_dropdown = ttk.Combobox(self.window, values=model_options, textvariable=self.selected_model)
        model_dropdown.pack(padx=10, pady=10)

        # Create a text box for entering a custom language model
        self.custom_model_text = tk.StringVar()
        self.custom_model_text.set("")
        custom_model_entry = tk.Entry(self.window, textvariable=self.custom_model_text, state="disabled")
        custom_model_entry.pack(padx=10, pady=10)

        # Create a button to confirm the language model selection
        confirm_button = tk.Button(self.window, text="Confirm", command=self.confirm_selection)
        confirm_button.pack(padx=10, pady=10)

        # Create a button to cancel the selection and exit the program
        cancel_button = tk.Button(self.window, text="Cancel", command=self.cancel_selection)
        cancel_button.pack(padx=10, pady=10)

        # Bind a function to the dropdown to enable/disable the custom model entry
        model_dropdown.bind("<<ComboboxSelected>>", self.toggle_custom_model_entry)

    def toggle_custom_model_entry(self, event):
        if self.selected_model.get() == "other":
            self.custom_model_text.set("")
            custom_model_entry = self.window.children["!entry"]
            custom_model_entry.config(state="normal")
        else:
            custom_model_entry = self.window.children["!entry"]
            custom_model_entry.config(state="disabled")
