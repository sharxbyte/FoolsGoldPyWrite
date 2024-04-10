# Standard library imports
import os
import tkinter as tk
from tkinter import ttk

# Third-party library imports
import openai
from PIL import Image, ImageTk

# Local imports
from definitions import *

def load_api_window():
    # Create the window
    api_window = tk.Toplevel()
    api_window.title("OpenAI API Key")
    
    # Calculate the window size as 30% of the screen size
    screen_width = api_window.winfo_screenwidth()
    screen_height = api_window.winfo_screenheight()
    window_width = int(screen_width * 0.30)
    window_height = int(screen_height * 0.30)
    api_window.maxsize(window_width, window_height)

    # Center the window
    position_right = int(api_window.winfo_screenwidth()/2 - api_window.winfo_width()/2)
    position_down = int(api_window.winfo_screenheight()/2 - api_window.winfo_height()/2)
    api_window.geometry(f"+{position_right}+{position_down}")

    def on_submit(api_key):
        # Set the API key
        openai.api_key = api_key

        # Create a new window to display the language model options
        language_model_window = tk.Toplevel(api_window)
        language_model_window.title("Select Language Model")

    def on_offline_mode():
        # Close the API key window
        api_window.destroy()

        # Add "Offline Mode" to the title of all windows in the program
        update_window_titles("Offline Mode")

    def update_window_titles(offline_mode_text):
        # Iterate through all windows in the application
        for window in main_window.winfo_children():
            # Update the window title by appending "Offline Mode"
            window.title(window.title() + f" - {offline_mode_text}")

            # If the window has any child windows, update their titles as well
            for child_window in window.winfo_children():
                child_window.title(child_window.title() + f" - {offline_mode_text}")

    # Create the API key entry label and text field
    api_key_label = ttk.Label(api_window, text="Enter your OpenAI API Key:")
    api_key_label.pack(side="top", pady=10)
    api_key_text = tk.StringVar()
    api_key_entry = ttk.Entry(api_window, textvariable=api_key_text)
    api_key_entry.pack(side="top", pady=10)

    # Create the submit button
    submit_button = ttk.Button(api_window, text="Submit", command=lambda: on_submit(api_key_text.get()))
    submit_button.pack(side="left", padx=10)

    # Create the cancel button
    cancel_button = ttk.Button(api_window, text="Cancel", command=api_window.destroy)
    cancel_button.pack(side="right", padx=10)

    # Create the offline mode button
    offline_mode_button = ttk.Button(api_window, text="Offline Mode", command=lambda: on_offline_mode())
    offline_mode_button.pack(side="bottom", pady=10)

    # Make the window a modal window
    api_window.grab_set()

    # Display the window on top of everything else
    api_window.lift()
